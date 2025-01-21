from humanoid import Humanoid
from rich.console import Console
from rich.markdown import Markdown
from datetime import datetime

console = Console()


def run():
    """Run the basic example. This function is called when the script is run."""
    prompt = input("Enter a prompt to summon autonomous agents: ")
    humanoid = Humanoid()
    result = humanoid.run(prompt=prompt)
    markdown = Markdown(f"## Prompt: {prompt}\n\n## Result\n\n{result}")
    console.print(markdown)
    result_bytes_size = len(result.encode("utf-8"))
    console.print(f"Result size: {result_bytes_size} bytes")
    now = datetime.now()
    now_formatted = now.strftime("%Y_%m_%d_%H_%M_%S")
    print("Writing result to file...")
    with open(f"basic_run_result_{now_formatted}.md", "w") as f:
        f.write(result)


run()
