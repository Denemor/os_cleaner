import logging
import typing
import subprocess
from urllib.parse import urljoin

import psutil
import requests

from src.settings import API_URL, CLEAN_COMMAND
from src.utils import get_hostname, get_ip_addr


class Client:
    login_url = urljoin(API_URL, "agent/")
    disk_usage_url = urljoin(API_URL, "disks/")
    command_result_url = urljoin(API_URL, "tasks/")

    headers = {"Authorization": ""}

    def login(self):

        return {"hostname": get_hostname(),
                "ip": get_ip_addr()}

    def _command_execute(self) -> typing.Dict:
        res = subprocess.Popen(CLEAN_COMMAND,
                               stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE,
                               )
        stdout, stderr = res.communicate()

        return {
                "metadata": self.login(),
                "data": {
                         "code": res.returncode,
                         "output": stdout.decode("utf-8"),
                         "errors": stderr.decode("utf-8"),
                         "command": CLEAN_COMMAND
                        }
                }


    def _get_disk_usage_data(self):
        results = []
        for disk in psutil.disk_partitions():
            usage = psutil.disk_usage(disk.mountpoint)
            results.append(
                {
                    "mountpoint": disk.mountpoint,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent,
                }
            )
        return {
                "metadata": self.login(),
                "data": results
                }

    def send_data(self, func, url):
        data = func()

        if not isinstance(data, list):
            data = [data]

        resp = requests.post(url=url,
                             json=data,
                             headers=self.headers)

        if 200 <= resp.status_code < 300:
            logging.info(resp.status_code)
        else:
            logging.error(resp.text)

    def run(self):
        __ = [
            {
                'function': self._get_disk_usage_data,
                'url': self.disk_usage_url
            },
            {
                'function': self._command_execute,
                'url': self.command_result_url
            }
        ]
        for func in __:
            try:
                self.login()
                self.send_data(func=func['function'], url=func['url'])
            except Exception as e:
                logging.error(e)
