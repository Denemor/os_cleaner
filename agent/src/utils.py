import psutil
import socket
import uuid
import netifaces
import ipaddress

def get_hostname() -> str:
    return socket.gethostname()


def get_mac_addr() -> str:
    mac = uuid.getnode()
    return ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))


def get_ip_addr() -> str:
    return psutil.net_if_addrs()


def network_addr():

    netifaces.interfaces()