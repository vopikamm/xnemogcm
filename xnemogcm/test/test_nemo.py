import pytest
from xnemogcm import open_domain_cfg, open_nemo, process_nemo
from xnemogcm.nemo import nemo_preprocess
from xnemogcm.arakawa_points import ALL_POINTS
import os
from pathlib import Path
import xarray as xr

TEST_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


@pytest.mark.parametrize("parallel", [True, False])
@pytest.mark.parametrize("option", [0, 1, 2, 3])
def test_options_for_files(parallel, option):
    """Test options to provide files"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
    )
    datadir = TEST_PATH / "data/nemo"
    if option == 0:
        # 0. Provide datadir and no files
        open_nemo(datadir=datadir, files=None, domcfg=domcfg, parallel=parallel)
        open_nemo(datadir=datadir, files="", domcfg=domcfg, parallel=parallel)
        open_nemo(datadir=datadir, files=[], domcfg=domcfg, parallel=parallel)
    elif option == 1:
        # 1. Provide datadir and files
        files = ["BASIN_grid_T.nc", "BASIN_grid_U.nc"]
        open_nemo(datadir=datadir, files=files, domcfg=domcfg, parallel=parallel)
    elif option == 2:
        # 2. Don't provide datadir but files
        open_nemo(
            datadir=None,
            files=datadir.glob("*grid*.nc"),
            domcfg=domcfg,
            parallel=parallel,
        )
        open_nemo(
            datadir="",
            files=datadir.glob("*grid*.nc"),
            domcfg=domcfg,
            parallel=parallel,
        )
        open_nemo(
            datadir=[],
            files=datadir.glob("*grid*.nc"),
            domcfg=domcfg,
            parallel=parallel,
        )
    elif option == 3:
        # 3. Don't provide anything => error
        try:
            open_nemo(datadir=None, files=None, domcfg=domcfg, parallel=parallel)
        except FileNotFoundError:
            pass


def test_no_file_provided_or_wrong_name():
    """Test exception raised if no file is found"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
    )
    try:
        open_nemo(datadir=TEST_PATH, domcfg=domcfg)
    except FileNotFoundError:
        pass
    try:
        open_nemo(
            files=(TEST_PATH / "data/domcfg_1_file").glob("domain*"), domcfg=domcfg
        )
    except ValueError:
        pass


def test_open_nemo():
    """Test opening of nemo files"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
    )
    nemo_ds = open_nemo(
        datadir=TEST_PATH / "data/nemo",
        domcfg=domcfg,
    )


def test_open_nemo_no_grid_in_filename():
    """Test opening of nemo files"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
    )
    nemo_ds = open_nemo(
        datadir=TEST_PATH / "data/nemo",
        domcfg=domcfg,
    )
    nemo_ds2 = open_nemo(
        files=(TEST_PATH / "data/nemo_no_grid_in_filename").glob("*.nc"),
        domcfg=domcfg,
    )
    xr.testing.assert_identical(nemo_ds, nemo_ds2)


def test_process_nemo():
    """Test processing of nemo files"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
    )
    nemo_ds = open_nemo(
        datadir=TEST_PATH / "data/nemo",
        domcfg=domcfg,
    )
    positions = [
        (xr.open_dataset(TEST_PATH / f"data/nemo_no_grid_in_filename/BASIN_{i}.nc"), i)
        for i in ["T", "U", "V", "W"]
    ]
    nemo_ds2 = process_nemo(
        positions=positions,
        domcfg=domcfg,
    )
    xr.testing.assert_identical(nemo_ds, nemo_ds2)


def test_process_nemo_from_desc():
    """Test processing of nemo files"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
    )
    nemo_ds = open_nemo(
        datadir=TEST_PATH / "data/nemo",
        domcfg=domcfg,
    )
    positions = [
        (
            xr.open_dataset(TEST_PATH / f"data/nemo_no_grid_in_filename/BASIN_{i}.nc"),
            None,
        )
        for i in ["T", "U", "V", "W"]
    ]
    nemo_ds2 = process_nemo(
        positions=positions,
        domcfg=domcfg,
    )
    xr.testing.assert_identical(nemo_ds, nemo_ds2)


def test_use_preprocess():
    """Test opening of one nemo file and preprocess it by hand"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
    )
    ds_raw = xr.open_dataset(TEST_PATH / "data/nemo/BASIN_grid_T.nc")
    ds_raw.encoding["source"] = "BASIN_grid_T.nc"
    ds = nemo_preprocess(ds_raw, domcfg)
    assert "x_c" in ds
    assert "t" in ds
