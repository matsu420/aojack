import argparse
import sys

import aoj

def aojack():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    parser_submit = subparsers.add_parser('submit')
    parser_submit.add_argument('path', type = str)
    parser_submit.add_argument('problemNO', type = str)
    parser_submit.add_argument('-l', '--lessonID', type = str, default = "")
    parser_submit.add_argument('--liveoff', action = "store_true", default = False)
    parser_submit.set_defaults(func = 'submit_file')

    args = parser.parse_args(sys.argv[1:])

    print args

    aoj_session = aoj.AOJ('userID', 'password')

    sys.exit(0)

    if args.func == 'submit_file':
        aoj_session.submit_file(args.path, args.problemNO, args.lessonID, not args.liveoff)


if __name__ == "__main__":
    aojack()
