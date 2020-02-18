import environs
import os

env = environs.Env()
if env.bool("READ_ENV", False):
    env.read_env()

if os.name == 'nt':
    DEFAULT_CLEAN_COMMAND = "cleanmgr.exe /verylowdisk /sagerun:1"
else:
    DEFAULT_CLEAN_COMMAND = "yum clean all"

IGNORED_NETWORKS = '127.0.0.0/8, 169.254.0.0/16'

API_URL = env.str("API_URL", "http://localhost:5001/api/")

CLEAN_COMMAND = env.str("CLEAN_COMMAND", DEFAULT_CLEAN_COMMAND)