from humanoid import Humanoid


def run():
    prompt = input("Enter a prompt to summon autonomous agents: ")
    humanoid = Humanoid()
    result = humanoid.run(prompt=prompt)
    print("RESULT:", result)


run()
