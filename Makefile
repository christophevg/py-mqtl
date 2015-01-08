PYTHON=PYTHONPATH=src:. python

all: run

run:
	@${PYTHON} examples/visitor.py

clean:

.PHONY: all clean run
