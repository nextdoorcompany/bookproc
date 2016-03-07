import os
import zipfile
import click

@click.command()
@click.argument('indir', type=click.Path(exists=True, dir_okay=True, file_okay=False))
def cli(indir):
    click.echo('job done')

def make_zip(indir):
    #need to change directories here
    zip_name = '1000.R0.F0.zip'
    new_zip = zipfile.ZipFile(os.path.join(indir, zip_name), 'w')
    for file in os.listdir(indir):
        if file != zip_name:
            full_file = os.path.join(indir, file)
            new_zip.write(full_file, compress_type=zipfile.ZIP_DEFLATED)
            os.remove(full_file)
    new_zip.close()

if __name__ == '__main__':
    cli()
