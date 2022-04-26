import json
import os

from tytest.memtrack.constants import TEST, PROCESSES, MT, MP, CP


def test_memory_tracking_when_valid_arguments(testdir):
    test_example = """
    import pytest

    pytest_plugins = "pytester"

    def test_memory_tracking():
        numbers = range(100000)
        assert len(numbers) == 100000
    """

    testdir.makepyfile(__init__="")
    testdir.makepyfile(test_example)
    result = testdir.runpytest("--memtrack", "--tracked_processes=python", "--export_format=json")

    assert len(result.errlines) == 0
    assert os.path.isfile("resources.json")

    with open("resources.json", "r") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0][TEST] == "test_memory_tracking"
    assert len(data[0][PROCESSES]) > 0


def test_memory_tracking_when_multiple_export_formats(testdir):
    test_example = """
    import pytest

    pytest_plugins = "pytester"

    def test_memory_tracking():
        numbers = range(100000)
        assert len(numbers) == 100000
    """

    testdir.makepyfile(__init__="")
    testdir.makepyfile(test_example)
    result = testdir.runpytest("--memtrack", "--tracked_processes=python", "--export_format=csv,tsv,json")

    assert len(result.errlines) == 0

    assert os.path.isfile("resources.csv")
    with open("resources.csv") as f:
        lines = f.readlines()
    assert len(lines) > 1

    assert os.path.isfile("resources.tsv")
    with open("resources.tsv") as f:
        lines = f.readlines()
    assert len(lines) > 1

    assert os.path.isfile("resources.json")
    with open("resources.json", "r") as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0][TEST] == "test_memory_tracking"
    assert len(data[0][PROCESSES]) > 0


def test_memory_tracking_when_multiple_plot_types(testdir):
    test_example = """
    import pytest

    pytest_plugins = "pytester"

    def test_memory_tracking():
        numbers = range(100000)
        assert len(numbers) == 100000
    """

    testdir.makepyfile(__init__="")
    testdir.makepyfile(test_example)
    result = testdir.runpytest("--memtrack", "--tracked_processes=python",
                               "--plot_types=memory_percent,memory_total,cpu_percent")

    assert len(result.errlines) == 0

    assert os.path.isfile("resources.csv")
    with open("resources.csv") as f:
        lines = f.readlines()
    assert len(lines) > 1

    assert os.path.isfile("resources_{}.png".format(MT))
    assert os.path.isfile("resources_{}.png".format(MP))
    assert os.path.isfile("resources_{}.png".format(CP))


def test_memory_tracking_when_skip_plot(testdir):
    test_example = """
    import pytest

    pytest_plugins = "pytester"

    def test_memory_tracking():
        numbers = range(100000)
        assert len(numbers) == 100000
    """

    testdir.makepyfile(__init__="")
    testdir.makepyfile(test_example)
    result = testdir.runpytest("--memtrack", "--tracked_processes=python", "--skip_plot")

    assert len(result.errlines) == 0

    assert os.path.isfile("resources.csv")
    with open("resources.csv") as f:
        lines = f.readlines()
    assert len(lines) > 1

    assert not os.path.isfile("resources_{}.png".format(MT))
    assert not os.path.isfile("resources_{}.png".format(MP))
    assert not os.path.isfile("resources_{}.png".format(CP))
