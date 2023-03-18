FROM docker.io/nixos/nix:2.3.6

WORKDIR /workdir

COPY shell.nix .
RUN nix-env -f shell.nix -i -A buildInputs

COPY poetry.lock pyproject.toml .

RUN poetry install

COPY zhudi zhudi
COPY scripts scripts
COPY tests tests

RUN poetry run coverage run -m unittest discover
RUN poetry run coverage report --fail-under 60
