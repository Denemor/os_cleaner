import logging
import typing
from urllib.parse import urljoin

import psutil
import requests

from src.settings import API_URL
from src.utils import get_hostname, get_mac_addr, get_ip_addr


class Client:
    login_url = urljoin(API_URL, "auth/login/")
    disk_usage_url = urljoin(API_URL, "disk-statictics/")

    headers = {"Authorization": ""}

    def login(self):
        data = {"hostname": get_hostname(), "mac": get_mac_addr(), "ip": get_ip_addr()}
        resp = requests.post(self.login_url, json=data)
        data = resp.json()

        if resp.status_code == 200:
            self.headers.update({"Authorization": data["access"]})

    def _get_disk_usage_data(self) -> typing.List[typing.Dict]:
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
        return results

    def send_disk_usage(self):
        data = self._get_disk_usage_data()
        resp = requests.post(self.disk_usage_url, json=data, headers=self.headers)

        if resp.status_code in {401, 403}:
            self.login()

        resp = requests.post(self.disk_usage_url, json=data, headers=self.headers)

        if 200 <= resp.status_code < 300:
            logging.info(resp.status_code)
        else:
            logging.error(resp.text)
