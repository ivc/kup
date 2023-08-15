import logging
import pathlib
import re
import sys
import typing
import yaml


class SafeLoaderWithDocBody(yaml.SafeLoader):
    def compose_document(self) -> yaml.Node | None:
        start = self.get_mark()
        doc = super().compose_document()
        end = self.get_mark()
        # only supports string input, but not files/streams
        self.doc_body = trim_yaml(self.buffer[start.pointer : end.pointer])
        return doc


def trim_yaml(body: str) -> str:
    return body.strip().removeprefix("---\n").removesuffix("\n---") + "\n"


def camel_to_kebab(text: str) -> str:
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r"-\1", text).lower()


def file_path(base_path: str, resource: typing.Dict[str, str]) -> pathlib.Path:
    kind = resource["kind"]
    name = resource["metadata"]["name"]
    return pathlib.PosixPath(base_path, camel_to_kebab(kind), name + ".yaml")


def read_all(paths: typing.List[str]) -> typing.Generator[str, None, None]:
    if not paths:
        logging.info("Reading from STDIN")
        yield sys.stdin.read()
        return
    for path in paths:
        logging.info("Reading from %s", path)
        yield pathlib.PosixPath(path).read_text()


def unpack(base_path: str, text: str) -> None:
    loader = SafeLoaderWithDocBody(text)
    try:
        while loader.check_data():
            resource = loader.get_data()
            path = file_path(base_path, resource)
            logging.info("Saving %s", path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(loader.doc_body)
    finally:
        loader.dispose()
