from psutil import virtual_memory, cpu_percent, cpu_count
from socket import gethostname, gethostbyname
from model.node_info import NodeInfo, CpuUsage, MemoryUsage

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

def get_memory_usage() -> MemoryUsage:
    memory = virtual_memory()
    return MemoryUsage(memory.total, memory.available, memory.percent, memory.used)


def get_cpu_usage() -> CpuUsage:
    cpu = cpu_percent(percpu=True)
    return CpuUsage(cpu_count(), cpu, sensors_temperatures()['cpu_thermal'][0].current)


def get_node_info() -> NodeInfo:
    return NodeInfo(gethostbyname(gethostname()), gethostname(), get_cpu_usage(), get_memory_usage())
