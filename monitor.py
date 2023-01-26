from psutil import virtual_memory, cpu_percent, cpu_count
from socket import gethostname, gethostbyname
from model.node_info import NodeInfo, CpuUsage, MemoryUsage
from threading import Thread
from typing import Callable, List
from time import sleep

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
        return {'cpu_thermal': [shwtemp(label='', current=uniform(15.0, 80.0), high=None, critical=None)]}


class Monitor(Thread):
    def __init__(self, check_interval: int = 1) -> None:
        super().__init__()
        self.__hostname: str = gethostname()
        self.__ip: str = gethostbyname(self.__hostname)
        self.__check_interval: int = check_interval
        self.__callbacks: List[Callable[[], NodeInfo]] = []
        self.__run: bool = True

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
        while self.__run:
            for callback in self.__callbacks:
                callback(self.get_node_info())
            sleep(self.__check_interval)

    def stop(self) -> None:
        self.__run = False