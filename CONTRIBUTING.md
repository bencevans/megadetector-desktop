# Contributing

MegaDetector Desktop is written in Python and expects a recent version to be installed. The package management is managed by Conda which is also required to be installed.

Once the repository is cloned and entered as the current working directory, the env/dependencies can be installed.

    conda env update --file environment.yml

Afterwhich you're able to drop into a shell where these dependencies are avalable.

    conda activate md-desktop

The application can then be run.

    python app.py

There are currently no automated tests, each version should be tested manually.

### Building

The Application is packaged into a native executable, .exe on Windows and .app on MacOS. The following commands are expected to be run within a poetry shell with the current dependencies installed.

#### Windows

    pyinstaller win.spec

#### MacOS

The MacOS application built will be for the same architecture as the building system.

    pyinstaller macos.spec

#### Linux

    pyinstaller linux.spec