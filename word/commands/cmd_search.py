import click


class Context:
    def __init__(self, word_arg):
        pass


@click.group()
@click.option("-s", "--search", type=str, help="search word or sentence.")
@click.pass_context
def cli(ctx, word_arg):
    """Search word in elasticsearch"""


@cli.command()
@click.pass_context
def word(ctx):
    pass


@cli.command()
@click.pass_context
def sentence(ctx):
    pass

