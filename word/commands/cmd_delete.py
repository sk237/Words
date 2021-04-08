import click


class Context:
    def __init__(self):
        pass


@click.group()
@click.option("-d", "--delete", type=str, help="Delete saved words.")
@click.pass_context
def cli(ctx):
    """Delete saved word in elasticsearch"""


@cli.command()
@click.pass_context
def delete(ctx):
    pass
