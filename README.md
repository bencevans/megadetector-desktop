# MegaDetector Desktop

MegaDetector Desktop makes MegaDetector accessable to all. No knowledge of Python, Machine Learning, Command Line etc. nessacary. Just download the software, run, choose your folder and the MegaDetector shall begin processing.

## Install

MegaDetector Desktop is currently available for Windows and MacOS. Latest versions can be found on the releases page.

## Development

MegaDetector Desktop is written in Python and expects a recent version to be installed. The package management is managed by Poetry which is also required to be installed.

Once the repository is cloned and entered as the current working directory, the dependencies can be installed.

    poetry install

Afterwhich you're able to drop into a shell where these dependencies are avalable.

    poetry shell

The application can then be run.

    python app.py

There are currently no automated tests, each version should be tested manually.

### Building

The Application is packaged into a native executable, .exe on Windows and .app on MacOS. The following commands are expected to be run within a poetry shell with the current dependencies installed.

#### Windows

    # TODO

#### MacOS

    poetry run pyinstaller macos.spec

#### Linux

    # TODO
