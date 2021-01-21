#!/usr/bin/python3
import subprocess
import sys
import json


# --- Extract arguments
if (len(sys.argv) != 1):
    prominence_job = sys.argv[1]
else:
    sys.exit()

try:
    cmd = 'prominence describe '+prominence_job
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    output = str(process.stdout.read(),'utf-8')
    described_json = json.loads(output)
    outputDirs = described_json["outputDirs"][0]
    outputDirs = str(outputDirs).replace("\'","\"")
    outputDirs = json.loads(outputDirs)
    url = outputDirs["url"]
    print(url)
except Exception as exc:
    sys.exit()

sys.exit()



