import requests, re, bs4, os, shutil
from dataclasses import dataclass, field
from typing import Dict, Set
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from markdownify import markdownify
from urllib import parse

INF = float("inf")
Url = str

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
    - `cache`: Cache options. Default: `Obsidianize.CacheOptions()` - Enabled, save and load cache from the current directory. 
    """

    @dataclass
    class Selectors:
        title: Set[str] = field(default_factory=lambda: {"main h1", "h1", "title"})

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

    @dataclass
    class CacheOptions:
        save: bool = True # Save the cache
        load: bool = True # Load saved cache (if exists)
        path: str = "./" # Directory to save the cache in


    def get_cache_file_path(self, notebook_name: str) -> str:
        return f"{notebook_name}.obsidianize.cache" 

    def __init__(
        self,
        notebook_name: str,
        url: str,
        link_search_depth_limit: int | float = INF,
        link_processing_limit: int | float = INF,
        selectors: Selectors = Selectors(),
        silent: bool = False,
        cache: CacheOptions = CacheOptions() 
    ):
        self.notebook_name = notebook_name
        self.url = url
        self.link_search_depth_limit = link_search_depth_limit
        self.link_processing_limit = link_processing_limit
        self.selectors = selectors
        self.cache: Obsidianize.CacheOptions = cache
        self.depth: int = 0

        self.found_links: Set[str] = set()
        self.processed_link_count = 0
        self.url_title_map: Dict[Url, str] = {} # Map from url to title

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
        self.print("Domain: ", self.domain)

        # Load the cache
        if self.cache.save:
            self.load_cache()

        # Start the process
        self.get_page(self.url)

    # Save cache on destruction
    def __del__(self):
        if not self.cache.save:
            return
        
        # Make sure the cache directory exists
        if not os.path.exists(self.cache.path):
            os.mkdir(self.cache.path)

        with open(self.get_cache_file_path(self.notebook_name), "w", encoding="utf-8") as file:
            for url, title in self.url_title_map.items():
                file.write(f"{url},{title}\n")


    def load_cache(self):
        """
        Load the cache from the cache file
        """

        cache_path = self.get_cache_file_path(self.notebook_name)

        if not os.path.exists(cache_path):
            return

        with open(cache_path, "r", encoding="utf-8") as file:
            for line in filter(str.isspace, file.readlines()):
                url, title = line.split(",")
                self.url_title_map[url] = title


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
        @param soup: The soup to find links in
        @return: A set of relative links (don't include the domain)
        """
        links = set()

        for selector in self.selectors.link:
            for link_element in soup.select(selector):
                href: str | None = link_element.get("href")  # type: ignore
                if not href:
                    continue

                url = parse.urlparse(href)

                # if the link is internal
                if href.startswith("/") or url.netloc == self.domain:
                    links.add(href)

        return links

    def normalize_title(self, t: str) -> str:
        """
        Normalize the title - remove characters that are not allowed in file names
        """
        return re.sub(r"[^\w\s]", "", t)

    def get_title_from_url(self, link: str) -> str:
        """
        Get the title from the url 
        """

        # If the title is already cached, return it    
        if link in self.url_title_map:
            return self.url_title_map[link]

        try:
            res = requests.get(self.domain + link)
            res.raise_for_status()  # Check for errors

        except Exception as e:
            self.print(f"Error getting title from url: {e}")
            return link

        soup = bs4.BeautifulSoup(res.text, "html.parser")

        # Get the title of the page
        title = self.find_element(soup, self.selectors.title)
        if not title:
            self.print("No title found. for url: ", link)
            return link

        title = self.normalize_title(title.text.strip())
        self.url_title_map[link] = title
        return title

    def tag_to_html(self, tag: bs4.Tag) -> str:
        """
        Convert the given tag to plain html text
        """
        return "".join([str(c) for c in tag.contents])

    def create_note(self, title: str, body: bs4.Tag, references: Set[str] = set()):
        """
        Create a markdown file with the given title and content
        @param title: The title of the note
        @param body: The body of the note - a tag containing the content
        @param references: A set of references (Internal Links) to add to the note
        """

        if os.path.exists(f"{self.notebook_name}/{title}.md"):
            return

        # convert tag into html text
        content = self.tag_to_html(body)

        # convert html to markdown
        content = markdownify(content)
        ref_titles = [self.get_title_from_url(ref) for ref in references]

        # make links on content point to notes
        for (ref, title) in zip(references, ref_titles):
            # remove domain from the link
            ref = ref.replace(self.domain, "")
            content = content.replace(ref, f"[[{title}.md]]")

        with open(f"{self.notebook_name}/{title}.md", "w", encoding="utf-8") as file:
            file.write(content)

    def process_link(self, link: str):
        if self.processed_link_count > self.link_processing_limit:
            return
        self.processed_link_count += 1

        if self.depth > self.link_search_depth_limit:
            return
        self.depth += 1

        # create note for the link
        self.get_page(url=link)

    def get_page(self, url: str):
        """
        Get the page from the given url and create it's note, then continue to repeat the process with links found at the page.
        """
        if url in self.found_links:
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

        self.print(f"Creating note for: {title}")

        # Get all the internal links in the page
        links = self.find_links(soup)
        self.print(f"Found {len(links)} links in: {title}")

        # Create the note
        Thread(target=self.create_note, args=(title, content, links)).start()
        self.found_links.add(url)

        # Filter out the links that have already been processed
        links = links.difference(self.found_links)

        if len(links) == 0:
            return

        if self.depth > self.link_search_depth_limit:
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
        links = list(map(lambda link: self.domain + link, links)) # Add the domain to the links
        with ThreadPoolExecutor() as executor:
            executor.map(self.process_link, links)
