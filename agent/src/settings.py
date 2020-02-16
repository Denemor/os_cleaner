import environs


env = environs.Env()
if env.bool("READ_ENV", False):
    env.read_env()

API_URL = env.str("API_URL", "http://localhost:5001/api/")
