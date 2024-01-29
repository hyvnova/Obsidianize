from obsidianize import Obsidianize

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


# notebook_name = required_input("Enter the notebook name: ")
# url = required_input("Enter the url: ")

notebook_name = "test"
url = "https://bevy-cheatbook.github.io/introduction.html"

Obsidianize(
    notebook_name,
    url,
    cache=Obsidianize.CacheOptions(
        load=False
    )
)
