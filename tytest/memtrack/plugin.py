from collections import OrderedDict
from datetime import datetime

import pytest

from .constants import DATE_FORMAT, PROCESSES, PID, PROCESS_NAME, STARTED_AT, FINISHED_AT, BEFORE_CPU, \
    BEFORE_MEMORY_TOTAL, BEFORE_MEMORY_PERCENT, AFTER_CPU, AFTER_MEMORY_TOTAL, AFTER_MEMORY_PERCENT

from .data_export import export_consumption_data, prepare_consumption_data_for_export
from .data_plot import generate_plot_image
from .consumption import get_memory_consumption, get_cpu_percent
from .config import get_selected_processes, get_export_formats, get_export_directory, get_plot_types, \
    load_tracked_processes, processes_loaded
from .exceptions import ProcessesNotLoadedException


def pytest_addoption(parser):
    parser.addoption("--memtrack", action="store_true", default=False,
                     help="Turns on tracking resource consumption. This option is mandatory in order to activate the "
                          "plugin. By default the plugin is deactivated.")
    parser.addoption("--export_format", action="store", default="csv",
                     help="Allows defining format of output file. Supported formats are: csv, tsv and json. Multiple "
                          "formats can be specified separated by comma (e.x. --export_format=csv,json). "
                          "Default value is 'csv'.")
    parser.addoption("--tracked_processes", action="store", default=None,
                     help="Allows defining names of tracked processes (separated by comma) whose resource "
                          "consumptions' are tracked during test session (e.x. python.exe,java,chrome). "
                          "Default value is None.")
    parser.addoption("--track_typhoon_processes", action="store_true", default=False,
                     help="When defined, processes related to regular testing session with TyphoonTest and Typhoon HIL"
                          " software are tracked and their resource consumption is recorded. By default, these "
                          "processes are not tracked.")
    parser.addoption("--plot_types", action="store", default="memory_total",
                     help="Allows defining types of plots that are saved as images. Supported formats are: "
                          "memory_percent, memory_total and cpu_percent. Multiple formats can be specified separated "
                          "by comma (e.x. --plot_types=memory_total,cpu_percent). Default value is 'memory_total'.")
    parser.addoption("--skip_plot", action="store_true", default=False,
                     help="If defined, images containing plots are not generated. By default, plot is generated.")
    parser.addoption("--export_directory", action="store", default=None,
                     help="Allows defining directory path where resource consumption tracking results are saved. "
                          "By default, exported files are located in working directory of testing session.")
    parser.addoption("--gc_collect", action="store_true", default=False,
                     help="If defined, garbage collection is called after each executed test (before resource "
                          "consumption  of processes after test execution). By default, manual garbage collection "
                          "after each test execution is not activated.")


def pytest_configure(config):
    config.consumption_summary = OrderedDict()
    if config.getoption("--memtrack"):
        load_tracked_processes(config.getoption("--tracked_processes"), config.getoption("--track_typhoon_processes"))
        if not processes_loaded():
            raise ProcessesNotLoadedException


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_setup(item):
    if item.config.getoption("--memtrack"):
        item.config.consumption_summary[item.name] = {PROCESSES: OrderedDict()}
        test = item.config.consumption_summary[item.name]
        for process in get_selected_processes():
            test[PROCESSES][process[PID]] = OrderedDict({PROCESS_NAME: process[PROCESS_NAME]})

            test[PROCESSES][process[PID]][BEFORE_CPU] = get_cpu_percent(process[PID])
            test[PROCESSES][process[PID]][BEFORE_MEMORY_TOTAL], test[PROCESSES][process[PID]][BEFORE_MEMORY_PERCENT] \
                = get_memory_consumption(process[PID])
    yield


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_teardown(item):
    if item.config.getoption("--memtrack"):
        if item.config.getoption("--gc_collect"):
            import gc
            gc.collect()

        test = item.config.consumption_summary[item.name]
        for process in get_selected_processes():
            if process[PID] not in test[PROCESSES]:
                test[PROCESSES][process[PID]] = {PROCESS_NAME: process[PROCESS_NAME]}

            test[PROCESSES][process[PID]][AFTER_CPU] = get_cpu_percent(process[PID])
            test[PROCESSES][process[PID]][AFTER_MEMORY_TOTAL], test[PROCESSES][process[PID]][AFTER_MEMORY_PERCENT] \
                = get_memory_consumption(process[PID])
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    if item.name in item.config.consumption_summary:
        test = item.config.consumption_summary[item.name]
        test_start = datetime.fromtimestamp(call.start)
        test_stop = datetime.fromtimestamp(call.stop)
        test[STARTED_AT] = datetime.strftime(test_start, DATE_FORMAT)
        test[FINISHED_AT] = datetime.strftime(test_stop, DATE_FORMAT)
    yield


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_sessionfinish(session):
    if session.config.getoption("--memtrack"):
        print("Generating resource consumption report...")
        export_directory = get_export_directory(session.config)
        export_format = session.config.getoption("--export_format")

        prepare_consumption_data_for_export(session.config.consumption_summary)
        export_consumption_data(export_directory, session.config.consumption_summary,
                                get_export_formats(export_format))
        if not session.config.getoption("--skip_plot"):
            plot_types = session.config.getoption("--plot_types")
            generate_plot_image(export_directory, session.config.consumption_summary, get_plot_types(plot_types))
    yield
