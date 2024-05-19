#!/usr/bin/python3

import os.path
import subprocess
from datetime import datetime
import logging
import argparse
import sys

logger = logging.getLogger(__name__)


def calculate_diff(before_file: str, after_file: str, diff_file: str) -> subprocess.CompletedProcess:
    """
    Function calculates the diff between two files and stores it in a third diff file.

    Note:
        Using subprocess with shell=True is prone to shell injection.
        Subprocess command needs to be rewritten, so it does not use the shell to avoid injection.

    Args:
        before_file: The original file before the patch.
        after_file:  A patched version of the file.
        diff_file: File in which the difference will be stored.

    Returns:
        result: Return from subprocess call.
    """
    # Construct the command to run diff
    command = f'diff -u {before_file} {after_file} > {diff_file}'

    # Execute the command using subprocess
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)

    # Log output of subprocess if not empty
    if result.stdout != "":
        logger.info(result.stdout)

    # Check if command executed successfully based on return code
    if result.returncode > 1:
        logger.error(f"Diff command failed with exit code: {result.returncode}")
        sys.exit(1)

    logger.info(f"Diff executed successfully!")
    logger.info(f"Diff between files stored at: {diff_file}")

    return result


def apply_patch(target_file: str, diff_file: str) -> subprocess.CompletedProcess:
    """
    Function applies patch from diff file to target file.

    Note:
        Using subprocess with shell=True is prone to shell injection.
        Subprocess command needs to be rewritten, so it does not use the shell to avoid injection.

    Args:
        target_file: File to which to apply the patch to.
        diff_file:  Diff file containing the patch.

    Returns:
        result: Return from subprocess call.
    """
    # Construct the command to run patch
    command = f'patch  {target_file} < {diff_file}'

    # Execute the command using subprocess
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)

    # Log output of subprocess if not empty
    if result.stdout != "":
        logger.info(result.stdout)

    # Check if command executed successfully based on return code
    if result.returncode > 1:
        logger.error(f"Patch command failed with exit code: {result.returncode}")
        sys.exit(1)

    return result


if __name__ == "__main__":

    # Initialize parser
    parser = argparse.ArgumentParser(description='Process input arguments.')

    # Adding argument
    parser.add_argument('-b', '--before', required=True, help='Location of file before the patch')
    parser.add_argument('-a', '--after', required=True, help='Location of file after the patch')
    parser.add_argument('-t', '--target', required=True, help='Location of file to which to apply the patch')
    parser.add_argument('-d', '--diff', required=False, help='Directory where the diff file will be stored',
                        default='/tmp/')
    parser.add_argument('-l', '--log-dir', required=False, help='Directory where the log file will be stored',
                        default='/tmp/')

    # Read arguments from command line
    args = parser.parse_args()

    # Define log file name using current time
    log_filename = os.path.join(args.log_dir, datetime.now().strftime('backporting_tool_%H_%M_%S_date_%d_%m_%Y.log'))

    # Setup logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler(log_filename), logging.StreamHandler(sys.stdout)])

    logger.info(f"Log file for current run stored at: {log_filename}")

    # Define diff file name using current time
    diff_filename = os.path.join(args.diff, datetime.now().strftime('backporting_tool_%H_%M_%S_date_%d_%m_%Y.diff'))

    # Find the diff between two files
    calculate_diff(args.before, args.after, diff_filename)

    # Apply the diff as a patch to a third file
    apply_patch(args.target, diff_filename)



