# pytest-typhoon-memtrack
A pytest plugin that tracks resource consumption during test session.

[![typhoon-hil](https://circleci.com/gh/typhoon-hil/pytest-typhoon-memtrack.svg?style=shield)](https://circleci.com/gh/typhoon-hil/pytest-typhoon-memtrack)

## Features

* specify which processes' resource consumption are tracked
* choose which module to use at runtime

## Requirements

* pytest 6+
* matplotlib 3+

## Installation

You can install `pytest-typhoon-memtrack` via `pip`:

```
pip install pytest-typhoon-memtrack
```

## Usage

In order to turn on the plugin that tracks resource consumption during test session, it is required to add ``` --memtrack ``` argument when running pytest test session. 

Example:
```python -m pytest --memtrack```

## Additional options

There are multiple additional arguments that can be added which allows selecting which processes and what types of data consumption are tracked.

* ```--export_format``` - Allows defining format of output file. Supported formats are: ```csv```, ```tsv``` and ```json```. Multiple formats can be specified separated by comma (e.x. ```--export_format=csv,json```). Default value is ```csv```.
* ```--tracked_processes``` - Allows defining names of tracked processes (separated by comma) whose resource consumptions' are tracked during test session (e.x. ```tracked_processes=python.exe,java,chrome```). Default value is None.
* ```--track_typhoon_processes``` - When defined, processes related to regular testing session with TyphoonTest and Typhoon HIL software are tracked and their resource consumption is recorded. By default, these processes are not tracked.
* ```--plot_types``` - Allows defining types of plots that are saved as images. Supported formats are: ```memory_percent```, ```memory_total``` and ```cpu_percent```. Multiple formats can be specified separated by comma (e.x. ```--plot_types=memory_total,cpu_percent```). Default value is ```memory_total```.
* ```--skip_plot``` - If defined, images containing plots are not generated. By default, plot is generated.
* ```--export_directory``` - Allows defining directory path where resource consumption tracking results are saved. By default, exported files are located in working directory of testing session.
* ```--gc_collect``` - If defined, garbage collection is called after each executed test (before resource consumption  of processes after test execution). By default, manual garbage collection after each test execution is not activated.

Example of a complex test run command with multiple arguments: ```--memtrack --export_format=csv,tsv,json --track_typhoon_processes --tracked_processes=python.exe,java,chrome --plot_types=memory_total,memory_percent,cpu_percent -k smoke_test```.

## Contributions

Contributions are very welcome. Feel free to contribute, open issues and send pull requests.

### Development

* In order to develop plugin and contribute, it is required to install ```dev-requirements.txt``` in virtual environment. 
* Tests can be run with ```tox```. Please ensure the coverage at least stays the same before you submit a pull request.
* Wheel can be generated by running either ```build_wheel.cmd``` or ```build_wheel.sh```.

## License

Distributed under the terms of the MIT license, `pytest-typhoon-memtrack` is
free and open source software.