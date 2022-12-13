import csv
import os.path
import re
import sys
import math
from typing import Optional, cast

from tqdm import tqdm
from benchexec import util
from benchexec.runexecutor import RunExecutor


def main(argv):
    # checking input folder format
    if not re.compile('.*\.csv').match(argv[1]):
        sys.exit("Bad command.csv input!")

    # checking output folder format
    if len(argv) > 2:
        parent_folder = argv[2]
        if not os.path.exists(parent_folder):
            if parent_folder[-1] != '/':
                parent_folder += '/'
    else:
        parent_folder = ""

    with open(argv[1]) as input_csv:
        tot = len(input_csv.readlines())

    # Reading the runs from the *.csv, that is given as a program argument
    with open(argv[1]) as input_csv:
        input_reader = csv.reader(input_csv, delimiter=';')

        for row in tqdm(input_reader, "Reading and executing commands", total=tot, unit="run"):
            # printOut("^", end="")

            # The run scenario's parameters
            args2 = row[0][1:-1].split(', ')
            i = 0
            for a in args2:
                a = a[1:-1]
                args2[i] = a
                i = i + 1

            out_fn = parent_folder + row[1]

            out_dir = parent_folder + row[2]

            res_fp = row[3]

            hardtl = None
            if row[4].isnumeric():
                hardtl = int(row[4])

            softtl = None
            if row[5].isdigit():
                softtl = int(row[5])

            walltl = None
            if row[6].isnumeric():
                walltl = int(row[6])

            cores = None
            if row[7] != '':
                tmp0 = row[7][1:-1]
                tmp1 = tmp0.split(',')
                cores = [eval(i) for i in tmp1]

            mem_ns = None
            if row[8] != "":
                tmp0 = row[8][1:-1]
                tmp1 = tmp0.split(',')
                mem_ns = [eval(i) for i in tmp1]

            mem_l = None
            if row[9].isnumeric():
                mem_l = int(row[9])

            env = {}
            if row[10] != "{}":
                env = dict((a[1:-1], b[1:-1])
                           for a, b in (element.split(':')
                                        for element in row[10][1:-1].split(', ')))

            w_dir = row[11]

            max_lfs = None
            if row[12].isnumeric():
                max_lfs = int(row[12])

            files_cl = None
            if row[13].isnumeric():
                files_cl = int(row[13])

            files_sl = None
            if row[14].isnumeric():
                files_sl = int(row[14])

            # RunExec's settings parameters
            param_dict = {}
            if row[15] != "{}":
                temp1 = row[15][1:-1].split('{')
                temp2 = temp1[1].split('}')
                temp3 = temp1[0].split(', ')

                # key of the value, that is a dictionary
                xtra = temp3.pop(-1)[1:-3]

                for element in temp3:
                    element = element.split(': ')
                    param_dict[element[0][1:-1]] = element[1]

                val_dict = {}
                if len(temp2) > 1:
                    for stuff in temp2[0].split(', '):
                        stuff = stuff.split(': ')
                        val_dict[stuff[0][1:-1]] = stuff[1][1:-1]
                param_dict[xtra] = val_dict

            for item in temp2[1].split(', '):
                if item != "":
                    item = item.split(': ')
                    param_dict[item[0][1:-1]] = item[1]

            for key in param_dict.keys():
                if param_dict.get(key) == "True":
                    param_dict[key] = True
                elif param_dict.get(key) == "False":
                    param_dict[key] = False

            # instantiate the RunExecutor with the given parameters - @param_dict -
            # execute the run, that's parameters have been read before
            run_result = RunExecutor(**param_dict).execute_run(
                args2,
                output_filename=out_fn,
                output_dir=out_dir,
                result_files_patterns=res_fp,
                hardtimelimit=hardtl,
                softtimelimit=softtl,
                walltimelimit=walltl,
                cores=cores,
                memory_nodes=mem_ns,
                memlimit=mem_l,
                environments=env,
                workingDir=w_dir,
                maxLogfileSize=max_lfs,
                files_count_limit=files_cl,
                files_size_limit=files_sl,
            )

            # printOut("_", end="")

            # exporting the result of the execution to a properties file

            # example file-name: folder + EXPL__SEQ_ITP.sanfoundry_24-1.properties
            result_file = open(
                parent_folder + out_fn.split('/')[-1].split('.')[0] + "." + out_fn.split('/')[-1].split('.')[
                    1] + ".properties", "w")

            exit_code = cast(Optional[util.ProcessExitCode], run_result.pop("exitcode", None))

            def print_optional_result(file, res_key):
                if res_key in run_result:
                    file.write(f"{res_key}={run_result[res_key]}\n")

            print_optional_result(result_file, "starttime")
            print_optional_result(result_file, "terminationreason")

            result_file.write(f"exitcode={repr(exit_code)}\n")

            print_optional_result(result_file, "walltime")
            print_optional_result(result_file, "cputime")

            for key in sorted(run_result.keys()):
                if key.startswith("cputime-"):
                    result_file.write(f"{key}={run_result[key]:.9f}\n")

            print_optional_result(result_file, "memory")
            print_optional_result(result_file, "blkio-read")
            print_optional_result(result_file, "blkio-write")
            print_optional_result(result_file, "exitcode")

            result_file.close()

    instance_num = ""
    for part in argv[1].split('.'):
        if re.compile('[0-9-_]').match(part):
            instance_num = part
            break
    printOut("\nWORK done!\n\ninstance code for Benchexec: "+instance_num)


def printOut(value, end="\n"):
    """
    This function prints the given String immediately and flushes the output.
    """
    sys.stdout.write(value)
    sys.stdout.write(end)
    sys.stdout.flush()


if __name__ == '__main__':
    main(sys.argv)
