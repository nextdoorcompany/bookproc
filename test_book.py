import os
import shutil
import zipfile
import pytest
import book

@pytest.fixture
def indir(request):
    os.mkdir('tmp')
    def fin():
        shutil.rmtree('tmp')
    request.addfinalizer(fin)
    return 'tmp'

def test_zip_frame(indir):
    open(os.path.join(indir, '1000.R0.F0 3HMF.pdf'), 'w')

    book.make_zip(indir)

    assert os.path.exists(os.path.join(indir, '1000.R0.F0.zip'))
    assert '1000.R0.F0 3HMF.pdf' in zipfile.ZipFile(os.path.join(indir, '1000.R0.F0.zip')).namelist()
    assert not os.path.exists(os.path.join(indir, '1000.R0.F0 3HMF.pdf'))

def test_zip_door(indir):
    open(os.path.join(indir, '1000.R0.D0 3HMD.pdf'), 'w')

    book.make_zip(indir)

    assert os.path.exists(os.path.join(indir, '1000.R0.D0.zip'))
    assert '1000.R0.D0 3HMD.pdf' in zipfile.ZipFile(os.path.join(indir, '1000.R0.D0.zip')).namelist()
    assert not os.path.exists(os.path.join(indir, '1000.R0.D0 3HMD.pdf'))
    