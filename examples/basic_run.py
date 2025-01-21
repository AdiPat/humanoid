from humanoid import Humanoid
from rich.console import Console
from rich.markdown import Markdown

console = Console()


def run():
    prompt = input("Enter a prompt to summon autonomous agents: ")
    humanoid = Humanoid()
    result = humanoid.run(prompt=prompt)
    markdown = Markdown(f"## Result\n\n{result}")
    console.print(markdown)


run()
