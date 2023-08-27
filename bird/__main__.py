# __main__.py - Martin Bukowski - 2023-08-26
import argparse
import logging
from .core.util import load_config
from .core.api import OAIApi
from .core.rookery import Rookery
from .core.prompter import Prompter
from .core.generator import PhraseWizard

# Initialize logger
logger = logging.getLogger(__name__)

def load_resources():
    """Load resources from configuration."""
    config = load_config()
    api = OAIApi.from_config(**config)
    rook = Rookery.from_config(**config)
    prompter = Prompter.from_config(**config)
    return api, rook, prompter

def generate(args):
    """Generate a phrase for a specified bird and styles."""
    api, rook, prompter = load_resources()
    wizard = PhraseWizard.factory(api=api)

    bird = rook.get_bird(bird_name=args.name)
    if bird is None:
        logger.error(f"Could not find bird with name {args.name}")
        return
    
    # Collect prompts
    prompts = [prompter.get_prompt(style) or bird.get_custom_style(style) for style in args.style]
    prompts.append(bird.get_prompt())

    # Add 'Witty' to styles
    styles_with_witty = args.style + ['Witty']

    phrase = wizard.generate_phrase(bird=bird, prompts=prompts, styles=styles_with_witty)
    print(f"{args.name} [{', '.join(styles_with_witty)}]: {phrase}")

def list_birds(args):
    """List all available birds."""
    _, rook, _ = load_resources()
    print("Available Birds:")
    for bird_name, bird in rook.birds.items():
        print(f"- {bird_name} (Species: {bird.species}, Persona: {bird.persona})")

def list_styles(args):
    """List all available styles."""
    _, _, prompter = load_resources()
    print("Available Styles:")
    for style in prompter.prompts.keys():
        print(f"- {style}")

def main():
    """Main entry point for the command-line application."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    parser = argparse.ArgumentParser(description="Manage bird phrases.")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a phrase for a bird.")
    generate_parser.add_argument("-n", "--name", required=True, help="Name of the bird.")
    generate_parser.add_argument("-s", "--style", action='append', required=True, help="Style of the phrase. Can specify multiple styles.")
    generate_parser.set_defaults(func=generate)

    # List birds command
    list_birds_parser = subparsers.add_parser("list_birds", help="List available birds.")
    list_birds_parser.set_defaults(func=list_birds)

    # List styles command
    list_styles_parser = subparsers.add_parser("list_styles", help="List available styles.")
    list_styles_parser.set_defaults(func=list_styles)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)

if __name__ == "__main__":
    main()
