import json

import click


class Context:
    def __init__(self):
        pass


@click.group()
@click.pass_context
def cli(ctx):
    """Save sample words in elasticsearch"""
    ctx.obj = Context()


@cli.command()
@click.argument("path", type=str)
@click.pass_context
def post(ctx, path):
    with open(path) as f:
        data = json.load(f)
    click.echo(data['60'])


@cli.command()
@click.option("-d", "--delete", type=str, help="Delete saved words.")
@click.pass_context
def delete(ctx):
    pass


@cli.command()
@click.option("-s", "--search", type=str, help="search word or sentence.")
@click.pass_context
def search(ctx):
    """Search word in elasticsearch"""

