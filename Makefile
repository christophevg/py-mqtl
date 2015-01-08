PYTHON=PYTHONPATH=src:. python
EXAMPLES=$(notdir $(wildcard examples/*.py))
RUN_EXAMPLES=$(patsubst %,run_%,${EXAMPLES})

all: run

run: ${RUN_EXAMPLES}
	echo $<

run_%: examples/%
	@echo "*** executing $<"
	@${PYTHON} $<
	@echo

clean:

.PHONY: all clean run
