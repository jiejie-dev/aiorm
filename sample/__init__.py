import click


@click.group()
def cli():
    pass


@cli.command()
def norm():
    from . import norm_bench
    norm_bench.main()


@cli.command()
def peewee():
    pass


def main():
    cli()
