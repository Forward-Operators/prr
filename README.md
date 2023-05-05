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