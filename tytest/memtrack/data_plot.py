import os

import matplotlib.pyplot as plt
from collections import OrderedDict

from .constants import PROCESSES, STARTED_AT, FINISHED_AT, PROCESS_NAME, MT, MP, CP, BEFORE_MEMORY_TOTAL, \
    AFTER_MEMORY_TOTAL, BEFORE_MEMORY_PERCENT, AFTER_MEMORY_PERCENT, BEFORE_CPU, AFTER_CPU, MEMORY_TOTAL_LABEL, \
    MEMORY_PERCENT_LABEL, CPU_LABEL, MEMORY_TOTAL_TITLE, MEMORY_PERCENT_TITLE, CPU_TITLE
from .exceptions import UnsupportedPlotTypeException


def generate_plot_image(export_directory, data, plot_types):
    process_labels = [[(pid, process_info[PROCESS_NAME]) for pid, process_info in test[PROCESSES].items()]
                      for test in data.values()]
    process_labels = list(set([process for item in process_labels for process in item]))

    time_x_axis = []
    plots_data = {}
    for plot_type in plot_types:
        plots_data[plot_type] = OrderedDict.fromkeys(process_labels)
        for label in process_labels:
            plots_data[plot_type][label] = [0.0 for _ in range(len(data) * 2)]

    for index, test in enumerate(data.values()):
        time_x_axis.append(test[STARTED_AT])
        time_x_axis.append(test[FINISHED_AT])

        for plot_type in plot_types:
            for pid, process_info in test[PROCESSES].items():
                time_point_data = plots_data[plot_type][(pid, process_info[PROCESS_NAME])]

                if plot_type == MT:
                    time_point_data[index * 2] = process_info[BEFORE_MEMORY_TOTAL]
                    time_point_data[index * 2 + 1] = process_info[AFTER_MEMORY_TOTAL]
                elif plot_type == MP:
                    time_point_data[index * 2] = process_info[BEFORE_MEMORY_PERCENT]
                    time_point_data[index * 2 + 1] = process_info[AFTER_MEMORY_PERCENT]
                elif plot_type == CP:
                    time_point_data[index * 2] = process_info[BEFORE_CPU]
                    time_point_data[index * 2 + 1] = process_info[AFTER_CPU]
                else:
                    raise UnsupportedPlotTypeException(plot_type)

    for index, plot_type in enumerate(plots_data.keys()):
        plt.figure(index)
        plt.set_loglevel('WARNING')
        plt.xlabel("Timestamp")
        plt.xticks(rotation=80)

        if plot_type == MT:
            plt.ylabel(MEMORY_TOTAL_LABEL)
            plt.title(MEMORY_TOTAL_TITLE)
        elif plot_type == MP:
            plt.ylabel(MEMORY_PERCENT_LABEL)
            plt.title(MEMORY_PERCENT_TITLE)
        elif plot_type == CP:
            plt.ylabel(CPU_LABEL)
            plt.title(CPU_TITLE)
        else:
            raise UnsupportedPlotTypeException(plot_type)

        for process, y_axis_data in plots_data[plot_type].items():
            plt.plot(time_x_axis, y_axis_data, label="{} ({})".format(process[1], process[0]), alpha=0.4, linewidth=4)

        plt.legend()
        file_path = os.path.join(export_directory, "resources_{}.png".format(plot_type))
        plt.savefig(file_path, bbox_inches="tight")
        print("Resource consumption plot exported to resources_{}.png".format(plot_type))
