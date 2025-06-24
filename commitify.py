# METADATA
VERSION = '1.2.9'
PRE_RELEASE = False
# METADATA ENDS

import os
import sys
import argparse
import requests
from InquirerPy import prompt
from InquirerPy.base.control import Choice
from helpers import config as config_helper
from helpers import utils as utils_helper
import printedcolors

Color = printedcolors.Color
fg_color = Color.fg

def is_running_through_pyinstaller():
    return hasattr(sys, '_MEIPASS')

parser = argparse.ArgumentParser(description="Argument parser", add_help=False)

# Add the -a flag as a boolean action
parser.add_argument("-a", action="store_true", help="Automaticlly add files before commiting.")
parser.add_argument("-p", action="store_true", help="Automaticlly push files after commiting.")
parser.add_argument("-h", action="store_true", help="Help.")
parser.add_argument("--help", action="store_true", help="Help.")

# Create a subparser for commands
commandparser = parser.add_subparsers(dest='command', required=False)
update = commandparser.add_parser('update', help='Update the script to latest version')
init_git = commandparser.add_parser('init', help='Inits the git project with commitify.')

def validate_required_input(input):
    """Validate that the input is not empty."""
    return bool(input)


def download_script(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {filename}")



# Parse the arguments
args = parser.parse_args()

if args.command == 'update':
    if is_running_through_pyinstaller():
        print("WARNING: Update only works with the python script. More versions will be added soon.")
        sys.exit(1)
    print("Downloading Update Script. This won't take too long.")
    download_script("https://raw.githubusercontent.com/kokofixcomputers/Commitify/refs/heads/main/helpers/update.py", "helpers/update.py")
    from helpers import update
    # Updating is not currently implemented.
    print("FeatureNotImplemented: This feature has not been implemented.")
    sys.exit(1)
    print("Checking for updates...")
    updates, download_url, found = update.check_for_updates(VERSION)
    if updates:
        print("Updates available!")
        print("Updating...")
        update.update_script(download_url)
    sys.exit(0)

elif args.command == 'init':
    if not utils_helper.is_git_directory():
        print(fg_color.red + "Error: The current directory is not a git initiated directory. Please `cd` into a git directory and try again." + Color.reset)
        sys.exit(1)
    current_dir = os.getcwd()
    if not config_helper.check_project_directory(current_dir):
        print("Welcome to Commitify! Initiating the current directory. Please wait...")
        git_remotes = utils_helper.get_git_remotes()
        git_branches = utils_helper.get_git_branches()
        def create_choices_from_branches(branches):
            choices = [Choice(name=branch, value=branch) for branch in branches]
            return choices
        choices = create_choices_from_branches(git_branches)
        standard_format_choices = [
            Choice(name="Gitmoji", value="gitmoji")
        ]

        choice = prompt(
            [
                {
                    "type": "list",
                    "name": "change_type",
                    "message": "Select a branch you want to commit to. (Move up and down to reveal more choices):",
                    "choices": choices,
                    "default": choices[0].value,
                    "pointer": "❯",
                    "validate": validate_required_input,
                }
            ]
        )
        standard_format_choice = prompt(
            [
                {
                    "type": "list",
                    "name": "standard_format",
                    "message": "Select a standard format. (Move up and down to reveal more choices):",
                    "choices": standard_format_choices,
                    "default": standard_format_choices[0].value,
                    "pointer": "❯",
                    "validate": validate_required_input,
                }
            ]
        )

        config_helper.ensure_project_directory(current_dir, choice['change_type'], standard_format_choice['standard_format'])
    sys.exit(0)

if args.h or args.help:
    print("Commitify")
    print("Style your commits.")
    print("Made by kokofixcomputers at https://kokodev.cc")
    print("GitHub: https://github.com/kokofixcomputers/Commitify")
    print("""------------------------------------------------------""")
    print("Available flag/arguments:")
    print("Arguments may be used together.")
    print("-a Automatically add files before commiting with `git add`")
    print("-p Automatically push files after commiting with `git push`")
    print("-h, --help Help (This Help)")
    print("Available commands:")
    print("update Automatically update the script with the latest version.")
    print("init Inits the git project with commitify.")
    sys.exit(0)
    

add = True if args.a else False
push = True if args.p else False
if args.a:
    print(f"Running git add.")
if args.p:
    print(f"Push after commit.")
    


def main():
    current_working_directory = os.getcwd()
    if not config_helper.check_project_directory(current_working_directory):
        print(fg_color.red + "Error: Project not initiated with Commitify. Please run <commitify file> init. Then re-try." + Color.reset)
        exit(1)
    configuration = config_helper.read_files()
    # Define the choices with emojis
    choices = [
        Choice(name="🎨 Improve structure / format of the code.", value=":art: style:"),
        Choice(name="⚡ Improve performance.", value=":zap: perf:"),
        Choice(name="🔥 Remove code or files.", value=":fire: fix:"),
        Choice(name="🐛 Fix a bug.", value=":bug: fix:"),
        Choice(name="🚑 Critical hotfix.", value=":ambulance: fix:"),
        Choice(name="✨ Introduce new features.", value=":sparkles: feat:"),
        Choice(name="📝 Add or update documentation.", value=":memo: docs:"),
        Choice(name="🚀 Deploy stuff.", value=":rocket: deploy:"),
        Choice(
            name="💄 Add or update the UI and style files.", value=":lipstick: style:"
        ),
        Choice(name="🎉 Begin a project.", value=":tada: init:"),
        Choice(name="✅ Add, update, or pass tests.", value=":white_check_mark: test:"),
        Choice(name="🔒 Fix security or privacy issues.", value=":lock: fix:"),
        Choice(name="🔐 Add or update secrets.", value=":closed_lock_with_key: sec:"),
        Choice(name="🔖 Release / Version tags.", value=":bookmark: version:"),
        Choice(
            name="🚨 Fix compiler / linter warnings.", value=":rotating_light: fix:"
        ),
        Choice(name="🚧 Work in progress.", value=":construction: wip:"),
        Choice(name="💚 Fix CI Build.", value=":green_heart: ci:"),
        Choice(name="⬇️ Downgrade dependencies.", value=":arrow_down: chore:"),
        Choice(name="⬆️ Upgrade dependencies.", value=":arrow_up: chore:"),
        Choice(
            name="📌 Pin dependencies to specific versions.", value=":pushpin: chore:"
        ),
        Choice(
            name="👷 Add or update CI build system.",
            value=":construction_worker: chore:",
        ),
        Choice(
            name="📈 Add or update analytics or track code.",
            value=":chart_with_upwards_trend: feat:",
        ),
        Choice(name="♻️ Refactor code.", value=":recycle: refactor:"),
        Choice(name="➕ Add a dependency.", value=":heavy_plus_sign: feat:"),
        Choice(name="➖ Remove a dependency.", value=":heavy_minus_sign: fix:"),
        Choice(name="🔧 Add or update configuration files.", value=":wrench: chore:"),
        Choice(name="🔨 Add or update development scripts.", value=":hammer: chore:"),
        Choice(
            name="🌐 Internationalization and localization.",
            value=":globe_with_meridians: feat:",
        ),
        Choice(name="✏️ Fix typos.", value=":pencil2: docs:"),
        Choice(
            name="💩 Write bad code that needs to be improved.", value=":poop: fix:"
        ),
        Choice(name="⏪ Revert changes.", value=":rewind: revert:"),
        Choice(name="🔀 Merge branches.", value=":twisted_rightwards_arrows: merge:"),
        Choice(
            name="📦 Add or update compiled files or packages.",
            value=":package: chore:",
        ),
        Choice(
            name="👽 Update code due to external API changes.", value=":alien: feat:"
        ),
        Choice(
            name="🚚 Move or rename resources (e.g.: files, paths, routes).",
            value=":truck: chore:",
        ),
        Choice(name="📄 Add or update license.", value=":page_facing_up: docs:"),
        Choice(name="💥 Introduce breaking changes.", value=":boom: BREAKING CHANGE:"),
        Choice(name="🍱 Add or update assets.", value=":bento: feat:"),
        Choice(name="♿ Improve accessibility.", value=":wheelchair: feat:"),
        Choice(name="💡 Add or update comments in source code.", value=":bulb: docs:"),
        Choice(name="🍻 Write code drunkenly.", value=":beers: fix:"),
        Choice(
            name="💬 Add or update text and literals.", value=":speech_balloon: docs:"
        ),
        Choice(
            name="📁 Perform database related changes.", value=":card_file_box: chore:"
        ),
        Choice(name="🔊 Add or update logs.", value=":loud_sound: chore:"),
        Choice(name="🔇 Remove logs.", value=":mute: chore:"),
        Choice(
            name="👥 Add or update contributor(s).", value=":busts_in_silhouette: feat:"
        ),
        Choice(
            name="🚸 Improve user experience / usability.",
            value=":children_crossing: feat:",
        ),
        Choice(
            name="🏗️ Make architectural changes.",
            value=":building_construction: refactor:",
        ),
        Choice(name="📱 Work on responsive design.", value=":iphone: feat:"),
        Choice(name="🤡 Mock things.", value=":clown_face: test:"),
        Choice(name="🥚 Add or update an easter egg.", value=":egg: feat:"),
        Choice(
            name="🙈 Add or update a .gitignore file.", value=":see_no_evil: chore:"
        ),
        Choice(name="📸 Add or update snapshots.", value=":camera_flash: test:"),
        Choice(name="⚗️ Perform experiments.", value=":alembic: chore:"),
        Choice(name="🔍 Improve SEO.", value=":mag: feat:"),
        Choice(name="🏷️ Add or update types.", value=":label: docs:"),
        Choice(name="🌱 Add or update seed files.", value=":seedling: feat:"),
        Choice(
            name="🚩 Add, update, or remove feature flags.",
            value=":triangular_flag_on_post: feat:",
        ),
        Choice(name="🥅 Catch errors.", value=":goal_net: test:"),
        Choice(
            name="💫 Add or update animations and transitions.", value=":dizzy: feat:"
        ),
        Choice(
            name="🗑️ Deprecate code that needs to be cleaned up.",
            value=":wastebasket: fix:",
        ),
        Choice(
            name="🛂 Work on code related to authorization, roles and permissions.",
            value=":passport_control: feat:",
        ),
        Choice(
            name="🩹 Simple fix for a non-critical issue.",
            value=":adhesive_bandage: fix:",
        ),
        Choice(name="🧐 Data exploration/inspection.", value=":monocle_face: docs:"),
        Choice(name="⚰️ Remove dead code.", value=":coffin: fix:"),
        Choice(name="🧪 Add a failing test.", value=":test_tube: test:"),
        Choice(name="👔 Add or update business logic.", value=":necktie: feat:"),
        Choice(name="🩺 Add or update healthcheck.", value=":stethoscope: feat:"),
        Choice(name="🧱 Infrastructure related changes.", value=":bricks: chore:"),
        Choice(
            name="🧑‍💻 Improve developer experience.", value=":technologist: chore:"
        ),
        Choice(
            name="💸 Add sponsorships or money related infrastructure.",
            value=":money_with_wings: chore:",
        ),
        Choice(
            name="🧵 Add or update code related to multithreading or concurrency.",
            value=":thread: feat:",
        ),
        Choice(
            name="🦺 Add or update code related to validation.",
            value=":safety_vest: feat:",
        ),
    ]

    # Prompt the user to select an option
    answers = prompt(
        [
            {
                "type": "fuzzy",
                "name": "change_type",
                "message": "Select the type of change you're committing. (Move up and down to reveal more choices):",
                "choices": choices,
                "pointer": "❯",  # Pointer emoji for highlighting
                "validate": validate_required_input,
            }
        ]
    )

    # Follow-up question based on the selected option
    description = prompt(
        [
            {
                "type": "input",
                "name": "description",
                "message": f"Please provide a short description:",
                "validate": validate_required_input,
            }
        ]
    )

    longdescription = prompt(
        [
            {
                "type": "input",
                "name": "longdescription",
                "message": f"Please provide a longer description:",
                "validate": lambda x: True,
            }
        ]
    )

    issuesclosed = prompt(
        [
            {
                "type": "input",
                "name": "issuesclosed",
                "message": f"List any closed issues:",
                "validate": lambda x: True,
            }
        ]
    )

    # Signing
    signedby = prompt(
        [
            {
                "type": "input",
                "name": "signedby",
                "message": f"Signed off username:",
                "validate": validate_required_input,
            }
        ]
    )

    signedbyemail = prompt(
        [
            {
                "type": "input",
                "name": "signedbyemail",
                "message": f"Signed off email:",
                "validate": validate_required_input,
            }
        ]
    )

    confirmed_details = prompt(
        [
            {
                "type": "confirm",
                "name": "confirm_details",
                "message": "Confirm the details above",
                "default": True,
            }
        ]
    )
    if issuesclosed.get("issuesclosed"):
        issuesclosed = f"Closes: {issuesclosed['issuesclosed']}"
    else:
        issuesclosed = ""
    if confirmed_details["confirm_details"]:
        print("Commit details confirmed! Commit initiated.")
        if add:
            print("Adding changes.")
            os.system(f"git add .")
        os.system(f'git checkout -b {configuration['branch']}')
        os.system(
            f"""git commit -m "{answers['change_type']} {description['description']}" -m "{longdescription['longdescription']}\n{issuesclosed}\n\nSigned-off-by: {signedby['signedby']} <{signedbyemail['signedbyemail']}>" """
        )
        if push:
            print("Pushing changes.")
            os.system("git push")


if __name__ == "__main__":
    main()
