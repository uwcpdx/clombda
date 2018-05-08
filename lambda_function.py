import subprocess as subp
import json, os


def lambda_handler(event, _):
    root = os.environ["LAMBDA_TASK_ROOT"]

    proc = subp.Popen([root + "/clj-native"],
                      env=os.environ,
                      bufsize=1,
                      universal_newlines=True,
                      stdout=subp.PIPE,
                      stderr=subp.PIPE,
                      stdin=subp.PIPE)

    stdout, stderr = proc.communicate(json.dumps(event))

    print "STDOUT"
    print stdout
    print "------"

    print "STDERR"
    print stderr
    print "------"

    print "return: " + str(proc.returncode)

    if proc.returncode == 0:
        return json.loads(stdout)
    else:
        raise Exception(stderr)

