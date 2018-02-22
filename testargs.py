import argparse

def main(args):
    print("main stuff")
    if args.a:
        print("a is true")
    if args.d:
        print("d is true")

parser = argparse.ArgumentParser()
parser.add_argument("-d",
                    default=False,
                    action='store_true',
                    help="")
parser.add_argument("-a",
                    default=False,
                    action='store_true',
                    help="")
args = parser.parse_args()
main(args)
