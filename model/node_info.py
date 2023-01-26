from dataclasses import dataclass
from typing import List
from os import getpid


@dataclass
class MemoryUsage:
    memory_total: int
    memory_available: int
    memory_percent: float
    memory_used: int

@dataclass
class CpuUsage:
    cpu_count: int
    cpu_usage: List[float]
    cpu_temp: float = None

@dataclass
class NodeInfo:
    ip: str
    hostname: str
    cpu: CpuUsage
    memory: MemoryUsage
    pid: int = getpid()
