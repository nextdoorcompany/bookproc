import os
import re
import zipfile
import click

@click.command()
@click.argument('indir', type=click.Path(exists=True, dir_okay=True, file_okay=False))
def cli(indir):
    click.echo('job done')

def make_zip(indir):
    old_dir = os.getcwd()
    os.chdir(indir)
    job = ''
    for file in os.listdir():
        result = (re.match(r'\d*\.R\d+\.[FD]\d+', file))
        if result:
            job = result.group()
            break

    #what if there is no match?
    file_list = [f for f in os.listdir() if job in f]

    zip_name = job + '.zip'
    new_zip = zipfile.ZipFile(zip_name, 'w')
    for file in file_list:
        new_zip.write(file, compress_type=zipfile.ZIP_DEFLATED)
        os.remove(file)

    new_zip.close()
    os.chdir(old_dir)

if __name__ == '__main__':
    cli()
