import argparse # command line inputs
import json # for i/o



__author__ = "Alexander Reynolds"
__email__ = "ar@reynoldsalexander.com"



"""Command line parsing"""



if __name__ == "__main__":
    """To be ran from command line
    Usage: python3 testIO.py jsonString
    Example: python3 testIO.py '{"name":"groot","occupation":"tree"}'
    """

    parser = argparse.ArgumentParser(description='Tests json I/O')

    parser.add_argument('jsonIn',
        help='JSON dict to be outputted')

    args = parser.parse_args()

    # grab inputs from json
    jsonIn = json.loads(args.jsonIn)

    # print json inputs
    print(json.dumps(jsonIn))
