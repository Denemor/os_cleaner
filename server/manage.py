from os_cleaner.app import create_app
from config import *

application = create_app()


if __name__ == "__main__":
    application.run(host=HOST, port=PORT, debug=True)
