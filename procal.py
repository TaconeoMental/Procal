import argparse
from src.tokenizer import Tokenizer

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("prop", help="Propositional statement")
    arg_parser.add_argument("--tokens", "-t", action='store_true')
    args = arg_parser.parse_args()
    
    tokenizer = Tokenizer(args.prop)
    
    if args.tokens:
        tokenizer.show_tokens()

if __name__ == '__main__':
    main()
