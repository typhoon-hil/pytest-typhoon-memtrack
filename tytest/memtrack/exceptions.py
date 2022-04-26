from .constants import SUPPORTED_DATA_FORMATS, SUPPORTED_PLOT_TYPES


class ProcessesNotLoadedException(Exception):
    """Exception raised when no processes are chosen for tracking."""

    def __init__(self):
        self.message = "No processes are chosen for resource consumption tracking. Please define names of resources " \
                       "that are tracked using --tracked_processes argument. "
        super().__init__(self.message)


class UnsupportedDataFormatException(Exception):
    """Exception raised when chosen unsupported format for data export."""

    def __init__(self, data_format):
        self.message = "Unsupported data format '{}' is chosen. Supported formats for exporting resource consumption" \
                       " data are: {}.".format(data_format, str(SUPPORTED_DATA_FORMATS))
        super().__init__(self.message)


class UnsupportedPlotTypeException(Exception):
    """Exception raised when chosen unsupported plot type."""

    def __init__(self, data_format):
        self.message = "Unsupported plot type '{}' is chosen. Supported plot types that can be exported as images " \
                       "are: {}.".format(data_format, str(SUPPORTED_PLOT_TYPES))
        super().__init__(self.message)
