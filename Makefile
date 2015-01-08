PYTHON=PYTHONPATH=src:. python

all: run

run: run-visitor run-basic_query

run-%: examples/%.py
	@echo "*** executing $<"
	@${PYTHON} $<
	@echo

clean:

.PHONY: all clean run
