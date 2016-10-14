import argparse
import sys

import config

import aoj

def aojack():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    parser_submit = subparsers.add_parser('submit', help = "submit to AOJ")
    parser_submit.add_argument('path', type = str, help = "path to the source code")
    parser_submit.add_argument('problemNO', type = str, help = "problemNO to submit to ")
    parser_submit.add_argument('-l', '--lessonID', type = str, default = "", help = "lessonID to submit to ")
    parser_submit.add_argument('--liveoff', action = "store_true", default = False, help = "set if you don't need live status after submitting")
    parser_submit.set_defaults(func = 'submit_file')

    args = parser.parse_args(sys.argv[1:])

    aoj_session = aoj.AOJ(config.USERID, config.PASSWORD)

    sys.exit(0)

    if args.func == 'submit_file':
        aoj_session.submit_file(args.path, args.problemNO, args.lessonID, not args.liveoff)


if __name__ == "__main__":
    aojack()
