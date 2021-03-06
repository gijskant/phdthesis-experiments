# Tools and examples used in the PhD thesis

This repository will contain scripts and example data used in the experiments
in my PhD thesis. Work in progress.

The [scripts directory](scripts) has scripts for installing required tools, scripts for generating
experiment input files and running the experiments.

Currently only the [Connect four](data/connectfour) example is available.


### Prerequisites

*   If your `cmake` is not recent, (`>=3.5.1`), you may want to install a local version
    using:
    ```bash
    ./scripts/install_cmake.sh
    ```

*   For several experiments, the [mCRL2](http://mcrl2.org) toolset is required.
    We support the official 201409.1 release and the experimental fork at
    [gijskant/mcrl2-pmc](https://github.com/gijskant/mcrl2-pmc).
    To install the experimental version, run:
    ```bash
    ./scripts/install-mcrl2.sh
    ```
    The script installs mCRL2 in your current working directory.
    Be patient, building mCRL2 can take a while. Perhaps it is a good idea to check out the
    binary releases of mCRL2: http://mcrl2.org/release/user_manual/download.html.

    You may need to execute `ldconfig` as root or run:
    ```
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:<prefix>/lib/mcrl2/
    ```

*   For installing [LTSmin](https://github.com/utwente-fmt/ltsmin),
    run the script:
    ```bash
    ./scripts/install_ltsmin.sh
    ```
    This installs LTSmin in your current working directory and expects mCRL2 to be installed
    there as well.

*   To install the Python dependencies, either run
    ```bash
    pip install -r scripts/requirements.txt
    ```
    or
    ```bash
    ./scripts/install_python_deps.sh
    ```

## License

Copyright &copy; 2017  Gijs Kant

All files are distributed under the MIT License (see accompanying file [LICENSE](LICENSE)).
