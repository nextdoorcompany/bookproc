import os
import re
import zipfile
import click

@click.command()
@click.argument('indir', type=click.Path(exists=True, dir_okay=True, file_okay=False))
def cli(indir):
    result = make_zip(indir)
    if not result:
        click.secho('no zip file created', fg='red')
    else:    
        count = len(zipfile.ZipFile(result).namelist())
        click.secho('{} file(s) added to zip'.format(count), fg='green')

def make_zip(indir):
    old_dir = os.getcwd()
    os.chdir(indir)
    job = ''
    for file in os.listdir():
        result = (re.match(r'\d*\.R\d+\.[FD]\d+', file))
        if result:
            job = result.group()
            break

    if not job:
        os.chdir(old_dir)
        return None
    
    file_list = [f for f in os.listdir() if f.startswith(job)]
    if job + ' SPECIAL PARTS.pdf' in file_list:
        file_list.remove(job + ' SPECIAL PARTS.xls')
        os.remove(job + ' SPECIAL PARTS.xls')

    zip_name = job + '.zip'
    new_zip = zipfile.ZipFile(zip_name, 'w')
    for file in file_list:
        new_zip.write(file, compress_type=zipfile.ZIP_DEFLATED)
        os.remove(file)

    new_zip.close()
    os.chdir(old_dir)
    return os.path.join(indir, zip_name)

if __name__ == '__main__':
    cli()
