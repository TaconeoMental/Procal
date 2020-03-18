from prettytable import PrettyTable
import itertools

def bin_to_bool(int):
    return ['F', 'T'][int]

class TruthTable:
    def __init__(self, ast, st, nfields):
        self.ast = ast
        self.sym_t = st
        self.table = PrettyTable()
        
        fields = list()
        for sym in self.sym_t.symbols:
            fields.append(sym)

        f = self.ast.infix_list_until(nfields)
   
        for i in f:
            fields.append(i.infix_str())
        
        self.table.field_names = fields
        
        bin_list = list(map(list, itertools.product([0, 1], repeat = self.sym_t.number_sym)))
        env = dict()
        for perm in bin_list:
            for val, sym in zip(perm, self.sym_t.symbols):
                env[sym] = val
            for ast_slice in f:
                perm.append(ast_slice.eval(env))
            self.table.add_row([bin_to_bool(n) for n in perm])
              
    def show(self):
        print(self.table)