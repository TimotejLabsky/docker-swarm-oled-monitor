from psutil import virtual_memory, cpu_percent, cpu_count
from socket import gethostname, gethostbyname
from model.model import NodeInfo, CpuUsage, MemoryUsage
from typing import Callable, List
from os import environ

# sensors_temperatures is not available on Windows or Mac
try:
    from psutil import sensors_temperatures
except ImportError:
    from dataclasses import dataclass
    from random import uniform
    @dataclass
    class shwtemp:
        label: str
        current: float
        high: float = None
        critical: float = None

        def __repr__(self):
            return f"shwtemp(label='{self.label}', current={self.current}, high={self.high}, critical={self.critical})"

    def sensors_temperatures():
        return {'cpu_thermal': [shwtemp(label='DUMMY VALUES !!!', current=uniform(15.0, 80.0), high=None, critical=None)]}


class Monitor():
    def __init__(self) -> None:
        self.__hostname: str = environ.get('HOSTNAME', gethostname())
        self.__ip: str = environ.get('HOST_IP', Monitor.__get_ip_by_host_name(self.__hostname))
        self.__callbacks: List[Callable[[], NodeInfo]] = []

    @staticmethod
    def get_memory_usage() -> MemoryUsage:
        memory = virtual_memory()
        return MemoryUsage(memory.total, memory.available, memory.percent, memory.used)

    @staticmethod
    def get_cpu_usage() -> CpuUsage:
        cpu = cpu_percent(percpu=True)
        return CpuUsage(cpu_count(), cpu, sensors_temperatures()['cpu_thermal'][0].current)

    def add_callback(self, callback: Callable[[], NodeInfo]) -> None:
        self.__callbacks.append(callback)

    def get_node_info(self) -> NodeInfo:
        return NodeInfo(self.__ip, self.__hostname, Monitor.get_cpu_usage(), Monitor.get_memory_usage())

    def run(self) -> None:
        node_info: NodeInfo = self.get_node_info()
        for callback in self.__callbacks:
            callback(node_info)

    @staticmethod
    def __get_ip_by_host_name(hostname: str) -> str:
        try:
            return gethostbyname(hostname)
        except:
            return gethostbyname(gethostname())
