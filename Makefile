PYTHON=PYTHONPATH=src:. python
COVERAGE=/usr/local/bin/coverage
EXAMPLES=$(notdir $(wildcard examples/*.py))
RUN_EXAMPLES=$(patsubst %,run_%,${EXAMPLES})

all: test coverage

run: ${RUN_EXAMPLES}
	echo $<

run_%: examples/%
	@echo "*** executing $<"
	@${PYTHON} $<
	@echo

test:
	@echo "*** performing unittests"
	@${PYTHON} $(COVERAGE) run -m unittest discover -s src -p 'test_*.py'

coverage:
	@echo "*** generating unittest coverage report (based on last test run)"
	@$(COVERAGE) report -m --omit '/Library/*,*__init__.py,*test_*.py'

clean:

.PHONY: all clean run
