# Humanoid 👽

[![GitHub license](https://img.shields.io/badge/license-MIT-blue)](#license)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)](#contributors)

Humanoid is a simple, natural language interface for orchestrating autonomous agents. With Humanoid, you can summon and execute AI agents using straightforward prompts. This project leverages the power of OpenAI's API to create and manage agents that can perform various tasks.

## Features ✨

- **Natural Language Interface**: Interact with AI agents using simple text prompts.
- **Autonomous Agents**: Create and manage agents that can perform tasks independently.
- **Configurable**: Easily configure agents, tasks, and crew settings.
- **Error Handling**: Robust error handling to ensure smooth operation.

## Installation 🛠️

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/humanoid.git
   cd humanoid
   ```

2. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   ```sh
   echo "OPENAI_API_KEY=your-api-key" > .env
   ```

## Usage 🚀

### Running the Humanoid

You can run the Humanoid by executing the `basic_run.py` script. This script will prompt you to enter a natural language prompt to summon autonomous agents.

```sh
python examples/basic_run.py
```

### Example Prompt

```
Enter a prompt to summon autonomous agents: Create a report on the current weather in New York.
```

## Project Structure 📂

- `humanoid.py`: Main class for the Humanoid application.
- `examples/basic_run.py`: Example script to run the Humanoid with a user prompt.
- `README.md`: Project documentation.

## Contributing 🤝

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more details.

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements 🙏

- [OpenAI](https://openai.com) for providing the API.
- [CrewAI](https://crewai.com) for the agent and task management framework.

Feel free to open an issue or submit a pull request if you have any questions or suggestions!
