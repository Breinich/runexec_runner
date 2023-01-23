# Runexec Runner

This is a needed tool and a small environment for the extended and distributed version of the [Benchexec](https://github.com/sosy-lab/benchexec) software.

This tool is responsible for the execution on the target hardware of the different runs, with which the user would like to benchmark a software using the [modified Benchexec](https://github.com/Breinich/benchexec).

The tool has 2 command line arguments:
- The first one is the file (ending with *.command.csv*), where the commands are, which are wanted to be executed as single runs of the target software.
- The second one is a folder, where the tool should place the output files and the results of the run.

The tool's dependencies:
- [tqdm](https://pypi.org/project/tqdm/) is used to report the progress of the commands to the user.
- [Benchexec](https://pypi.org/project/BenchExec/) because this tool uses its RunExecutor submodule for executing the runs.
