import os.path as osp
import shutil
import tempfile

import pytest

import labelme.app
import labelme.config
import labelme.testing


here = osp.dirname(osp.abspath(__file__))
data_dir = osp.join(here, "data")


@pytest.mark.parametrize(
    "maximum",
    [
        (0,),
        (1000,),
        (2400,),
        (3200,),
    ],
)
def test_fov_offset_fixed_6x6(maximum):
    offsets = [
        labelme.app._fov_offset_with_overlap(
            maximum=maximum,
            index=i,
            tiles_per_axis=6,
        )
        for i in range(6)
    ]

    assert offsets[0] == 0
    assert offsets[-1] == max(0, int(maximum))
    assert all(offsets[i] <= offsets[i + 1] for i in range(5))
    if maximum > 0:
        expected_step = maximum / 5.0
        assert abs((offsets[1] - offsets[0]) - expected_step) <= 1


@pytest.mark.parametrize("maximum", [1000, 2400, 3200])
def test_fov_axis_step_is_positive(maximum):
    steps = [
        labelme.app._fov_axis_step(maximum=maximum, index=i, tiles_per_axis=6)
        for i in range(6)
    ]
    assert all(step >= 1 for step in steps)
def _win_show_and_wait_imageData(qtbot, win):
    win.show()

    def check_imageData():
        assert hasattr(win, "imageData")
        assert win.imageData is not None

    qtbot.waitUntil(check_imageData)  # wait for loadFile


@pytest.mark.gui
def test_MainWindow_open(qtbot):
    win = labelme.app.MainWindow()
    qtbot.addWidget(win)
    win.show()
    win.close()


@pytest.mark.gui
def test_MainWindow_open_img(qtbot):
    img_file = osp.join(data_dir, "raw/2011_000003.jpg")
    win = labelme.app.MainWindow(filename=img_file)
    qtbot.addWidget(win)
    _win_show_and_wait_imageData(qtbot, win)
    win.close()


@pytest.mark.gui
def test_MainWindow_open_json(qtbot):
    json_files = [
        osp.join(data_dir, "annotated_with_data/apc2016_obj3.json"),
        osp.join(data_dir, "annotated/2011_000003.json"),
    ]
    for json_file in json_files:
        labelme.testing.assert_labelfile_sanity(json_file)

        win = labelme.app.MainWindow(filename=json_file)
        qtbot.addWidget(win)
        _win_show_and_wait_imageData(qtbot, win)
        win.close()


@pytest.mark.gui
def test_MainWindow_open_dir(qtbot):
    directory = osp.join(data_dir, "raw")
    win = labelme.app.MainWindow(filename=directory)
    qtbot.addWidget(win)
    _win_show_and_wait_imageData(qtbot, win)
    return win


@pytest.mark.gui
def test_MainWindow_openNextImg(qtbot):
    win = test_MainWindow_open_dir(qtbot)
    win.openNextImg()


@pytest.mark.gui
def test_MainWindow_openPrevImg(qtbot):
    win = test_MainWindow_open_dir(qtbot)
    win.openNextImg()


@pytest.mark.gui
def test_MainWindow_annotate_jpg(qtbot):
    tmp_dir = tempfile.mkdtemp()
    input_file = osp.join(data_dir, "raw/2011_000003.jpg")
    out_file = osp.join(tmp_dir, "2011_000003.json")

    config = labelme.config.get_default_config()
    win = labelme.app.MainWindow(
        config=config, filename=input_file, output_file=out_file,
    )
    qtbot.addWidget(win)
    _win_show_and_wait_imageData(qtbot, win)

    label = "whole"
    points = [
        (100, 100),
        (100, 238),
        (400, 238),
        (400, 100),
    ]
    shapes = [
        dict(
            label=label,
            group_id=None,
            points=points,
            shape_type="polygon",
            flags={},
            other_data={},
        )
    ]
    win.loadLabels(shapes)
    win.saveFile()

    labelme.testing.assert_labelfile_sanity(out_file)
    shutil.rmtree(tmp_dir)
