.PHONY: flake mypy pytest check html tox

flake:
	-uv run flake8 || true

mypy:
	-uv run mypy ambra_sdk || true

pytest:
	-uv run pytest || true

check: flake mypy doctest pytest

html:
	-uv run sphinx-build -b html docs/source docs/build || true
text:
	-uv run sphinx-build -b text docs/source docs/build/texts || true
text-unify:
	-cat docs/build/texts/index.txt \
             docs/build/texts/installation.txt \
             docs/build/texts/quickstart.txt \
             docs/build/texts/service_api.txt \
             docs/build/texts/storage_api.txt \
             docs/build/texts/addon.txt \
             docs/build/texts/faq.txt > docs/build/texts/single.txt || true
doctest:
	-uv run sphinx-build -b doctest docs/source docs/build || true
spelling:
	-uv run sphinx-build -b spelling docs/source docs/build || true
gh:
	-uv run sphinx-build -b html docs/source ../sdk-python-doc || true
	-touch ../sdk-python-doc/.nojekyll
tox:
	-uv run tox || true

check-full: flake mypy doctest tox
