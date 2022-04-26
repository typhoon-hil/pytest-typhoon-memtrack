import os
import psutil

from .constants import PROCESS_NAME, PID, TEST_SESSION_PROCESS, SUPPORTED_DATA_FORMATS, SUPPORTED_PLOT_TYPES
from .exceptions import UnsupportedDataFormatException, UnsupportedPlotTypeException

tracked_processes = []


def load_tracked_processes(loaded_processes, load_typhoon_processes):
    global tracked_processes
    if load_typhoon_processes:
        tracked_processes = ["typhoon_hil", "virtual_hil_device"]
    if loaded_processes:
        additional_processes = loaded_processes.split(",")
        for process in additional_processes:
            tracked_processes.append(process.strip())


def processes_loaded():
    global tracked_processes
    return len(tracked_processes) > 0


def get_selected_processes():
    global tracked_processes
    processes = [{PID: process.pid, PROCESS_NAME: process.name()} for process in psutil.process_iter()
                 if any(tracked_process.lower() in process.name().lower() for tracked_process in tracked_processes)]
    processes.append({PID: os.getpid(), PROCESS_NAME: TEST_SESSION_PROCESS})
    return processes


def get_export_formats(formats):
    export_formats = []
    for token in formats.split(","):
        export_format = token.strip()
        if export_format not in SUPPORTED_DATA_FORMATS:
            raise UnsupportedDataFormatException(export_format)
        else:
            export_formats.append(export_format)
    return export_formats


def get_export_directory(config):
    export_directory = config.getoption("--export_directory")
    return export_directory if export_directory else ""


def get_plot_types(types):
    plot_types = []
    for token in types.split(","):
        plot_type = token.strip()
        if plot_type not in SUPPORTED_PLOT_TYPES:
            raise UnsupportedPlotTypeException(plot_type)
        else:
            plot_types.append(plot_type.strip())
    return plot_types
