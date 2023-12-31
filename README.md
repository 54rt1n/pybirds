# PyBirds

## Overview

The wordbirds are back, and this time they're in Python! PyBirds is a project that allows you to generate unique, funny, and creative phrases using characters with distinct personalities. Built to utilize OpenAI compatable API's, this project provides a user-friendly way to interact with the language model and get interesting outputs.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
    - [Generate Phrases](#generate-phrases)
    - [List Available Birds](#list-available-birds)
    - [List Available Styles](#list-available-styles)
- [Configuration](#configuration)
- [Local Models](#local-models)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Installation

### Installing Poetry

If you don't have Poetry installed, you can install it using the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or refer to the [official Poetry installation guide](https://python-poetry.org/docs/#installation) for more options.

### Installing PyBirds

To install PyBirds, clone the repository, set up a Poetry shell, and then install the dependencies:

```bash
git clone https://github.com/54rt1n/pybirds.git
cd pybirds
poetry shell
poetry install
```

## Usage

### Generate Phrases

To generate a phrase for a specific bird and one or more styles, run:

```bash
python -m bird generate -n Joey -s Insult
```

This will output a phrase generated by Joey the Red-Tailed Hawk, in the style of an Insult.

### List Available Birds

To list all the available birds, run:

```bash
python -m bird list_birds
```

### List Available Styles

To list all the available styles, run:

```bash
python -m bird list_styles
```

## Configuration

Configuration options like API key, max tokens, and data paths can be modified in the `config.json` file located in the `config` folder.

## Local Models

You can use the default model hosted on the OpenAI API, or you can run the model locally.  To run the model locally, you can download [llama.cpp](https://github.com/ggerganov/llama.cpp) and use a GGUF model from [HuggingFace](https://huggingface.co/models?search=gguf).

Once installed, you run the model locally in two steps:
```bash
CTX=2048
MODEL=llama-2-13b-chat.q8_0.gguf
NGL=20 # or whatever your GPU can handle
# Both of these need to be running at the same time, so you may want to use tmux
./server -c $CTX -m $MODEL -ngl $NGL

python3 ./examples/server/api_like_OAI.py --host 0.0.0.0
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the Apache 2.0 License. See `LICENSE` for more details.

## Author

by Martin Bukowski <mbukowski@bmds.us>
