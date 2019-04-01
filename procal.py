import argparse

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("prop", help="Propositional statement")
    args = arg_parser.parse_args()

if __name__ == '__main__':
    main()
