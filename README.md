# requirements

```prompt lib with some tooling
pip install --upgrade openai
pip install python-dotenv
pip install anthropic


pip install rich

```

# setup

`.env.example` - setup your keys and save as `.env`

# usage

## Run a prompt from your library

```
prr run common/dingo-dog
```

## Run a prompt from your library against specific model

```
prr run --model anthropic/claude-v1 concept-maps/subconcepts-of-buddhism
```

## Run a prompt from your library and save output to file

```
prr run common/dingo-dog > /tmp/dingo-response.txt
```

## Test "adjectives" version of "common/dingo-dog" prompt against defined test expectations

```
prr test common/dingo-dog/adjectives
```

# library


## prompts

Prompts are versions/attempts at creating prompt text content.

prompts/dingo-dog (if just a file)

prompts/dingo-dog/prompt (file)
prompts/dingo-dog/crazy-chihuahua-mix (file)

## tests

Tests describe expected effect we're looking for with different LLMs we're considering. They include latency, token efficiency and content expectations.

prompts/dingo-dog/prompt/prompt
prompts/dingo-dog/prompt/test.yaml

prompts/dingo-dog/crazy-chihuahua-mix/prompt
prompts/dingo-dog/crazy-chihuahua-mix/test.yaml

## runs

Each modified prompt run is saved for later analysis.

prompts/dingo-dog/crazy-chihuahua-mix/runs
prompts/dingo-dog/crazy-chihuahua-mix/runs/2023-05-02-22:39.31337/


# other

## provider - model
## library - prompt - template - text

# Prr - Prompt Runner

![Prr - Prompt Runner Logo](/images/prr-logo.png)

Welcome to **Prr - Prompt Runner**! An innovative Python-based toolchain designed to help you run prompts across multiple Large Language Models (LLMs), whether they are hosted locally or accessible through APIs. Easily refine your parameters and prompts to achieve the best results.

Prr is released as an open-source project under the MIT License.

## Features

- Easy integration with Anthropic and OpenAI APIs
- Simple setup with `.env` API keys
- Command-line execution of prompts
- YAML configuration files for each prompt
- Refine your prompts and parameters with ease
- Expandable to other LLM providers

## Getting Started

To start using Prr, simply follow these steps:

1. Clone the repo: `git clone https://github.com/yourusername/prr.git`
2. Navigate to the project directory: `cd prr`
3. Set up a virtual environment (optional but recommended): `python3 -m venv venv`
4. Activate the virtual environment:
   - On Linux/MacOS: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`
5. Install the required packages: `pip install -r requirements.txt`
6. Fill in your API keys for Anthropic and OpenAI in the `.env` file.
7. Run your first prompt: `./bin/run <prompt_path>`

## Example: Running a Prompt with Configuration

Let's say you have a prompt named `example_prompt.txt`. To run it with Prr, you'll need to create a configuration file named `example_prompt.config` in YAML format.

Here's an example of a simple configuration file:

```yaml
llm_provider: "openai"
api_key: "your_openai_api_key_here"
model: "text-davinci-002"
max_tokens: 100
```

With the configuration file in place, simply run the prompt using Prr:

```bash
./bin/run example_prompt.txt
```

This will run the prompt with the specified parameters, leveraging the power of the chosen LLM provider.

## Contributing

We'd love your help in making Prr even better! To contribute, please follow these steps:

1. Fork the repo
2. Create a new branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some new feature'`
4. Push the branch to your fork: `git push origin feature/my-new-feature`
5. Create a new Pull Request

## License

Prr - Prompt Runner is released under the [MIT License](/LICENSE).

## Support and Community

Join our [Gitter community](https://gitter.im/prr-prompt-runner/community) for help, discussions, and updates about Prr.

## Screenshots and Screencasts

![Screenshot of Prr in action](/images/screenshot.png)

[![Screencast: Using Prr](/images/screencast-thumbnail.png)](https://youtu.be/your_video_link)

Watch our [screencast](https://youtu.be/your_video_link) to see Prr in action and learn how to get the most out of your prompt running experience.

---

Happy prompting!