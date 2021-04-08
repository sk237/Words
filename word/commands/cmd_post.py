import click


class Context:
    def __init__(self, file_path):
        pass


@click.group()
@click.option("-p", "--post", type=str, help="Post sample words file.")
@click.pass_context
def cli(ctx, file_path):
    """Save sample words in elasticsearch"""


@cli.command()
@click.pass_context
def post(ctx):
    result = ctx.obj.weather.current(location=ctx.obj.location)
