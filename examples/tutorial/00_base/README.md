# 0. The starting point

The UVM env for the IPv4 forwarder with an SV-only scoreboard, and no
Python. Every other example starts from here and changes one thing.

```bash
make run        # SIM=vlt by default
```

The base test programs four routes, sends 40 random packets (some with a
bad checksum, TTL <= 1, a malformed header or no route), waits for the
forwarded ones to come out, and checks the DUT's counters against the
scoreboard. `+N_PKTS=<n>` changes the count.
