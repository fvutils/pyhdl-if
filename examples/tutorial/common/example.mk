# Included by each example's Makefile, which sets PKG to its dfm package name.
SIM ?= vlt

run:
	dfm run -D sim=$(SIM) sim-run
	@if grep -q "TEST PASSED" rundir/$(PKG).sim-run/sim.log; then \
		echo "PASS: $(PKG)"; \
	else \
		echo "FAIL: $(PKG) (see rundir/$(PKG).sim-run/sim.log)"; exit 1; \
	fi

clean:
	rm -rf rundir

.PHONY: run clean
