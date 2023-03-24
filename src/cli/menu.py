import inquirer
from cli.operation import Operation
from cli.bcolors import bcolors
from playlist import Playlist


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


def playlists_checkbox(playlists: list[Playlist]) -> list[Playlist]:

    questions = [
        inquirer.Confirm("isAll",
                         message=f"{bcolors.BOLD}Do you want to sync all spotify playlists?{bcolors.ENDC}",
                         default=False),
        inquirer.Checkbox("playlists",
                          message=f"{bcolors.BOLD}Which playlists do you want to sync?{bcolors.ENDC}",
                          choices=[playlist.name for playlist in playlists],
                          ignore=lambda answer: answer["isAll"],
                          ),
    ]

    answers = inquirer.prompt(questions)

    if answers["isAll"]:
        return playlists

    elif answers["playlists"] == []:
        questions = [
            inquirer.Confirm("isEmpty",
                             message=f"{bcolors.BOLD}You have not selected any playlists. Do you want to exit?{bcolors.ENDC}",
                             default=False),
        ]

        if (inquirer.prompt(questions)["isEmpty"]):
            exit(0)
        else:
            print()
            return playlists_checkbox(playlists)

    else:
        return list(playlist for playlist in playlists if playlist.name.casefold() in [playlist.casefold() for playlist in answers["playlists"]])
