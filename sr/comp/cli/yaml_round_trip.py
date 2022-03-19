_ryaml = None


def _load():
    global _ryaml
    if _ryaml is None:
        import ruamel.yaml

        _ryaml = ruamel.yaml.YAML()
        _ryaml.version = (1, 1)

        from sr.comp.yaml_loader import add_time_constructor
        add_time_constructor(ruamel.yaml)

    return _ryaml


def load(yaml_file):
    ryaml = _load()
    with open(yaml_file) as yf:
        return ryaml.load(stream=yf)


def dump(yaml_file, data):
    import io
    ryaml = _load()

    with io.StringIO() as buffer:
        ryaml.dump(data, stream=buffer)
        yaml = buffer.getvalue()

        YAML_1_1_prefix = '%YAML 1.1\n---\n'
        if yaml.startswith(YAML_1_1_prefix):
            yaml = yaml[len(YAML_1_1_prefix):]

    yaml = "\n".join(x.rstrip() for x in yaml.splitlines())
    with open(yaml_file, 'w') as yf:
        print(yaml, file=yf)


def command(settings):
    fp = settings.file_path
    dump(fp, load(fp))


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'round-trip',
        help="Round-trip a yaml file using compstate loading",
    )
    parser.add_argument('file_path', help="target file to round trip")
    parser.set_defaults(func=command)
