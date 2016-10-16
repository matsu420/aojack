#!/usr/bin/env python

import argparse
import sys
import traceback

from aojack import aoj
from aojack import config

def aojack():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    parser_submit = subparsers.add_parser('submit', help = "submit to AOJ")
    parser_submit.add_argument('path', type = str, help = "path to the source code")
    parser_submit.add_argument('problemNO', type = str, help = "problemNO to submit to ")
    parser_submit.add_argument('-l', '--lessonID', type = str, default = "", help = "lessonID to submit to ")
    parser_submit.add_argument('--liveoff', action = "store_true", default = False, help = "set if you don't need live status after submitting")
    parser_submit.set_defaults(func = 'submit_file')


    parser_getin = subparsers.add_parser('getin', help = "get judge input")
    parser_getin.add_argument('runID', type = str, help = "runID to get judge input")
    parser_getin.add_argument('-c', '--case', type = str, default = "1", help = "case no of test case")
    parser_getin.set_defaults(func = 'getin')

    parser_getout = subparsers.add_parser('getout', help = "get judge output")
    parser_getout.add_argument('runID', type = str, help = "runID to get judge input")
    parser_getout.add_argument('-c', '--case', type = str, default = "1", help = "case no of test case")
    parser_getout.set_defaults(func = 'getout')

    parser_getboth = subparsers.add_parser('getboth', help = "get both judge input and output")
    parser_getboth.add_argument('runID', type = str, help = "runID to get judge input")
    parser_getboth.add_argument('-c', '--case', type = str, default = "1", help = "case no of test case")
    parser_getboth.set_defaults(func = 'getboth')


    args = parser.parse_args(sys.argv[1:])

    aoj_session = aoj.AOJ(config.USERID, config.PASSWORD)

    try:

        if args.func == 'submit_file':
            aoj_session.submit_file(args.path, args.problemNO, args.lessonID, not args.liveoff)
        elif args.func == 'getin':
            aoj_session.get_file(args.runID, args.case, True, False)
        elif args.func == 'getout':
            aoj_session.get_file(args.runID, args.case, False, True)
        elif args.func == 'getboth':
            aoj_session.get_file(args.runID, args.case, True, True)
    except:
        print traceback.format_exc()


if __name__ == "__main__":
    aojack()
