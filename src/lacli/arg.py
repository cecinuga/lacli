import os
import argparse

def get_argparse():
    parser = argparse.ArgumentParser(
        prog='lacli',
        description='linear algebra in your console',
        suggest_on_error=True
    )
    parser.add_argument('-f', '--file', help='the file to load, relative path', type=str, required=True)
    parser.add_argument('-b', action='store_true', help='enable simple benchmark, from start to end the job', default=False)

    return parser
