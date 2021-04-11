import click

from word.utils import CommandEnum, JsonParser
from word.utils import CommandFactory


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
        self.indices = ['word', 'doc', 'examples']
        self.factory = CommandFactory(self.host, self.port, self.indices)
        self.parser = JsonParser(self.indices)


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
    sample_dict = ctx.obj.parser.parse_to_dic(file_path=file_path)
    ctx.obj.factory.mapper(CommandEnum.POST).run(sample_dict=sample_dict)


@cli.command()
@click.pass_context
def delete(ctx):
    """Delete stored words in elasticsearch"""
    if click.confirm("Do you want to delete stored words?"):
        ctx.obj.factory.mapper(CommandEnum.DELETE).run()


@cli.command()
@click.argument("args", nargs=-1)
@click.option("-s", "--size", type=int, help="how many relevant words do you need?", default=2, show_default=True)
@click.option("-w", "--word", 'key', type=str, help="Do you want to search by word?",
              flag_value='word', default=True, show_default=True, cls=OnceSameNameOption)
@click.option("-e", "--examples", 'key', type=str, help="Do you want to search by example sentence?",
              flag_value='examples', cls=OnceSameNameOption)
@click.option("-d", "--doc", 'key', type=str, help="Do you want to search for dictionary?",
              flag_value='doc', cls=OnceSameNameOption)
@click.pass_context
def search(ctx, args, size, key):
    """Search word or example sentence in elasticsearch"""
    word = ' '.join(args)
    if len(word) != 0:
        ctx.obj.factory.mapper(CommandEnum.SEARCH).run(key, word, size)
    else:
        click.echo("Usage: word cli search [OPTIONS] ARGS")
        click.echo("Try 'word cli search --help' for help.")
        click.echo()
        click.echo("Error: Got unexpected argument (Empty argument)", err=True)
