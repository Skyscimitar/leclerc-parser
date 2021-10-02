import argparse
from pathlib import Path
from typing import Tuple

from .order import Order


def convert_order_to_csv(input_file_path: Path, output_file_path: Path) -> None:
    order = Order.from_file(file_path=input_file_path)
    order.write_to_csv(file_path=output_file_path)


def get_argument_parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "-i",
        "--input-file",
        help="Path to the input file containing the order",
        required=True,
    )
    argument_parser.add_argument(
        "-o", "--output-file", help="Path to write the output to", required=True
    )
    return argument_parser


def get_input_and_output_file_paths_from_arguments(
    argument_parser: argparse.ArgumentParser,
) -> Tuple[Path, Path]:
    arguments = vars(argument_parser.parse_args())
    input_file_path = Path(arguments["input_file"])
    output_file_path = Path(arguments["output_file"])
    return input_file_path, output_file_path


def main():
    argument_parser = get_argument_parser()
    input_file_path, output_file_path = get_input_and_output_file_paths_from_arguments(
        argument_parser
    )
    convert_order_to_csv(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
