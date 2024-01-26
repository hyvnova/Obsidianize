import requests, re, bs4, os, shutil
from dataclasses import dataclass, field
from typing import Set
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from markdownify import markdownify
from urllib import parse

"""
Obsidianize - turn a given url into a obsidian notebook.
- Each link in webpage will be condired a note
- Each note will be saved as a markdown file
"""

INF = float("inf")


INF = float("inf")


class Obsidianize:
    """
    Obsidianize - turn a given url into a obsidian notebook.

    ### Usage:
    ```python
    Obsidianize(
        notebook_name="Bevy Cheatbook",
        url="https://bevy-cheatbook.github.io/introduction.html",
    )
    ```

    ### Parameters:
    - `notebook_name`: The name of the notebook. A directory with this name will be created in the current directory.
    - `url`: The url to obsidianize.
    - `link_search_depth_limit`: The depth limit for searching links. Default: `INF`. Link depth is the number of links away from root url.
    - `link_processing_limit`: The limit for processing links. Default: `INF`. Each link is roughly a note.
    - `selectors`: The selectors to use for finding the title, content and links. Default: 

    ```python
    Obsidianize.Selectors(
        title={"title", "main h1", "h1"},
        content={"main",},
        link={"main a", "a"},
    )
    ```
    - `silent`: If `True`, no output will be printed. Default: `False`.
    """

    @dataclass
    class Selectors:
        title: Set[str] = field(default_factory=lambda: {"title", "main h1", "h1"})
        content: Set[str] = field(
            default_factory=lambda: {
                "main",
            }
        )
        link: Set[str] = field(
            default_factory=lambda: {
                "main a",
                "a",
            }
        )

    def __init__(
        self,
        notebook_name: str,
        url: str,
        link_search_depth_limit: int | float = INF,
        link_processing_limit: int | float = INF,
        selectors: Selectors = Selectors(),
        silent: bool = False,
    ):
        self.notebook_name = notebook_name
        self.url = url
        self.link_search_depth_limit = link_search_depth_limit
        self.link_processing_limit = link_processing_limit
        self.selectors = selectors

        self.found_links: Set[str] = set()
        self.processed_link_count = 0
        self.url_title_map = {}

        self.domain = parse.urlparse(url).scheme + "://" + parse.urlparse(url).netloc

        if silent:
            self.print = lambda *args, **kwargs: None
        else:
            self.print = print

        # Clear the notebook directory or create it if it doesn't exist
        self.clear_directory(self.notebook_name)
        if not os.path.exists(self.notebook_name):
            os.mkdir(self.notebook_name)

        self.print("Notebook name: ", notebook_name)
        self.print("URL: ", url)

        # Start the process
        self.get_pages_and_create_note(self.url)

    def clear_directory(self, directory_path: str):
        if not os.path.exists(directory_path):
            return
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

            self.print(f"Directory {directory_path} cleared successfully.")

        except Exception as e:
            self.print(f"Error clearing directory {directory_path}: {e}")

    def find_element(
        self, soup: bs4.BeautifulSoup, selectors: Set[str]
    ) -> bs4.Tag | None:
        """
        Find the first element in the soup that matches the given selectors
        """
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element

        return None

    def find_links(self, soup: bs4.BeautifulSoup) -> Set[str]:
        """
        Find all the (internal) links in the soup
        """
        links = set()

        for selector in self.selectors.link:
            for link in soup.select(selector):
                href = link.get("href")
                if not href or not href.startswith("/") or (href in links):  # type: ignore
                    continue

                links.add(href)

        return links

    def normalize_title(self, t: str) -> str:
        """
        Normalize the title - remove characters that are not allowed in file names
        """
        return re.sub(r"[^\w\s]", "", t)

    def get_title_from_url(self, url: str) -> str:
        """
        Get the title from the url (internal link. starts with /)
        """

        if url in self.url_title_map:
            return self.url_title_map[url]

        res = requests.get(f"{self.domain}{url}")
        try:
            res.raise_for_status()  # Check for errors
        except Exception as e:
            self.print(f"Error getting title from url: {e}")
            return ""

        self.print("Getting title from url: ", f"{self.domain}{url}")

        soup = bs4.BeautifulSoup(res.text, "html.parser")

        # Get the title of the page
        title = self.find_element(soup, self.selectors.title)
        if not title:
            self.print("No title found.")
            return ""

        title = self.normalize_title(title.text.strip())
        self.url_title_map[url] = title
        return title

    def tag_to_html(self, tag: bs4.Tag) -> str:
        """
        Convert the given tag to plain html text
        """
        return "".join([str(c) for c in tag.contents])

    def create_note(self, title: str, body: bs4.Tag, references: Set[str] = set()):
        """
        Create a markdown file with the given title and content
        """

        if os.path.exists(f"{self.notebook_name}/{title}.md"):
            self.print("Note already created. Skipping...")
            return

        # convert tag into html text
        content = self.tag_to_html(body)

        # convert html to markdown
        content = markdownify(content)

        with open(f"{self.notebook_name}/{title}.md", "w", encoding="utf-8") as file:
            file.write(content)

            file.write("\n\n")
            file.write("### References\n")
            for ref in references:
                file.write(f"[[{self.get_title_from_url(ref)}]] ")

    def process_link(self, link: str, depth: list[int]):
        self.processed_link_count += 1
        if self.processed_link_count > self.link_processing_limit:
            self.print(
                f"Reached the link listing limit. Not processing any more links."
            )
            return

        # create note for the link
        url = self.domain + link
        self.print("Processing link: ", url)
        depth[0] += 1
        self.get_pages_and_create_note(url=url, depth=depth)

    def get_pages_and_create_note(self, url: str, depth=[0]):
        """
        Get the page from the given url and create it's note, then continue to repeat the process with links found at the page.
        """
        if url in self.found_links:
            self.print("Note already created. Skipping...")
            return

        res = requests.get(url)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, "html.parser")

        # Get the title of the page
        title = self.find_element(soup, self.selectors.title)
        if not title:
            self.print("No title found. Skipping...")
            return

        # normalize the title
        title = self.normalize_title(title.text.strip())

        # Get the content of the page
        content = self.find_element(soup, self.selectors.content)
        if not content:
            self.print("No content found. Skipping...")
            return

        self.print(f"Creating note for {title}...")

        # Get all the links in body with name
        # filter out the external links
        links = self.find_links(soup)

        self.print(f"Found {len(links)} links in {title}...")

        # Create the note
        Thread(target=self.create_note, args=(title, content, links)).start()
        self.found_links.add(url)

        if depth[0] > self.link_search_depth_limit:
            self.print(
                f"Reached the depth limit. Skipping... {len(links)} links; at {title}"
            )
            return

        if self.processed_link_count > self.link_processing_limit:
            self.print(
                f"Reached the link listing limit. Skipping... {len(links)} links; at {title}"
            )
            return

        # Process the links
        with ThreadPoolExecutor() as executor:
            executor.map(self.process_link, links, [depth] * len(links))
