"""The library's interface, declared in Python. gen-from-py generates the
SV interface classes (ipv4_lib_gen.sv) that the SV facade wraps."""
from typing import Protocol

from hdl_if.rt import u8, u32, u64


class Ipv4Pkt(Protocol):
    """One IPv4 packet."""

    def set_src(self, addr: str) -> None: ...

    def set_dst(self, addr: str) -> None: ...

    def get_dst(self) -> str: ...

    def set_ttl(self, ttl: u8) -> None: ...

    def get_ttl(self) -> u8: ...

    def set_protocol(self, name: str) -> None:
        """icmp, tcp or udp"""
        ...

    def add_option(self, name: str) -> None:
        """nop, rr (record route) or router_alert"""
        ...

    def set_payload(self, data: bytes) -> None: ...

    def corrupt_checksum(self) -> None: ...

    def checksum_ok(self) -> bool: ...

    def pack(self) -> bytes: ...

    def summary(self) -> str:
        """A Wireshark-style one-liner."""
        ...


class Ipv4Mutator(Protocol):
    """Protocol-aware malformed variants of a packet."""

    def mutate(self, data: bytes) -> Ipv4Pkt: ...

    def last_mutation(self) -> str: ...


class PcapWriter(Protocol):

    def write(self, data: bytes, time_ps: u64) -> None: ...

    def close(self) -> None: ...


class PcapReader(Protocol):

    def read(self) -> bytes:
        """The next packet; empty at the end of the file."""
        ...

    def close(self) -> None: ...


class Ipv4Lib(Protocol):
    """The library's entry point."""

    def new_pkt(self) -> Ipv4Pkt: ...

    def unpack(self, data: bytes) -> Ipv4Pkt: ...

    def new_mutator(self, seed: u32) -> Ipv4Mutator: ...

    def pcap_writer(self, path: str) -> PcapWriter: ...

    def pcap_reader(self, path: str) -> PcapReader: ...
