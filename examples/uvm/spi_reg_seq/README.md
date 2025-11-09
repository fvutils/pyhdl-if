# SPI Register Model UVM Example

Contents
- top_pkg.sv: UVM RAL model, adapter, bus agent, env, test
- top.sv: Testbench top calling run_test()
- pyseq.py: Optional Python sequence that drives raw bus ops
- flow.yaml: dv-flow description to build and run

Address map (byte addressing, stride 4)
- 0x00 CTRL   (RW): enable[0], master[1], cpol[2], cpha[3], lsb_first[4]
- 0x04 STATUS (RO): busy[0], tx_empty[1], rx_full[2]
- 0x08 CLKDIV (RW): div[15:0]
- 0x0C SS     (RW): ss_mask[3:0]
- 0x10 TXDATA (WO): data[7:0]
- 0x14 RXDATA (RO): data[7:0]

Run with dv-flow (from workspace root)
- Choose simulator: -Dsim=mti | -Dsim=vcs | -Dsim=xcm
- Task: sim-run

```bash
# Example (Questa/Modelsim)
python -m dv_flow run \
  --workspace . \
  --root examples/uvm/spi_reg_seq/flow.yaml \
  --task sim-run \
  -Dsim=mti
```

Notes
- Python warnings from Pylance about unknown attrs on SV req are intentional; `setattr` is used to set fields exposed by the SV `seq_item`.
- The driver emulates a simple memory-mapped backend for demonstrating frontdoor RAL accesses.
