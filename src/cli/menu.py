from pprint import pprint
import inquirer
from cli.operation import Operation


def main_menu() -> Operation:
    questions = [
        inquirer.List(
            "operation",
            message="Select an operation:",
            choices=[op.value for op in Operation],
        ),
    ]

    answers = inquirer.prompt(questions)
    return Operation(answers["operation"])
