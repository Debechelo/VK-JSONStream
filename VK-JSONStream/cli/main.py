import click
from generate_models import generate_models
from generate_controllers import generate_controllers


@click.group()
def cli():
    pass


cli.add_command(generate_models, name='gen-models')
cli.add_command(generate_controllers, name='gen-controllers')

if __name__ == "__main__":
    cli()
