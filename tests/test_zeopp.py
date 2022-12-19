import shutil
import subprocess
from pathlib import Path
import os 
import pytest
from parsers import (
    AVolumeParser,
    ChannelParser,
    PoresSizeDistParser,
    ResParser,
    SurfaceAreaParser,
)

_CWD = Path(__file__).parent
_NETWORK_BINARY = os.path.join(_CWD, "../zeo++/network")


def test_xyz(tmpdir):
    # run network -xyz ZIF-67_opt.cif
    shutil.copy("ZIF-67_opt.cif", tmpdir)
    subprocess.run([_NETWORK_BINARY, "-xyz", "ZIF-67_opt.cif"], cwd=tmpdir)
    # check if ZIF-67_opt.xyz exists
    assert tmpdir.join("ZIF-67_opt.xyz").exists()

    # assert that the content matches the references "EDI_ref.chan"
    # for now, stick to the exact match
    with open(tmpdir.join("ZIF-67_opt.xyz"), "r") as f:
        content = f.read()
    with open("ZIF-67_opt_ref.xyz", "r") as f:
        ref_content = f.read()
    assert content == ref_content


def test_allow_adjust_coords_and_cell(tmpdir):
    # run network -ha -res -allowAdjustCoordsAndCell EDI.cssr
    shutil.copy("EDI.cssr", tmpdir)
    subprocess.run(
        [_NETWORK_BINARY, "-ha", "-res", "-allowAdjustCoordsAndCell", "EDI.cssr"],
        cwd=tmpdir,
    )
    # check if EDI.res exists
    assert tmpdir.join("EDI.res").exists()

    # parse the content of EDI.res
    with open(tmpdir.join("EDI.res"), "r") as f:
        res = ResParser.parse(f.read())

    # assert that the content matches the references "EDI_ref.chan"
    # for now, stick to the exact match
    with open("EDI_ref.res", "r") as f:
        res_ref = ResParser.parse(f.read())

    assert res == res_ref


def test_chan(tmpdir):
    # run network -ha -chan 1.5 EDI.cssr
    shutil.copy("EDI.cssr", tmpdir)
    subprocess.run([_NETWORK_BINARY, "-ha", "-chan", "1.5", "EDI.cssr"], cwd=tmpdir)
    # check if EDI.chan exists
    assert tmpdir.join("EDI.chan").exists()

    # parse the content of EDI.chan
    with open(tmpdir.join("EDI.chan"), "r") as f:
        chan = ChannelParser.parse(f.read())

    # assert that the content matches the references "EDI_ref.chan"
    # for now, stick to the exact match
    with open("EDI_ref.chan", "r") as f:
        chan_ref = ChannelParser.parse(f.read())

    assert chan == chan_ref


def test_sa(tmpdir):
    # run network -ha -sa 1.2 1.2 2000 EDI.cssr
    shutil.copy("EDI.cssr", tmpdir)
    subprocess.run(
        [_NETWORK_BINARY, "-ha", "-sa", "1.2", "1.2", "2000", "EDI.cssr"],
        cwd=tmpdir,
    )
    # check if EDI.sa exists
    assert tmpdir.join("EDI.sa").exists()

    # parse the content of EDI.sa
    with open(tmpdir.join("EDI.sa"), "r") as f:
        sa = SurfaceAreaParser.parse(f.read())

    # assert that the content matches the references "EDI_ref.chan"
    with open("EDI_ref.sa", "r") as f:
        sa_ref = SurfaceAreaParser.parse(f.read())

    for key in sa:
        assert sa[key] == pytest.approx(sa_ref[key], rel=0.06)


def test_vol(tmpdir):
    # run network -ha -vol 1.2 1.2 50000 EDI.cssr
    shutil.copy("EDI.cssr", tmpdir)
    subprocess.run(
        [_NETWORK_BINARY, "-ha", "-vol", "1.2", "1.2", "50000", "EDI.cssr"],
        cwd=tmpdir,
    )
    # check if EDI.vol exists
    assert tmpdir.join("EDI.vol").exists()

    # parse the content of EDI.vol
    with open(tmpdir.join("EDI.vol"), "r") as f:
        volpo = AVolumeParser.parse(f.read())

    # assert that the content matches the references "EDI_ref.vol
    with open("EDI_ref.vol", "r") as f:
        volpo_ref = AVolumeParser.parse(f.read())

    for key in volpo:
        assert volpo[key] == pytest.approx(volpo_ref[key], rel=0.06)


def test_psd(tmpdir):
    # run network -ha -psd 1.2 1.2 50000 EDI.cssr
    shutil.copy("EDI.cssr", tmpdir)
    subprocess.run(
        [_NETWORK_BINARY, "-ha", "-psd", "1.2", "1.2", "50000", "EDI.cssr"],
        cwd=tmpdir,
    )
    # check if EDI.psd exists
    assert tmpdir.join("EDI.psd_histo").exists()

    # parse the content of EDI.psd
    with open(tmpdir.join("EDI.psd_histo"), "r") as f:
        psd = PoresSizeDistParser.parse(f.read())

    # assert that the content matches the references "EDI_ref.psd
    with open("EDI_ref.psd_histo", "r") as f:
        psd_ref = PoresSizeDistParser.parse(f.read())

    for i, bin_val in enumerate(psd["psd"]["bins"]):
        assert bin_val == psd_ref["psd"]["bins"][i]

    for i, bin_count in enumerate(psd["psd"]["counts"]):
        assert bin_count == pytest.approx(psd_ref["psd"]["counts"][i], abs=1)
