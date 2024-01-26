from typing import Set
import requests, re, bs4, os, shutil
from urllib import parse
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from markdownify import markdownify
"""
Obsidianize - turn a given url into a obsidian notebook.
- Each link in webpage will be condired a note
- Each note will be saved as a markdown file
"""

INF = float("inf")

def required_input(prompt: str) -> str:  # type: ignore
    """
    Prompt the user for input and return the input. If the input is try again, if no input again then exit.
    """
    inp: str = (input(prompt) or "").strip()

    # retry once
    if not inp:
        inp = (input(prompt) or "").strip()

    if not inp:
        print("No input provided. Exiting...")
        exit(1)

    return inp

def normalize_title(t: str) -> str:
    """
    Normalize the title - remove characters that are not allowed in file names
    """
    return re.sub(r"[^\w\s]", "", t)


# notebook_name = required_input("Enter the notebook name: ")
# url = required_input("Enter the url: ")
# domain = f"{parse.urlparse(url).scheme}://{parse.urlparse(url).netloc}"

notebook_name = "test"
url = "https://bevy-cheatbook.github.io/introduction.html"
domain = "https://bevy-cheatbook.github.io"


print("Notebook name: ", notebook_name)
print("URL: ", url)
print("Domain: ", domain)


LINK_SEARCH_DEPTH_LIMIT = INF 
# total number of links to be processed
LINK_PROCESSING_LIMIT = 1

found_links = set()
processed_link_count = 0
url_title_map = {}


def clear_directory(directory_path: str):
    try:
        # Remove all files in the directory
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                os.unlink(file_path)

        # Remove all subdirectories and their contents
        for subdirectory_name in os.listdir(directory_path):
            subdirectory_path = os.path.join(directory_path, subdirectory_name)
            if os.path.isdir(subdirectory_path):
                shutil.rmtree(subdirectory_path)

        print(f"Directory {directory_path} cleared successfully.")

    except Exception as e:
        print(f"Error clearing directory {directory_path}: {e}")


def get_title_from_url(url: str) -> str:
    """
    Get the title from the url (internal link. starts with /)
    """

    if url in url_title_map:
        return url_title_map[url]

    res = requests.get(f"{domain}{url}")
    try:
        res.raise_for_status()  # Check for errors
    except Exception as e:
        print(f"Error getting title from url: {e}")
        return ""

    print("Getting title from url: ", f"{domain}{url}")

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    # Get the title of the page
    title = soup.select_one("title")
    if not title:
        title = soup.select_one("h1")
    if not title:
        print("No title found.")
        return ""

    title = normalize_title(title.text.strip())
    url_title_map[url] = title
    return title

def tag_to_html(tag: bs4.Tag) -> str:
    """
    Convert the given tag to html 
    """
    return "".join([str(c) for c in tag.contents])

def create_note(title: str, body: bs4.Tag, references: Set[str] = set()):
    """
    Create a markdown file with the given title and content
    """

    if os.path.exists(f"{notebook_name}/{title}.md"):
        print("Note already created. Skipping...")
        return

    # convert tag into html text
    content =  tag_to_html(body) # convert tag to html text
    content = markdownify(content) # convert html to markdown

    with open(f"{notebook_name}/{title}.md", "w", encoding='utf-8') as file:
        file.write(content)

        file.write("\n\n")
        file.write("### References\n")
        for ref in references:
            file.write(f"[[{get_title_from_url(ref)}]] ")


def process_link(link: str, depth: list[int]):
    global processed_link_count

    processed_link_count += 1
    if processed_link_count > LINK_PROCESSING_LIMIT:
        print(f"Reached the link listing limit. Not processing any more links.")
        return

    # create note for the link
    url = domain + link
    print("Processing link: ", url)
    depth[0] += 1
    get_pages_and_create_note(url=url, depth=depth)


def get_pages_and_create_note(url=url, depth=[0]):
    """
    Get the page from the given url and create it's note, then continue to repeat the process with links found at the page.
    """
    if url in found_links:
        print("Note already created. Skipping...")
        return

    res = requests.get(url)
    res.raise_for_status()  # Check for errors

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    # Get the title of the page
    title = soup.select_one("main h1")
    if not title: title = soup.select_one("h1")
    if not title: title = soup.select_one("title")
    
    if not title:
        print("No title found. Skipping...")
        return

    title = normalize_title(title.text.strip())

    print(f"Creating note for {title}...")

    # Get the content of the page
    content = soup.select_one("main")
    if not content:
        print("No content found. Skipping...")
        return


    # Get all the links in body with name
    # filter out the external links
    links = set()
    for link in soup.select("body a"):
        href = link.get("href")
        if not href or not href.startswith("/") or (href in links):  # type: ignore
            continue

        links.add(href)

    print(f"Found {len(links)} links in {title}...")

    # Create the note
    Thread(target=create_note, args=(title, content, links)).start()
    found_links.add(url)

    if depth[0] > LINK_SEARCH_DEPTH_LIMIT:
        print(f"Reached the depth limit. Skipping... {len(links)} links; at {title}")
        return

    if processed_link_count > LINK_PROCESSING_LIMIT:
        print(
            f"Reached the link listing limit. Skipping... {len(links)} links; at {title}"
        )
        return

    # Process the links
    with ThreadPoolExecutor() as executor:
        executor.map(process_link, links, [depth] * len(links))


clear_directory(notebook_name)

if not os.path.exists(notebook_name):
    os.mkdir(notebook_name)

get_pages_and_create_note()
