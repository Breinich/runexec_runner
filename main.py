import csv
import sys
from benchexec.runexecutor import RunExecutor


def main(argv):
    #     args,
    #     output_filename=run.log_file,
    #     output_dir=run.result_files_folder,
    #     result_files_patterns=benchmark.result_files_patterns,
    #     hardtimelimit=benchmark.rlimits.cputime_hard,
    #     softtimelimit=benchmark.rlimits.cputime,
    #     walltimelimit=benchmark.rlimits.walltime,
    #     cores=self.my_cpus,
    #     memory_nodes=self.my_memory_nodes,
    #     memlimit=benchmark.rlimits.memory,
    #     environments=benchmark.environment(),
    #     workingDir=benchmark.working_directory(),
    #     maxLogfileSize=benchmark.config.maxLogfileSize,
    #     files_count_limit=benchmark.config.filesCountLimit,
    #     files_size_limit=benchmark.config.filesSizeLimit,
    with open(argv[1]) as input_csv:
        input_reader = csv.reader(input_csv, delimiter=';')
        for row in input_reader:
            args2 = row[0][1:-1].split(', ')
            i = 0
            for a in args2:
                a = a[1:-1]
                args2[i] = a
                i = i + 1
            out_fn = row[1]
            out_dir = row[2]
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

            param_dict = {}
            if row[15] != "{}":
                temp1 = row[15][1:-1].split('{')
                temp2 = temp1[1].split('}')
                temp3 = temp1[0].split(', ')

                # key of the value, that is a dict
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

            # Union[OrderedDict[str, Union[ProcessExitCode, dict, str]], Dict[str, str], Dict[str, str]]
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



    #     args,
    #     output_filename=run.log_file,
    #     output_dir=run.result_files_folder,
    #     result_files_patterns=benchmark.result_files_patterns,
    #     hardtimelimit=benchmark.rlimits.cputime_hard,
    #     softtimelimit=benchmark.rlimits.cputime,
    #     walltimelimit=benchmark.rlimits.walltime,
    #     cores=self.my_cpus,
    #     memory_nodes=self.my_memory_nodes,
    #     memlimit=benchmark.rlimits.memory,
    #     environments=benchmark.environment(),
    #     workingDir=benchmark.working_directory(),
    #     maxLogfileSize=benchmark.config.maxLogfileSize,
    #     files_count_limit=benchmark.config.filesCountLimit,
    #     files_size_limit=benchmark.config.filesSizeLimit,
    # )


if __name__ == '__main__':
    main(sys.argv)
