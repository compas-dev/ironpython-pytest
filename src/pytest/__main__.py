from __future__ import print_function

import argparse
import os

from .test_runner import run


def main():
    parser = argparse.ArgumentParser(description='IronPython pytest runner.')
    parser.add_argument('file_or_dir', type=str, help='Directory or file to test', default=os.path.dirname(__file__))
    parser.add_argument('--ignore', type=str, action='append',
                        help='Ignore files during testing (multiple allowed)')

    args = parser.parse_args()

    run(args.file_or_dir, exclude_list=args.ignore, capture_stdout=True)


if __name__ == '__main__':
    main()
