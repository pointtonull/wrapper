SRC = src
PYTHON = python

.PHONY: unit test coverage clean

clean:
	@echo "Cleaning all artifacts..."
	@-rm -rf _build .deps $(DEPS)

deps: .deps
.deps: $(REQUIREMENTS) requirements.txt
	pip install -qr requirements.txt
	touch .deps

tdd: tools deps
	cd $(SRC);\
	$(PYTHON) -m pytest -v --exitfirst  --pdb ../tests

try: tools deps
	cd $(SRC);\
	ipython

unit test: tools deps
	cd $(SRC);\
	$(PYTHON) -m pytest -v --doctest-modules ../tests ./

coverage: tools deps
	cd $(SRC);\
	$(PYTHON) -m pytest -v --doctest-modules ./ --cov=./ --cov-report=term-missing ../tests

tools: .tools
.tools:
	pip -q install pytest ipython
	@touch .tools

