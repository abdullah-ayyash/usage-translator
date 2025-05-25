
.PHONY: run test install clean

install:
	pip install -r requirements.txt

run:
	python src/main.py

test:
	pytest -v tests/

clean:
	rm -f output.sql
