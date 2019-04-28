import subprocess
import signal
import os
import sys

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

os.chdir("../code")

producer_script = "../harness/recipe-steps/dev/console-producer.sh"
usa_consumer_script = "../harness/recipe-steps/dev/console-consumer-usa.sh"
mex_consumer_script = "../harness/recipe-steps/dev/console-consumer-mex.sh"
ger_consumer_script = "../harness/recipe-steps/dev/console-consumer-ger.sh"
other_consumer_script = "../harness/recipe-steps/dev/console-consumer-other.sh"
run_app_script = "../harness/recipe-steps/dev/run-dev-app.sh"

inputs_file = "../harness/recipe-steps/dev/input-events.json"
usa_outputs_file = "../harness/recipe-steps/dev/outputs/actual-usa-events.json"
mex_outputs_file = "../harness/recipe-steps/dev/outputs/actual-mex-events.json"
ger_outputs_file = "../harness/recipe-steps/dev/outputs/actual-ger-events.json"
other_outputs_file = "../harness/recipe-steps/dev/outputs/actual-other-events.json"

timeout_ms = 3000

def run_consumer(consumer_script):
    consumer_file = open(consumer_script, "r")
    consumer_cmd = consumer_file.read()[:-1] + " --timeout-ms " + str(timeout_ms)
    consumer_cmds = consumer_cmd.split()
    consumer_file.close()

    return subprocess.run(consumer_cmds, stdout=subprocess.PIPE)

def write_consumer_output(consumer, outputs_file):
    output_file = open(outputs_file, "w")
    output_file.write(str(consumer.stdout, "UTF-8"))
    output_file.close()

producer = subprocess.run(["sh", producer_script],
                          stdin=open(inputs_file, "r"),
                          stdout=subprocess.PIPE)
app = subprocess.Popen(["sh", run_app_script], preexec_fn=os.setsid)

usa_consumer = run_consumer(usa_consumer_script)
mex_consumer = run_consumer(mex_consumer_script)
ger_consumer = run_consumer(ger_consumer_script)
other_consumer = run_consumer(other_consumer_script)

os.killpg(os.getpgid(app.pid), signal.SIGTERM)
app.terminate()

write_consumer_output(usa_consumer, usa_outputs_file)
write_consumer_output(mex_consumer, mex_outputs_file)
write_consumer_output(ger_consumer, ger_outputs_file)
write_consumer_output(other_consumer, other_outputs_file)
