"""Test fixtures."""

import os
import shutil
import tempfile

import pytest

import dtoolcore

_HERE = os.path.dirname(__file__)


@pytest.fixture
def chdir_fixture(request):
    d = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(d)

    @request.addfinalizer
    def teardown():
        os.chdir(curdir)
        shutil.rmtree(d)


@pytest.fixture
def tmp_dir_fixture(request):
    d = tempfile.mkdtemp()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)
    return d


@pytest.fixture
def local_tmp_dir_fixture(request):
    d = tempfile.mkdtemp(dir=_HERE)

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)
    return d


@pytest.fixture
def dataset_fixture(request):
    d = tempfile.mkdtemp()

    dest_path = os.path.join(d, "test")
    proto_dataset = dtoolcore.ProtoDataSet.create(
        uri=dest_path, name="test_dataset")

    for s in ["hello", "world"]:
        fname = s + ".txt"
        fpath = os.path.join(d,  fname)
        with open(fpath, "w") as fh:
            fh.write(s)
        proto_dataset.put_item(fpath, fname)

    proto_dataset.freeze()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)
    return dest_path
