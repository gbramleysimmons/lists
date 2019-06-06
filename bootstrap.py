import json
import os
import sys
import subprocess
from optparse import OptionParser


usage = """usage: %prog [options]"""
parser = OptionParser(usage=usage)


def exit_in_error(msg, show_usage=False):
    sys.stderr.write("Error: {}\n".format(msg))

    if show_usage:
        parser.print_usage()

    sys.exit(-1)


def execute(project_root_dir):
    if "VIRTUAL_ENV" not in os.environ:
        exit_in_error("$VIRTUAL_ENV not found.\n\n", show_usage=True)

    virtualenv = os.environ["VIRTUAL_ENV"]

    requirements_files = list(filter(os.path.exists, [os.path.join(project_root_dir, "conf/requirements.txt"), os.path.join(project_root_dir, "conf/test_requirements.txt")]))

    if not requirements_files:
        exit_in_error("Couldn't find suitable requirements file")
    pip_args = ["pip", "install", "--requirement", requirements_files[0]]
    print("Installing python libs")
    retval = subprocess.call(pip_args)
    if retval:
        exit_in_error('Pip failed to install one more libs. See error(s) above.')


if __name__ == "__main__":
    execute(os.path.dirname(__file__))
    sys.exit()
