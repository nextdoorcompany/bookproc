import click

@click.command()
@click.argument('indir', type=click.Path(exists=True, dir_okay=True, file_okay=False))
def cli(indir):
    click.echo('job done')

def make_zip(indir):
    pass

if __name__ == '__main__':
    cli()
