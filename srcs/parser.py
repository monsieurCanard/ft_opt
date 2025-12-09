import argparse


def init_parser():
    parser = argparse.ArgumentParser(
        description="Temporary Password Generator - HOTP (HMAC-based One-Time Password)",
        add_help=True,
    )

    parser.add_argument("-g", type=str, help="Take a key from a given file")

    parser.add_argument(
        "-k", type=str, help="Generate temporary password based on the given key"
    )

    return parser
