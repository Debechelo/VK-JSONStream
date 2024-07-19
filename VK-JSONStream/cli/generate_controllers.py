import os
import click


@click.command(name='gen-rest')
@click.option('-models', required=True, type=click.Path(exists=True), help='Directory with Pydantic models')
@click.option('-rest-routes', required=True, type=click.Path(), help='Directory to save generated REST code')
def generate_controllers(models, rest_routes):
    try:
        pass
    except FileNotFoundError:
        click.echo(f"Error: Directory {models} not found.")
    except Exception as e:
        click.echo(f"Error generating REST API code: {e}")


# if __name__ == "__main__":
#     generate_controllers()
