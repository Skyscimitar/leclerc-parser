import subprocess
from typing import Sequence

BASE_COMMAND = ["poetry", "run"]
PYTHON_DIRECTORIES = ["leclerc_parser/", "scripts/"]


def _get_full_command_applied_to_python_directories(command_name: str) -> Sequence[str]:
    return [*BASE_COMMAND, command_name, *PYTHON_DIRECTORIES]


def _run_command_on_python_directories(command_name: str) -> None:
    try:
        subprocess.run(
            _get_full_command_applied_to_python_directories(command_name),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError as err:
        print(str(err.stdout))
        print(str(err.stderr))
        raise err


def format_python_code():
    _run_command_on_python_directories("black")


def sort_python_imports():
    _run_command_on_python_directories("isort")


def lint_python_code():
    _run_command_on_python_directories("pylint")


def check_code_style():
    sort_python_imports()
    format_python_code()
    lint_python_code()
