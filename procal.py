#!/usr/bin/env python3

import argparse
from src.tokenizer import Tokenizer
from src.parser import Parser
from src.error_collector import ErrorCollector

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("prop", help="Propositional statement")
    arg_parser.add_argument("--tokens", "-t", action="store_true")
    arg_parser.add_argument("--ast", "-a", action="store_true")
    args = arg_parser.parse_args()
    
    if not args.prop:
        args.prop = " "
    
    error_collector = ErrorCollector(args.prop)

    tokenizer = Tokenizer(error_collector)

    parser = Parser(tokenizer, error_collector)
    ast = parser.parse()

    if error_collector.has_errors():
        error_collector.show_errors()
        return

    if args.tokens:
        tokenizer.show_tokens()

    if args.ast:
        print(ast)

if __name__ == '__main__':
    main()
