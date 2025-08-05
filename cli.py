import click
from commands import sonarr

@click.group()
def cli():
    """Homelab Infrastructure CLI"""
    pass

cli.add_command(sonarr.sonarr)

if __name__ == "__main__":
    cli()
