import click

from word.model.service_enum import Command
from word.service.service_factory import ServiceFactory


class OnceSameNameOption(click.Option):

    def add_to_parser(self, parser, ctx):

        def parser_process(value, state):
            # method to hook to the parser.process
            if self.name in state.opts:
                param_same_name = [
                    opt.opts[0] for opt in ctx.command.params
                    if isinstance(opt, OnceSameNameOption) and opt.name == self.name
                ]

                raise click.UsageError(
                    "Illegal usage: `{}` are mutually exclusive arguments.".format(
                        ', '.join(param_same_name))
                )

            # call the actual process
            self._previous_parser_process(value, state)

        retval = super(OnceSameNameOption, self).add_to_parser(parser, ctx)
        for name in self.opts:
            our_parser = parser._long_opt.get(name) or parser._short_opt.get(name)
            if our_parser:
                self._previous_parser_process = our_parser.process
                our_parser.process = parser_process
                break
        return retval


class Context:
    def __init__(self):
        self.host = '[localhost]:'
        self.port = '9200'
        self.index = 'samples'
        self.factory = ServiceFactory(self.host, self.port, self.index)


@click.group()
@click.pass_context
def cli(ctx):
    """Search Engine Command Line Interface"""
    ctx.obj = Context()


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.pass_context
def post(ctx, file_path):
    """Save sample words to elasticsearch"""
    ctx.obj.factory.mapper(Command.POST).run(file_path=file_path)


@cli.command()
@click.pass_context
def delete(ctx):
    """Delete stored words in elasticsearch"""
    if click.confirm("Do you want to delete stored words?"):
        ctx.obj.factory.mapper(Command.DELETE).run()


@cli.command()
@click.argument("args", nargs=-1)
@click.option("-n", "--num", type=int, help="how many relevant words do you need?", default=2, show_default=True)
@click.option("-w", "--word", "key", type=str, help="Do you want to search by word?",
              flag_value='key', default=True, show_default=True, cls=OnceSameNameOption)
@click.option("-s", "--sentence", "key", type=str, help="Do you want to search by example sentence?",
              flag_value='examples', cls=OnceSameNameOption)
@click.pass_context
def search(ctx, args, num, key):
    """Search word or example sentence in elasticsearch"""
    word = ' '.join(args)
    if len(word) != 0:
        ctx.obj.factory.mapper(Command.SEARCH).run(key, word, num)
    else:
        click.echo("Usage: word cli search [OPTIONS] ARGS")
        click.echo("Try 'word cli search --help' for help.")
        click.echo()
        click.echo("Error: Got unexpected argument (Empty argument)", err=True)
