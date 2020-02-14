from urllib.parse import urljoin

import psutil
import requests
import typing
from .settings import API_URL


class Client:
    login_url = urljoin(API_URL, "auth/login/")
    disk_usage_url = urljoin(API_URL, "disks")

    headers = {"Authorization": ""}

    def login(self):
        data = {"hostname": "", "mac": "", "ip": ""}
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

    def send_disk_usage(self):
        data = self._get_disk_usage_data()
        resp = requests.post(self.disk_usage_url, json=data, headers=self.headers)
