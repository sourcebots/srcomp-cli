from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, IO, TYPE_CHECKING, Union

if TYPE_CHECKING:
    import ruamel.yaml

_ryaml = None


def _load() -> ruamel.yaml.YAML:
    global _ryaml
    if _ryaml is None:
        import ruamel.yaml

        _ryaml = ruamel.yaml.YAML()
        _ryaml.version = (1, 1)  # type: ignore[assignment]

        from sr.comp.yaml_loader import add_time_constructor
        add_time_constructor(_ryaml.Constructor)

    return _ryaml


def load(source: Union[Path, IO[str]]) -> Any:
    ryaml = _load()
    return ryaml.load(stream=source)


def dump(data: Dict[str, Any], dest: Union[Path, IO[str]]) -> None:
    import io
    ryaml = _load()

    with io.StringIO() as buffer:
        ryaml.dump(data, stream=buffer)
        yaml = buffer.getvalue()

        YAML_1_1_prefix = '%YAML 1.1\n---\n'
        if yaml.startswith(YAML_1_1_prefix):
            yaml = yaml[len(YAML_1_1_prefix):]

    yaml = "\n".join(x.rstrip() for x in yaml.splitlines()) + "\n"
    if isinstance(dest, Path):
        dest.write_text(yaml)
    else:
        dest.write(yaml)


def command(settings: argparse.Namespace) -> None:
    fp = settings.file_path
    dump(load(fp), dest=fp)


def add_subparser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        'round-trip',
        help="Round-trip a yaml file using compstate loading",
    )
    parser.add_argument(
        'file_path',
        help="target file to round trip",
        type=Path,
    )
    parser.set_defaults(func=command)
