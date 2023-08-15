import argparse
import kup
import logging
import sys


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files",
        nargs="*",
        type=str,
        default=[],
        help=(
            "Input files containing multiple manifests to unpack. "
            "If none specified, manifests are read from stdin."
        ),
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default=".",
        help="Directory to unpack into (default: .).",
    )
    args = parser.parse_args(sys.argv[1:])
    for yaml_text in kup.read_all(args.files):
        kup.unpack(args.directory, yaml_text)


if __name__ == "__main__":
    main()
