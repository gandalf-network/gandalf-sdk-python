import click
import os
from subprocess import run
from .generate_queries import generate_queries

@click.group()
def cli():
    pass

@click.command()
@click.option(
    '--folder',
    default=".",
    help='The destination folder for the generated SDK.'
)
def generate(folder="."):
    base_path = os.path.dirname(os.path.abspath(__file__))
    remote_schema_url = "https://sauron.gandalf.network/public/gql"

    # Generate queries file
    formatted_query = generate_queries(remote_schema_url)
    print(base_path)
    queries_path = os.path.join(base_path, 'queries.graphql').replace("\\", "/")
    with open(queries_path, 'w') as file:
            file.write(formatted_query)

    config_content = f"""
    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"

    [project]
    name = "gandalf-eyeofsauron"
    description = "Generate fully typed GraphQL client from schema, queries and mutations!"
    version = "0.0.1"
    readme = "README.md"

    [tool.ariadne-codegen]
    remote_schema_url = "{remote_schema_url}"
    queries_path = "{queries_path}"
    target_package_path = "{folder}"
    target_package_name = "eyeofsauron"
    client_name = "Eye"
    plugins = [
        "eyeofsauron.custom_client_plugin.CustomClientPlugin",
    ]
    """

    config_path = os.path.join(base_path, 'pyproject.toml')
    os.makedirs(folder, exist_ok=True)
    
    with open(config_path, 'w') as config_file:
        config_file.write(config_content)

    """Generate SDK from GraphQL schema."""  
    run(['ariadne-codegen', '--config', config_path])

    click.echo(f"SDK generated at {folder}")

cli.add_command(generate)

if __name__ == '__main__':
    cli()
