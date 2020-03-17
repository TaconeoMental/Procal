#!/usr/bin/env python3

import argparse
from src.tokenizer import Tokenizer
from src.parser import Parser
from src.error_collector import ErrorCollector
from src.symbol_table import SymbolTable
from src.truth_table import TruthTable


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("prop", help="Propositional statement")
    arg_parser.add_argument("--tokens", "-t", action="store_true")
    arg_parser.add_argument("--ast", "-a", action="store_true")
    arg_parser.add_argument("--symbols", "-s", action="store_true")
    arg_parser.add_argument("--truthtable", "-tt", nargs='?', const=1, type=int)
    args = arg_parser.parse_args()

    if not args.prop:
        args.prop = " "

    error_collector = ErrorCollector(args.prop)
    symbol_table = SymbolTable()

    tokenizer = Tokenizer(error_collector, symbol_table)

    parser = Parser(tokenizer, error_collector)
    ast = parser.parse()
    
    # Para hacer debug jeje
    if args.symbols:
        symbol_table.show_symbols()

    if error_collector.has_errors():
        error_collector.show_errors()
        return

    if args.tokens:
        tokenizer.show_tokens()

    if args.ast:
        print(ast)
        
    if args.truthtable:
        tt = TruthTable(ast, symbol_table, args.truthtable)
        tt.show()


if __name__ == '__main__':
    main()
