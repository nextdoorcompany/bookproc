import os
import shutil
import zipfile
import glob
import pytest
import book

from click.testing import CliRunner

@pytest.fixture
def indir(request):
    os.mkdir('tmp')
    def fin():
        shutil.rmtree('tmp')
    request.addfinalizer(fin)
    return 'tmp'

def test_zip_frame(indir):
    open(os.path.join(indir, '1000.R0.F0 3HMF.pdf'), 'w')

    result = book.make_zip(indir)

    assert os.path.exists(os.path.join(indir, '1000.R0.F0.zip'))
    assert '1000.R0.F0 3HMF.pdf' in zipfile.ZipFile(os.path.join(indir, '1000.R0.F0.zip')).namelist()
    assert not os.path.exists(os.path.join(indir, '1000.R0.F0 3HMF.pdf'))
    assert result == os.path.join(indir, '1000.R0.F0.zip')

def test_zip_door(indir):
    open(os.path.join(indir, '1000.R0.D0 3HMD.pdf'), 'w')

    result = book.make_zip(indir)

    assert os.path.exists(os.path.join(indir, '1000.R0.D0.zip'))
    assert '1000.R0.D0 3HMD.pdf' in zipfile.ZipFile(os.path.join(indir, '1000.R0.D0.zip')).namelist()
    assert not os.path.exists(os.path.join(indir, '1000.R0.D0 3HMD.pdf'))
    assert result == os.path.join(indir, '1000.R0.D0.zip')

def test_zip_frame_multiple_files(indir):
    open(os.path.join(indir, '1000.R0.F0 3HMF.pdf'), 'w')
    open(os.path.join(indir, '1000.R0.F0 STANDARD PARTS.pdf'), 'w')
    open(os.path.join(indir, '1000.R0.F0 PRECUT.xls'), 'w')

    result = book.make_zip(indir)

    assert os.path.exists(os.path.join(indir, '1000.R0.F0.zip'))
    assert '1000.R0.F0 3HMF.pdf' in zipfile.ZipFile(os.path.join(indir, '1000.R0.F0.zip')).namelist()
    assert '1000.R0.F0 STANDARD PARTS.pdf' in zipfile.ZipFile(os.path.join(indir, '1000.R0.F0.zip')).namelist()
    assert '1000.R0.F0 PRECUT.xls' in zipfile.ZipFile(os.path.join(indir, '1000.R0.F0.zip')).namelist()
    assert not os.path.exists(os.path.join(indir, '1000.R0.F0 3HMF.pdf'))
    assert not os.path.exists(os.path.join(indir, '1000.R0.F0 STANDARD PARTS.pdf'))
    assert not os.path.exists(os.path.join(indir, '1000.R0.F0 PRECUT.xls'))
    assert result == os.path.join(indir, '1000.R0.F0.zip')

def test_zip_frame_excludes_non_job_files(indir):
    open(os.path.join(indir, '1000.R0.F0 3HMF.pdf'), 'w')
    open(os.path.join(indir, 'something else.pdf'), 'w')

    result = book.make_zip(indir)

    assert os.path.exists(os.path.join(indir, '1000.R0.F0.zip'))
    assert os.path.exists(os.path.join(indir, 'something else.pdf'))
    assert '1000.R0.F0 3HMF.pdf' in zipfile.ZipFile(os.path.join(indir, '1000.R0.F0.zip')).namelist()
    assert not os.path.exists(os.path.join(indir, '1000.R0.F0 3HMF.pdf'))
    assert result == os.path.join(indir, '1000.R0.F0.zip')

def test_zip_frame_special_parts_no_pdf(indir):
    open(os.path.join(indir, '1000.R0.F0 3HMF.pdf'), 'w')
    open(os.path.join(indir, '1000.R0.F0 SPECIAL PARTS.xls'), 'w')

    result = book.make_zip(indir)

    assert os.path.exists(os.path.join(indir, '1000.R0.F0.zip'))
    assert '1000.R0.F0 3HMF.pdf' in zipfile.ZipFile(os.path.join(indir, '1000.R0.F0.zip')).namelist()
    assert '1000.R0.F0 SPECIAL PARTS.xls' in zipfile.ZipFile(os.path.join(indir, '1000.R0.F0.zip')).namelist()
    assert not os.path.exists(os.path.join(indir, '1000.R0.F0 3HMF.pdf'))
    assert not os.path.exists(os.path.join(indir, '1000.R0.F0 SPECIAL PARTS.xls'))
    assert result == os.path.join(indir, '1000.R0.F0.zip')

def test_zip_frame_special_parts_yes_pdf(indir):
    open(os.path.join(indir, '1000.R0.F0 3HMF.pdf'), 'w')
    open(os.path.join(indir, '1000.R0.F0 SPECIAL PARTS.xls'), 'w')
    open(os.path.join(indir, '1000.R0.F0 SPECIAL PARTS.pdf'), 'w')

    result = book.make_zip(indir)

    assert os.path.exists(os.path.join(indir, '1000.R0.F0.zip'))
    assert '1000.R0.F0 3HMF.pdf' in zipfile.ZipFile(os.path.join(indir, '1000.R0.F0.zip')).namelist()
    assert '1000.R0.F0 SPECIAL PARTS.xls' not in zipfile.ZipFile(os.path.join(indir, '1000.R0.F0.zip')).namelist()
    assert '1000.R0.F0 SPECIAL PARTS.pdf' in zipfile.ZipFile(os.path.join(indir, '1000.R0.F0.zip')).namelist()
    assert not os.path.exists(os.path.join(indir, '1000.R0.F0 3HMF.pdf'))
    assert not os.path.exists(os.path.join(indir, '1000.R0.F0 SPECIAL PARTS.xls'))
    assert not os.path.exists(os.path.join(indir, '1000.R0.F0 SPECIAL PARTS.pdf'))
    assert result == os.path.join(indir, '1000.R0.F0.zip')

def test_zip_no_files(indir):
    result = book.make_zip(indir)

    assert not glob.glob(os.path.join(indir, '*.zip'))
    assert not result

def test_zip_frame_more_digits(indir):
    open(os.path.join(indir, '55555.R127.F0 3HMF.pdf'), 'w')

    result = book.make_zip(indir)

    assert os.path.exists(os.path.join(indir, '55555.R127.F0.zip'))
    assert '55555.R127.F0 3HMF.pdf' in zipfile.ZipFile(os.path.join(indir, '55555.R127.F0.zip')).namelist()
    assert not os.path.exists(os.path.join(indir, '55555.R127.F0 3HMF.pdf'))
    assert result == os.path.join(indir, '55555.R127.F0.zip')

def test_cli():
    runner = CliRunner()
    with runner.isolated_filesystem():
        open('1000.R0.F0 3HMF.pdf', 'w')
        result = runner.invoke(book.cli, '.')
        assert os.path.exists('1000.R0.F0.zip')

    assert result.output == '1 file(s) added to zip\n'
    
def test_cli_no_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(book.cli, '.')

    assert result.output == 'no zip file created\n'

    