import psutil
import socket
import ipaddress
from agent.src.settings import IGNORED_NETWORKS

def if_in_ignored_network(ip):
    networks = IGNORED_NETWORKS.split(',')

    for network in networks:
        network = network.strip()
        if type(ip) is not ipaddress.ip_address:
            ip = ipaddress.ip_address(ip)

        if ip in ipaddress.ip_network(network):
            return True

    return False

def get_hostname() -> str:
    return socket.gethostname()


def get_ip_addr() -> str:
    res = []
    for __, data in psutil.net_if_addrs().items():
        for info in data:
            if info.family == socket.AF_INET:
                if not if_in_ignored_network(info.address):
                    res.append(info.address)
    return ", ".join(res)
