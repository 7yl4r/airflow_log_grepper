import os
import sys
import subprocess

from airflow_log_grepper.log_grepper import get_grepped_log_counts
from airflow_log_grepper.sanitize_glob_string import sanitize_glob_string


def main():
    _main(*sys.argv[1:])


def _main(greps_json_file, dag_logs_dir, testing=False):
    if (
        testing is not False and
        testing.lower() in ['y', '1', 'yes', 'test', 'testing', 'true']
    ):
        print("test mode")
        testing = True
    else:
        testing = False

    print("-"*100)
    HOSTNAME = subprocess.check_output("hostname -s", shell=True).strip()
    DATE = subprocess.check_output("date +%s", shell=True).strip()
    # DAG name for graphite comes from filename
    dag_dir_glob = os.path.basename(greps_json_file).replace(".json", "")

    for match_name, count in get_grepped_log_counts(
        greps_json_file, dag_logs_dir
    ):
        metric = "{host}.exec.per_one_hour.airflow.logs.{dag}.{match}".format(
            host=HOSTNAME,
            dag=sanitize_glob_string(dag_dir_glob),
            match=match_name
        )
        if not testing:
            cmd = (
                "timeout 3 echo {metric} {count} {dt} | " +
                "nc {server} {port}"
            ).format(
                metric=metric,
                count=count,
                dt=DATE,
                server="graphite",
                port=2003
            )
            result = subprocess.check_output(
                cmd,
                shell=True,
            )
            print("{}\n---------------------------\n\t{}".format(cmd, result))
        else:
            print("{} {} {}".format(metric, count, DATE))

if __name__ == "__main__":
    main()
