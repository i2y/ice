import warnings
from collections import Sequence

import rply
from rply import ParserGenerator

from ice import __version__
from . import lexer


name_seq = 0


def get_temp_name():
    global name_seq
    name_seq += 1
    name_symbol = Symbol('_gs%s' % name_seq)
    return name_symbol


class ParsingError(Exception):
    def __init__(self, file_path, lineno=1, colno=1):
        self.file_path = file_path
        self.lineno = lineno
        self.colno = colno

    def __str__(self):
        return 'ParsingError: file=' \
               + self.file_path\
               + ' lineno='\
               + str(self.lineno)\
               + ' colno='\
               + str(self.colno)


def parse(lexer, filename="<string>"):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            return pg.build().parse(lexer)
    except rply.errors.ParsingError as e:
        source_pos = e.getsourcepos()
        if source_pos is None:
            raise ParsingError(filename)
        else:
            raise ParsingError(filename,
                               source_pos.lineno,
                               source_pos.colno)


class Symbol(object):
    def __init__(self, name, lineno=0, col_offset=0):
        self.name = name
        self.outer_name = name
        self.lineno = lineno
        self.col_offset = col_offset

    def eval(self, env):
        pass

    def __repr__(self):
        return self.outer_name

    def __str__(self):
        return self.outer_name

    def __eq__(self, other):
        if type(other) is not Symbol:
            return False
        if self.name == other.name:
            return True
        else:
            return False

    def __hash__(self):
        return (self.name.__hash__() << 16) + self.outer_name.__hash__()


class Keyword(object):
    def __init__(self, name, lineno=0, col_offset=0):
        self.name = name
        self.lineno = lineno
        self.col_offset = col_offset
        self.repr = ':' + self.name

    def __repr__(self):
        return self.repr

    def __str__(self):
        return self.name

    def __call__(self, table):
        return table[self.name]

    def __eq__(self, other):
        if type(other) is not Keyword:
            return False
        if self.name == other.name:
            return True
        else:
            return False

    def __hash__(self):
        return self.name.__hash__()


pg = ParserGenerator(['NUMBER', 'OPPLUS', 'OPMINUS', 'OPTIMES', 'OPDIV', 'OPLEQ', 'OPGEQ', 'OPEQ', 'OPNEQ',
                      'OPLT', 'OPGT', 'OPBITOR', 'OPPOW', 'MACRO_NAME', 'LET',  # 'UNION', 'PREDICATE',
                      'INFIX_MACRO_NAME', 'INFIX_1_MACRO_NAME', 'INFIX_2_MACRO_NAME', 'INFIX', 'INFIX_1', 'INFIX_2',
                      'OPRSHIFT', 'OPLSHIFT', 'OPFLOORDIV', 'OPBITAND', 'OPBITXOR', 'USER_DEFINED_KEYWORD',
                      'OPAND', 'OPOR', 'OPIS', 'NOT', 'PERCENT', 'EXPORT', 'ASSERT',
                      'LPAREN', 'RPAREN', 'TRUE', 'FALSE', 'TQUOTE_STR', 'DQUOTE_STR', 'SQUOTE_STR', 'NAME_LPAREN',
                      'AT', 'DOT_NAME', 'DOT_NAME_LPAREN', 'TQUOTE_RAW_STR', 'DQUOTE_RAW_STR', 'SQUOTE_RAW_STR',
                      'NAME', 'EQUALS', 'IF', 'ELSEIF', 'ELSE', 'COLON', 'SEMI', 'DATA', 'IMPORT', 'INCLUDE',
                      'LBRACK', 'RBRACK', 'COMMA', 'FUNC', 'DOC', 'CALET', 'PIPELINE', 'PIPELINE_BIND',
                      'PIPELINE_FIRST', 'PIPELINE_FIRST_BIND', 'RETURN', 'CALL', 'DO',
                      'LBRACE', 'RBRACE', 'MATCH', 'CASE', 'DEFM', 'RECORD', 'AMP', 'FATARROW', 'THINARROW',
                      'YIELD', 'FROM', 'USE', 'FOR', 'IN', 'TRY', 'FINALLY', 'EXCEPT',
                      'AS', 'RAISE', 'WITH', 'MACRO', 'QUOTE', 'QUASI_QUOTE', 'UNQUOTE', 'UNQUOTE_SPLICING',
                      'QUOTE_LPAREN', 'QUASI_QUOTE_LPAREN', 'UNQUOTE_LPAREN', 'UNQUOTE_SPLICING_LPAREN'],
                     precedence=[('left', ['EQUALS']),
                                 ('left', ['NOT']),
                                 ('left', ['OPIS']),
                                 ('left', ['IN']),
                                 ('left', ['AS', 'OPEQ', 'OPLEQ', 'OPGEQ', 'OPNEQ', 'OPLT', 'OPGT', 'OPAND', 'OPOR',
                                           'PIPELINE', 'PIPELINE_BIND', 'PIPELINE_FIRST', 'PIPELINE_FIRST_BIND',
                                           'INFIX_MACRO_NAME']),
                                 ('left', ['OPPLUS', 'OPMINUS', 'INFIX_1_MACRO_NAME']),
                                 ('left', ['LBRACK', 'RBRACK']),
                                 ('left', ['OPTIMES', 'OPDIV', 'OPFLOORDIV', 'PERCENT', 'OPBITAND', 'OPBITOR',
                                           'OPBITXOR', 'OPPOW', 'OPRSHIFT', 'OPLSHIFT', 'INFIX_2_MACRO_NAME']),
                                 ('left', ['IF'])],
                     cache_id='ice_' + __version__)


@pg.production('program : block')
def program(p):
    return p[0]


@pg.production('block : stmts')
def block(p):
    return p[0]


@pg.production('stmts : stmts stmt')
def stmts_b(p):
    if p[1] is None:
        return p[0]
    else:
        return p[0] + [p[1]]


@pg.production('stmts : stmt')
def stmts_stmt(p):
    if p[0] is None:
        return []
    else:
        return [p[0]]


@pg.production('stmt : SEMI')
def stmt_semi(p):
    pass

@pg.production('stmt : binop_expr')
@pg.production('stmt : let_expr')
@pg.production('stmt : as_expr')
@pg.production('stmt : deco_expr')
@pg.production('stmt : func_expr')
@pg.production('stmt : funcm_expr')
# @pg.production('stmt : record_expr')
@pg.production('stmt : data_expr')
@pg.production('stmt : import_expr')
@pg.production('stmt : from_expr')
@pg.production('stmt : macros_stmt')
@pg.production('stmt : try_stmt')
@pg.production('stmt : with_stmt')
@pg.production('stmt : raise_stmt')
@pg.production('stmt : return_stmt')
@pg.production('stmt : macro_stmt')
@pg.production('stmt : infix_macro_stmt')
@pg.production('stmt : q_stmt')
@pg.production('stmt : qq_stmt')
@pg.production('stmt : assert_stmt')
def stmt(p):
    return p[0]

# # TODO fukkatu?
# @pg.production('call_macro_stmt : id_expr COLON do_suite')
# def call_macro_stmt(p):
#     head = []
#     body = p[2]
#     rest = []
#     return process_calling_macro(p[0], head, body, rest)


# @pg.production('call_macro_stmt : id_expr COLON do_suite rest')
# def call_macro_expr(p):
#     head = []
#     body = p[2]
#     rest = p[3]
#     return process_calling_macro(p[0], head, body, rest)


@pg.production('import_expr : IMPORT names_list')
def import_expr(p):
    return [Symbol('import')] + p[1]


@pg.production('names_list : names_list COMMA names')
def names(p):
    return p[0] + [p[2]]


@pg.production('names_list : names')
def names_single(p):
    return [p[0]]


@pg.production('names : _names')
def names(p):
    return Symbol('.'.join(p[0]))


@pg.production('_names : NAME')
def _names_one(p):
    return [p[0].getstr()]


@pg.production('_names : _names DOT_NAME')
def _names(p):
    return p[0] + [p[1].getstr()[1:]]


@pg.production('names_lparen : _names_lparen')
def names(p):
    return Symbol('.'.join(p[0]))


@pg.production('_names_lparen : NAME_LPAREN')
def _names_one(p):
    return [p[0].getstr()[:-1]]


@pg.production('_names_lparen : _names DOT_NAME_LPAREN')
def _names(p):
    return p[0] + [p[1].getstr()[1:-1]]


# @pg.production('include_expr : INCLUDE string')
# def include_expr(p):
#     return [Symbol('require'), p[1]]


@pg.production('lbrace : LBRACE')
def lbrace(p):
    pass


@pg.production('rbrace : RBRACE')
def rbrace(p):
    pass


@pg.production('namelist : namelist COMMA name')
def names(p):
    return p[0] + [p[2]]


@pg.production('namelist : name')
def names_single(p):
    return [p[0]]


@pg.production('name : NAME')
def name(p):
    return token_to_symbol(p[0])


@pg.production('tuple_elt : binop_expr COMMA')
def tuple_elt(p):
    return p[0]


@pg.production('from_expr : FROM names IMPORT namelist')
def from_expr(p):
    return [Symbol('from_import'), p[1], p[3]]


@pg.production('macros_stmt : USE lbrace use_expr_list rbrace')
def macros_stmt(p):
    return [Symbol('do')] + p[2]


@pg.production('use_expr_list : use_expr')
def macros_stmt(p):
    return [p[0]]


@pg.production('use_expr_list : use_expr_list use_expr')
def macros_stmt(p):
    return p[0] + p[1]


@pg.production('use_expr : namelist FROM names')
def use_expr(p):
    filename = p[1].filename
    module_name = p[2].name
    import importlib
    mod = importlib.import_module(module_name)
    if hasattr(mod, 'get_keywords'):
        keywords = mod.get_keywords()
    else:
        keywords = {}
    for macro_name in p[0]:
        macro_name_str = str(macro_name)
        lexer.add_macro_name((filename, macro_name_str))
        if macro_name_str in keywords:
            for user_defined_keyword in keywords[macro_name_str]:
                print(user_defined_keyword)
                lexer.add_user_defined_keyword((filename, user_defined_keyword))
     #   else:
     #       raise SyntaxError(macro_name_str)

    return [Symbol('use'), p[0], p[2]]


#@pg.production('use_infix_expr : USE INFIX namelist FROM names')
#def use_expr(p):
#    for macro_name in p[1]:
#        lexer.add_infix_macro_name(str(macro_name))
#    return [Symbol('use'), p[1], p[3]]


@pg.production('suite : binop_expr')
def suite_expr(p):
    return p[0]


@pg.production('suite : lbrace stmts rbrace')
def suite_stmts(p):
    return [Symbol('do')] + p[1]


# @pg.production('suite : NEWLINE INDENT stmts DEDENT END')
# def suite_stmts(p):
#     return [Symbol('do')] + p[2]


@pg.production('suite2 : lbrace stmts rbrace')
def suite2_stmts(p):
    return p[1]


# @pg.production('suite2 : NEWLINE INDENT stmts DEDENT END')
# def suite2_stmts(p):
#     return p[2]


@pg.production('try_stmt : TRY suite2 finally_cls')
def try_finally_stmt(p):
    return [Symbol('try')] + p[1] + [p[2]]


@pg.production('try_stmt : TRY suite2 except_cls_list')
def try_except_stmt(p):
    return [Symbol('try')] + p[1] + p[2]


@pg.production('try_stmt : TRY suite2 except_cls_list finally_cls')
def try_excepts_finally_stmt(p):
    return [Symbol('try')] + p[1] + p[2] + [p[3]]


@pg.production('except_cls_list : except_cls_list except_cls')
def except_cls_list(p):
    return p[0] + [p[1]]


@pg.production('except_cls_list : except_cls')
def except_cls_list(p):
    return [p[0]]


@pg.production('except_cls : EXCEPT binop_expr AS NAME suite2')
def except_cls(p):
    return [Symbol('except'), p[1], token_to_symbol(p[3])] + p[4]


@pg.production('finally_cls : FINALLY suite2')
def finally_cls(p):
    return [Symbol('finally')] + p[1]


@pg.production('raise_stmt : RAISE binop_expr')
def raise_stmt(p):
    return [Symbol('raise'), p[1]]


#@pg.production('do_suite : binop_expr')
#def suite_expr(p):
#    return [Symbol('do'), p[0]]


@pg.production('do_suite : lbrace stmts rbrace')
def suite_stmts(p):
    return [Symbol('do')] + p[1]


# @pg.production('do_suite : NEWLINE INDENT stmts DEDENT END')
# def suite_stmts(p):
#     return [Symbol('do')] + p[2]


#@pg.production('labeled_expr : binop_expr COLON binop_expr')
#def labeled_expr(p):
#    # return [Symbol('label'), p[0], p[2]]
#    return [Symbol('call_macro'), p[0], [], [Symbol('do'), p[2]], []]

class Label:
    def __init__(self, label):
        self.label = label


# @pg.production('labeled_expr : binop_expr do_suite')
# def labeled_expr(p):
#     name = Label(p[0])
#     head = []
#     body = p[1]
#     rest = None
#     return [Symbol('call_macro'), name, [head, body, rest]]


#@pg.production('cont_labeled_expr : id_expr COLON do_suite')
#def labeled_expr(p):
#    name = p[0]
#    head = []
#    body = p[2]
#    rest = None
#    return [Symbol('call_macro'), name, [head, body, rest]]


#@pg.production('cont_labeled_expr : id_expr COLON do_suite cont_labeled_expr')
#def labeled_expr(p):
#    name = p[0]
#    head = []
#    body = p[2]
#    rest = p[3][1:]
#    return [Symbol('call_macro'), name, [head, body, rest]]


#@pg.production('labeled_expr : binop_expr COLON do_suite cont_labeled_expr')
#def labeled_expr(p):
#    name = p[0]
#    head = []
#    body = p[2]
#    rest = p[3][1:]
#    return [Symbol('call_macro'), name, [head, body, rest]]


# @pg.production('labeled_expr : binop_expr do_suite labeled_expr')
# def labeled_expr(p):
#     name = Label(p[0])
#     head = []
#     body = p[1]
#     rest = p[2][1:]
#     return [Symbol('call_macro'), name, [head, body, rest]]


# @pg.production('labeled_expr : binop_expr do_suite call_macro_expr')
# def labeled_expr(p):
#     name = Label(p[0])
#     head = []
#     body = p[1]
#     rest = p[2][1:]
#     return [Symbol('call_macro'), name, [head, body, rest]]


# @pg.production('user_defined_stmt : NAME NAME COLON trailing_dict')
# def user_defined_stmt(p):
#     return [Symbol('val'),
#             token_to_symbol(p[1]),
#            [Symbol(p[0].getstr() + '.define'), p[1].getstr(), p[3]]]


# @pg.production('user_defined_stmt : NAME id_expr app_args COLON trailing_dict')
# def user_defined_stmt(p):
#     return [Symbol(p[0].getstr() + '.define'), p[1]] + p[2] + [p[4]]


# @pg.production('user_defined_stmt : NAME NAME DOT_NAME app_args COLON trailing_dict')
# def user_defined_stmt(p):
#     return [Symbol(p[0].getstr() + '.define'), Symbol(p[1].getstr() + '.' + p[2].getstr()[1:])] + p[3] + [p[5]]


@pg.production('macro_stmt : MACRO fun_header suite2')
def macro_stmt(p):
    fun_name, fun_args = p[1]
    lexer.add_macro_name((p[0].filename, str(fun_name)))
    return [Symbol('mac'), fun_name, fun_args] + p[2]


@pg.production('infix_macro_stmt : INFIX MACRO fun_header suite2')
def macro_stmt(p):
    fun_name, fun_args = p[2]
    lexer.add_infix_macro_name((p[0].filename, str(fun_name)))
    return [Symbol('mac'), fun_name, fun_args] + p[3]


@pg.production('infix_macro_stmt : INFIX_1 MACRO fun_header suite2')
def macro_stmt(p):
    fun_name, fun_args = p[2]
    lexer.add_infix_1_macro_name((p[0].filename, str(fun_name)))
    return [Symbol('mac'), fun_name, fun_args] + p[3]


@pg.production('infix_macro_stmt : INFIX_2 MACRO fun_header suite2')
def macro_stmt(p):
    fun_name, fun_args = p[2]
    lexer.add_infix_2_macro_name((p[0].filename, str(fun_name)))
    return [Symbol('mac'), fun_name, fun_args] + p[3]


@pg.production('q_stmt : QUOTE suite')
def q_stmt(p):
    return [Symbol('quote'), p[1]]


#@pg.production('quote_expr : QUOTE_LPAREN binop_expr RPAREN')
#@pg.production('quote_expr : QUOTE binop_expr')
@pg.production('quote_expr : QUOTE stmt')
def quote_expr(p):
    return [Symbol('quote'), p[1]]


@pg.production('qq_stmt : QUASI_QUOTE suite')
def qq_stmt(p):
    return [Symbol('quasiquote'), p[1]]


#@pg.production('quasi_quote_expr : QUASI_QUOTE_LPAREN binop_expr RPAREN')
#@pg.production('quasi_quote_expr : QUASI_QUOTE binop_expr')
@pg.production('quasi_quote_expr : QUASI_QUOTE stmt')
def quasi_quote_expr(p):
    return [Symbol('quasiquote'), p[1]]


#@pg.production('uq_expr : UNQUOTE_LPAREN binop_expr RPAREN')
@pg.production('uq_expr : UNQUOTE binop_expr')
def uq_expr(p):
    return [Symbol('unquote'), p[1]]


#@pg.production('uqs_expr : UNQUOTE_SPLICING_LPAREN binop_expr RPAREN')
@pg.production('uqs_expr : UNQUOTE_SPLICING binop_expr')
def uqs_expr(p):
    return [Symbol('unquote_splicing'), p[1]]


@pg.production('assert_stmt : ASSERT binop_expr')
def assert_stmt(p):
    return [Symbol('assert'), p[1]]


@pg.production('with_stmt : WITH with_contexts suite2')
def with_stmt(p):
    return [Symbol('with'), p[1]] + p[2]


@pg.production('with_contexts : with_contexts COMMA with_context')
def with_contexts(p):
    return p[0] + [p[2]]


@pg.production('with_contexts : with_context')
def with_contexts_one(p):
    return [p[0]]


@pg.production('with_context : binop_expr AS NAME')
def with_context(p):
    return [p[0], token_to_symbol(p[2])]


@pg.production('return_stmt : RETURN binop_expr')
def raise_stmt(p):
    return [Symbol('return'), p[1]]


def token_to_symbol(token):
    return Symbol(token.getstr(), token.getsourcepos().lineno, token.getsourcepos().colno)


def token_to_keyword(token):
    return Keyword(token.getstr(), token.getsourcepos().lineno, token.getsourcepos().colno)


@pg.production('let_expr : LET pattern EQUALS binop_expr')
def let_expr(p):
    return [Symbol('match'), p[3], p[1], Symbol('True')]


@pg.production('binding : NAME')
def binding(p):
    return token_to_symbol(p[0])


@pg.production('as_expr : binop_expr AS id_expr')
def let_expr(p):
    return [Symbol('val', 0, 0), p[2], p[0]]


@pg.production('expr : record_expr')
# @pg.production('expr : func_expr')
# @pg.production('expr : union_expr')
# @pg.production('expr : predicate_expr')
@pg.production('expr : fn_expr')
@pg.production('expr : paren_expr')
@pg.production('expr : if_expr')
@pg.production('expr : prim_expr')
@pg.production('expr : uq_expr')
@pg.production('expr : uqs_expr')
@pg.production('expr : app_expr')
@pg.production('expr : left_app_expr')
@pg.production('expr : dict_expr')
@pg.production('expr : tuple_expr')
@pg.production('expr : match_expr')
@pg.production('expr : yield_expr')
@pg.production('expr : yield_from_expr')
@pg.production('expr : for_expr')
@pg.production('expr : block_expr')
@pg.production('expr : dot_expr')
@pg.production('expr : get_expr')
@pg.production('expr : quote_expr')
@pg.production('expr : quasi_quote_expr')
@pg.production('expr : id_expr')
@pg.production('expr : call_macro_expr')
@pg.production('expr : call_func_expr')
@pg.production('expr : call_method_expr')
def expr(p):
    return p[0]


@pg.production('paren_expr : LPAREN binop_expr RPAREN')
def paren_expr(p):
    return p[1]


@pg.production('prim_expr : NUMBER')
def expr_num(p):
    num_repr = p[0].getstr()
    try:
        return int(num_repr)
    except ValueError as _:
        return float(num_repr)


@pg.production('prim_expr : string')
def expr_string(p):
    return p[0]


@pg.production('string : DQUOTE_STR')
@pg.production('string : SQUOTE_STR')
def expr_quote_str(p):
    return quote_str(p[0].getstr()[1:-1])


@pg.production('string : TQUOTE_STR')
def expr_triple_quote_str(p):
    return quote_str(p[0].getstr()[3:-3])


def quote_str(string):
    new_string = ''
    string_enumerator = enumerate(string)
    for index, char in string_enumerator:
        if char == '\\':
            index, char = next(string_enumerator)
            if char == 'n':
                char = '\n'
            elif char == 't':
                char = '\t'
            elif char == 'r':
                char = '\r'
            elif char in {'\\', "'", '"'}:
                pass
            else:
                char = '\\' + char
        new_string = new_string + char
    return new_string


@pg.production('string : DQUOTE_RAW_STR')
@pg.production('string : SQUOTE_RAW_STR')
def expr_quote_raw_str(p):
    return p[0].getstr()[2:-1]


@pg.production('string : TQUOTE_RAW_STR')
def expr_triple_quote_raw_str(p):
    return p[0].getstr()[4:-3]


@pg.production('prim_expr : bool_expr')
def expr_false(p):
    return p[0]


@pg.production('bool_expr : TRUE')
def expr_true(p):
    return Symbol('True')


@pg.production('bool_expr : FALSE')
def expr_false(p):
    return Symbol('False')


@pg.production('id_expr : NAME')
def id_expr(p):
    return token_to_symbol(p[0])


@pg.production('id_expr : AMP')
def id_expr(p):
    return Symbol('&')


@pg.production('if_expr : IF binop_expr suite elseif_exprs ELSE suite')
def if_else_expr(p):
    return [Symbol('if'), p[1], p[2]] + p[3] + [p[5]]


@pg.production('if_expr : IF binop_expr suite ELSE suite')
def if_else_expr(p):
    return [Symbol('if'), p[1], p[2], p[4]]


@pg.production('elseif_exprs : elseif_exprs elseif_expr')
def elseif_exprs(p):
    return p[0] + p[1]


@pg.production('elseif_exprs : elseif_expr')
def elseif_exprs_expr(p):
    return p[0]


@pg.production('elseif_expr : ELSEIF binop_expr suite')
def elseif_expr(p):
    return [p[1], p[2]]


# @pg.production('elseif_expr :')
# def elseif_expr_empty(p):
#     return None


#@pg.production('trailing_if_expr : binop_expr IF binop_expr ELSE binop_expr')
def trailing_if_expr(p):
    return [Symbol('if'), p[2], p[0], p[4]]


@pg.production('yield_expr : YIELD binop_expr')
def yield_expr(p):
    return [Symbol('yield'), p[1]]


@pg.production('yield_from_expr : YIELD FROM binop_expr')
def yield_from_expr(p):
    return [Symbol('yield_from'), p[1]]


def issequence(obj):
    return isinstance(obj, Sequence)


def issequence_except_str(obj):
    if isinstance(obj, str):
        return False
    return isinstance(obj, Sequence)


def _compute_underscore_max_num(exps):
    max_num = 0

    if not issequence_except_str(exps):
        exps = (exps,)

    for exp in exps:
        if isinstance(exp, Symbol) and exp.name.startswith('$'):
            try:
                n = int(exp.name[1:])
            except:
                n = 1
        elif issequence_except_str(exp):
            n = _compute_underscore_max_num(exp)
        else:
            n = 0

        if n > max_num:
            max_num = n
    return max_num


@pg.production('dot_expr : expr DOT_NAME')
def dot_expr(p):
    return [Symbol('getattr'), p[0], p[1].getstr()[1:]]


@pg.production('get_expr : binop_expr LBRACK binop_expr RBRACK')
def get_expr(p):
    return [Symbol('get'), p[0], p[2]]


@pg.production('get_expr : binop_expr LBRACK binop_expr COMMA binop_expr RBRACK')
def get_expr(p):
    return [Symbol('get'), p[0], [Symbol('v'), p[2], p[4]]]


@pg.production('get_expr : binop_expr LBRACK binop_expr COMMA binop_expr COMMA binop_expr RBRACK')
def get_expr(p):
    return [Symbol('get'), p[0], [Symbol('v'), p[2], p[4], p[6]]]


@pg.production('get_expr : binop_expr LBRACK range_start COLON range_end RBRACK')
def get_slice_expr(p):
    return [Symbol('get'), p[0], p[2], p[4]]


@pg.production('get_expr : binop_expr LBRACK range_start COLON range_end COLON range_interval RBRACK')
def get_slice_expr(p):
    return [Symbol('get'), p[0], p[2], p[4], p[6]]


@pg.production('range_start : ')
@pg.production('range_end : ')
@pg.production('range_interval : ')
def range_start_none(p):
    return Symbol('None')


@pg.production('range_start : binop_expr')
@pg.production('range_end : binop_expr')
@pg.production('range_interval : binop_expr')
def range_start_none(p):
    return p[0]


@pg.production('for_expr : LBRACK binop_expr FOR pattern IN binop_expr RBRACK')
def for_expr(p):
    pattern = p[3]
    items = p[5]
    body = p[1]
    return [Symbol('tuple_of'), body, [pattern, items]]


@pg.production('for_expr : LBRACK binop_expr FOR pattern IN binop_expr IF binop_expr RBRACK')
def for_expr_if(p):
    pattern = p[3]
    items = p[5]
    body = p[1]
    when = p[7]
    return [Symbol('tuple_of'), body, [pattern, items, Keyword('when'), when]]


@pg.production('tuple_expr : LBRACK tuple_elts binop_expr RBRACK')
def tuple_expr(p):
    return [Symbol('make_tuple')] + p[1] + [p[2]]


@pg.production('tuple_expr : LBRACK binop_expr RBRACK')
def tuple_expr_one(p):
    return [Symbol('make_tuple'), p[1]]


@pg.production('tuple_expr : LBRACK tuple_elts binop_expr RBRACK')
def tuple_expr(p):
    return [Symbol('make_tuple')] + p[1] + [p[2]]


@pg.production('tuple_expr : LBRACK binop_expr RBRACK')
def tuple_expr_one(p):
    return [Symbol('make_tuple'), p[1]]


@pg.production('tuple_expr : LBRACK RBRACK')
def tuple_expr_empty(p):
    return [Symbol('make_tuple')]


@pg.production('tuple_elts : tuple_elts tuple_elt')
def tuple_elts(p):
    return p[0] + [p[1]]


@pg.production('tuple_elts : tuple_elt')
def tuple_elts_elt(p):
    return [p[0]]


@pg.production('tuple_elt : binop_expr COMMA')
def tuple_elt(p):
    return p[0]


#@pg.production('deco_expr : decorators binop_expr')
@pg.production('deco_expr : decorators func_expr')
def deco_expr(p):
    # return p[1][:2] + p[0] + p[1][2:]
    return [Symbol('with_decorator')] + p[0] + [p[1]]


@pg.production('decorators : decorators decorator')
def decorators(p):
    return p[0] + [p[1]]


@pg.production('decorators : decorator')
def decorators_single(p):
    return [p[0]]


@pg.production('decorator : AT binop_expr')
def decorator(p):
    return p[1]


@pg.production('func_expr : FUNC fun_header doc_string suite')
def fun_expr(p):
    fun_name, fun_args = p[1]
    return [Symbol('def'), fun_name, fun_args, p[3]]


@pg.production('funcm_expr : FUNC NAME doc_string lbrace defm_case_branches rbrace')
def fun_expr(p):
    return [Symbol('defm'), token_to_symbol(p[1])] + p[4]


@pg.production('defm_case_branches : defm_case_branches defm_case_branch')
def case_branches(p):
    return p[0] + p[1]


@pg.production('defm_case_branches : defm_case_branch')
def case_branches_branch(p):
    return p[0]


@pg.production('defm_case_branch : CASE defm_pattern THINARROW lbrace stmts rbrace')
def case_branch(p):
    return [p[1], [Symbol('do')] + p[4]]


@pg.production('defm_case_branch : CASE defm_pattern THINARROW binop_expr')
def case_branch(p):
    return [p[1], p[3]]


# @pg.production('defm_case_branch : CASE defm_pattern COLON binop_expr NEWLINE')
# def case_branch(p):
#     return [p[1], p[3]]


# @pg.production('defm_case_branch : CASE defm_pattern COLON binop_expr SEMI')
# def case_branch(p):
#     return [p[1], p[3]]


@pg.production('defm_pattern : app_nc_args')
def pattern(p):
    return p[0]


@pg.production('defm_pattern : pattern')
def app_args(p):
    return [p[0]]


@pg.production('defm_pattern : pattern COMMA defm_pattern')
def app_args(p):
    return [p[0]] + p[2]


@pg.production('fun_header : NAME_LPAREN list_arg_elts id_expr RPAREN')
def fun_header(p):
    return [namelparen_to_symbol(p[0]), p[1] + [p[2]]]


@pg.production('fun_header : NAME_LPAREN id_expr RPAREN')
def fun_header(p):
    return [namelparen_to_symbol(p[0]), [p[1]]]


@pg.production('fun_header : NAME_LPAREN RPAREN')
def fun_header(p):
    return [namelparen_to_symbol(p[0]), []]


@pg.production('fn_expr : id_expr FATARROW suite')
def fun_expr(p):
    return [Symbol('fn'), [p[0]], p[2]]


@pg.production('fn_expr : args FATARROW suite')
def fun_expr(p):
    return [Symbol('fn'), p[0], p[2]]


@pg.production('args : LPAREN list_arg_elts id_expr RPAREN')
def args(p):
    return p[1] + [p[2]]


@pg.production('args : LPAREN id_expr RPAREN')
def args_one(p):
    return [p[1]]


@pg.production('args : LPAREN RPAREN')
def args_empty(p):
    return []


@pg.production('nc_args : list_arg_elts id_expr')
def args(p):
    return p[0] + [p[1]]


@pg.production('nc_args : id_expr')
def args_one(p):
    return [p[0]]


@pg.production('list_arg_elts : list_arg_elts list_arg_elt')
def list_arg_elts(p):
    return p[0] + [p[1]]


@pg.production('list_arg_elts : list_arg_elt')
def list_arg_elts_elt(p):
    return [p[0]]


@pg.production('list_arg_elt : id_expr COMMA')
def list_arg_elt(p):
    return p[0]


def _create_underscore_args(exps):
    max_num = _compute_underscore_max_num(exps)
    if max_num == 1:
        return [Symbol('$1')]
    else:
        return [Symbol('$' + str(n)) for n in range(1, max_num + 1)]


@pg.production('block_expr : FATARROW suite')
def block_expr(p):
    block = p[1]
    return [Symbol('fn'), _create_underscore_args(block), block]


@pg.production('doc_string : DOC string')
@pg.production('doc_string : ')
def doc_string(p):
    pass


from collections import Iterable


def flatten_list(lis):
    i = 0
    while i < len(lis):
        while isinstance(lis[i], Iterable):
            if not lis[i]:
                lis.pop(i)
                i -= 1
                break
            else:
                lis[i:i + 1] = lis[i]
        i += 1
    return lis


@pg.production('call_macro_expr : MACRO_NAME head')
def call_macro_expr(p):
    head = p[1]
    body = None
    rest = []
    return process_calling_macro(token_to_symbol(p[0]), head, body, rest)


@pg.production('call_macro_expr : MACRO_NAME head rest')
def call_macro_expr(p):
    head = p[1]
    body = None
    rest = p[2]
    return process_calling_macro(token_to_symbol(p[0]), head, body, rest)


@pg.production('call_macro_expr : MACRO_NAME do_suite')
def call_macro_expr(p):
    head = []
    body = p[1]
    rest = []
    return process_calling_macro(token_to_symbol(p[0]), head, body, rest)


@pg.production('call_macro_expr : MACRO_NAME head do_suite')
def call_macro_expr(p):
    head = p[1]
    body = p[2]
    rest = []
    return process_calling_macro(token_to_symbol(p[0]), head, body, rest)


@pg.production('call_macro_expr : MACRO_NAME head do_suite rest')
def call_macro_expr(p):
    head = p[1]
    body = p[2]
    rest = p[3]
    return process_calling_macro(token_to_symbol(p[0]), head, body, rest)


def process_calling_macro(name, head, body, rest):
    # macro_name = name.name
    # if macro_name == 'macro':
    #     call_func, *rest = head
    #     _, fun_name, *fun_args = call_func
    #     return [Symbol('mac'), fun_name, fun_args, body]
    # elif macro_name == 'def':
    #     call_func, *rest = head
    #     _, fun_name, *fun_args = call_func
    #     return [Symbol('def'), fun_name, fun_args, body]
    # elif macro_name == 'if':
    #     clauses = [head[0], body]
    #     for rest_clause in rest:
    #         label, head, body = rest_clause
    #         if label == Symbol('elif'):
    #             clauses.append(head[0])
    #             clauses.append(body)
    #         elif label == Symbol('else'):
    #             clauses.append(body)
    #             return [Symbol('if'), *clauses]
    #         else:
    #            error = SyntaxError(label)
    #             error.filename = '<string>'
    #             error.lineno = name.lineno
    #             error.offset = name.col_offset
    #             raise error
    #     return [Symbol('if'), *clauses]
    # elif macro_name == 'return':
    #     return [Symbol('return'), head[0]]
    # elif macro_name == 'raise':
    #     return [Symbol('raise'), head[0]]
    # else:
    # if rest is None or len(rest) == 0:
    #     return [Symbol('call_macro'), name, head, body]
    # else:
    return [Symbol('call_macro'), name, head, body, rest]


@pg.production('rest : ')
def rest(p):
    return []


@pg.production('rest : rest_item')
def rest(p):
    return [p[0]]


@pg.production('rest : rest rest_item')
def rest(p):
    return p[0] + [p[1]]


@pg.production('rest_item : sub_keyword head do_suite')
def rest_item(p):
    head = p[1]
    body = p[2]
    return [p[0], head, body]


@pg.production('rest_item : sub_keyword do_suite')
def rest_item(p):
    head = []
    body = p[1]
    return [p[0], head, body]


@pg.production('sub_keyword : ELSE')
@pg.production('sub_keyword : ELSEIF')
@pg.production('sub_keyword : EXCEPT')
@pg.production('sub_keyword : USER_DEFINED_KEYWORD')
def sub_keyword(p):
    return token_to_symbol(p[0])


@pg.production('head : app_nc_args')
def head(p):
    return p[0]


@pg.production('if_expr : IF binop_expr suite')
def if_expr(p):
    return [Symbol('if'), p[1], p[2]]


@pg.production('if_expr : IF binop_expr suite elseif_exprs')
def if_expr(p):
    return [Symbol('if'), p[1], p[2]] + p[3]


def namelparen_to_symbol(token):
    return Symbol(token.getstr()[:-1],
                  token.getsourcepos().lineno,
                  token.getsourcepos().colno)


@pg.production('call_func_expr : NAME_LPAREN RPAREN')
def call_func_expr(p):
    return [Symbol('call_func'),
            namelparen_to_symbol(p[0])]


# @pg.production('call_func_expr : NAME_LPAREN RPAREN fn_expr')
# @pg.production('call_func_expr : NAME_LPAREN RPAREN block_expr')
def call_func_expr(p):
    return [Symbol('call_func'),
            namelparen_to_symbol(p[0]), p[2]]


@pg.production('call_func_expr : NAME_LPAREN app_args_elts RPAREN')
def call_func_expr(p):
    return [Symbol('call_func'),
            namelparen_to_symbol(p[0])] + p[1]


@pg.production('app_expr : binop_expr app_args')
def call_func_expr(p):
    return [p[0]] + p[1]


#@pg.production('call_func_expr : NAME_LPAREN app_args_elts RPAREN fn_expr')
#@pg.production('call_func_expr : NAME_LPAREN app_args_elts RPAREN block_expr')
#def call_func_expr(p):
#    return [Symbol('call_func'),
#            namelparen_to_symbol(p[0])] + [p[3]] + p[1]


@pg.production('call_func_expr : paren_expr LPAREN RPAREN')
def call_func_expr(p):
    return [Symbol('call_func'), p[0]]


@pg.production('call_func_expr : paren_expr LPAREN app_args_elts RPAREN')
def call_func_expr(p):
    return [Symbol('call_func'), p[0]] + p[2]


#@pg.production('call_func_expr : call_func_expr LPAREN RPAREN')
#def call_func_expr(p):
#    return [Symbol('call_func'), p[0]]


#@pg.production('call_func_expr : call_func_expr LPAREN app_args_elts RPAREN')
#def call_func_expr(p):
#    return [Symbol('call_func'), p[0]] + p[2]


@pg.production('call_method_expr : expr DOT_NAME_LPAREN RPAREN')
def call_method_expr(p):
    return [Symbol('call_func'), [Symbol('getattr'), p[0], p[1].getstr()[1:-1]]]


@pg.production('call_method_expr : expr DOT_NAME_LPAREN app_args_elts RPAREN')
def call_method_expr(p):
    return [Symbol('call_func'), [Symbol('getattr'), p[0], p[1].getstr()[1:-1]]] + p[2]


@pg.production('app_args : LPAREN app_args_elts RPAREN')
def app_args(p):
    return p[1]


@pg.production('app_args : LPAREN RPAREN')
def app_args(p):
    return []


@pg.production('app_args_elts : app_args_elts COMMA app_args_elt')
def app_args_elts(p):
    return p[0] + p[2]


@pg.production('app_args_elts : app_args_elt')
def app_args_elts(p):
    return p[0]


@pg.production('app_args_elt : NAME EQUALS binop_expr')
def app_args_elt(p):
    return [token_to_keyword(p[0]), p[2]]


@pg.production('app_args_elt : EQUALS NAME')
def app_args_elt_short(p):
    return [token_to_keyword(p[1]), token_to_symbol(p[1])]


@pg.production('app_args_elt : binop_expr')
def app_args_elt(p):
    return [p[0]]


# TODO
#@pg.production('app_expr : expr app_args app_args')
#@pg.production('app_expr : expr app_args app_args')
def trailing_closure_expr(p):
    return [[p[0]] + p[1]] + p[2]


#@pg.production('app_expr : expr app_args AT fn_expr')
#@pg.production('app_expr : expr app_args AT block_expr')
#def trailing_closure_expr(p):
#    return [p[0]] + p[1] + [p[3]]


@pg.production('app_nc_expr : expr app_nc_args')
def app_expr(p):
    return [p[0]] + p[1]


@pg.production('app_nc_args : app_nc_arg')
def app_nc_args(p):
    return [p[0]]


@pg.production('app_nc_args : app_nc_arg COMMA app_nc_args')
def app_nc_args(p):
    return [p[0]] + p[2]


# @pg.production('app_nc_args : app_nc_arg app_nc_args')
# def app_nc_args(p):
#     return [p[0]] + p[1]


# @pg.production('app_nc_args : app_nc_arg labeled_blocks')
# def app_nc_args(p):
#     return [p[0]] + p[1]
#
#
# @pg.production('labeled_blocks : labeled_block labeled_blocks')
# def labeled_blocks(p):
#     return [p[0]] + p[1]
#
#
# @pg.production('labeled_blocks : labeled_block')
# def labeled_blocks(p):
#     return [p[0]]


@pg.production('app_nc_arg : binop_expr')
def app_nc_arg(p):
    return p[0]


@pg.production('left_app_expr : expr CALET left_app_fun_expr app_args')
def left_app_expr(p):
    expr, _, left_app_fun_expr, app_args = p
    return [left_app_fun_expr, expr] + app_args


@pg.production('left_app_fun_expr : id_expr')
def left_app_fun_expr(p):
    return p[0]


@pg.production('dict_expr : lbrace rbrace')
def dict_expr_empty(p):
    return [Symbol('table')]


@pg.production('dict_expr : lbrace fields rbrace')
def dict_expr(p):
    return [Symbol('table')] + p[1]


@pg.production('fields : field')
def fields_one(p):
    return p[0]


@pg.production('fields : list_fields field')
def fields(p):
    return p[0] + p[1]


@pg.production('list_fields : list_field')
def list_fields_one(p):
    return p[0]


@pg.production('list_fields : list_fields list_field')
def list_fields(p):
    return p[0] + p[1]


@pg.production('list_field : field COMMA')
def list_field(p):
    return p[0]


@pg.production('field : key COLON binop_expr')
def field(p):
    return [p[0], p[2]]


@pg.production('field : EQUALS NAME')
def field(p):
    s = token_to_symbol(p[1])
    return [s.name, s]


@pg.production('key : prim_expr')
@pg.production('key : id_expr')
@pg.production('key : call_func_expr')
def key(p):
    return p[0]


@pg.production('match_expr : MATCH binop_expr lbrace case_branches rbrace')
def case(p):
    return [Symbol('match'), p[1]] + p[3]


@pg.production('case_branches : case_branches case_branch')
def case_branches(p):
    return p[0] + p[1]


@pg.production('case_branches : case_branch')
def case_branches_branch(p):
    return p[0]


@pg.production('case_branch : CASE pattern THINARROW lbrace stmts rbrace')
def case_branch(p):
    return [p[1], [Symbol('do')] + p[4]]


@pg.production('case_branch : CASE pattern THINARROW binop_expr')
def case_branch(p):
    return [p[1], p[3]]


# @pg.production('case_branch : CASE pattern COLON binop_expr SEMI')
# def case_branch(p):
#     return [p[1], p[3]]


# @pg.production('pattern : fn_expr')
@pg.production('pattern : prim_pattern')
@pg.production('pattern : dict_pattern')
@pg.production('pattern : sequence_pattern')
@pg.production('pattern : sequence_type_pattern')
@pg.production('pattern : type_pattern')
@pg.production('pattern : id_pattern')
@pg.production('pattern : ref_pattern')
# @pg.production('pattern : and_pattern')
# @pg.production('pattern : or_pattern')
@pg.production('pattern : quote_pattern')
# TODO @pg.production('defm_pattern : app_nc_args')
def pattern(p):
    return p[0]


@pg.production('prim_pattern : NUMBER')
def pattern_num(p):
    num_repr = p[0].getstr()
    try:
        return int(num_repr)
    except ValueError as _:
        return float(num_repr)


@pg.production('prim_pattern : string')
def pattern_string(p):
    return p[0]


@pg.production('prim_pattern : bool_expr')
def pattern_bool(p):
    return p[0]


@pg.production('dict_pattern : lbrace rbrace')
def dict_pattern_empty(p):
    return [Symbol('table')]


@pg.production('dict_pattern : lbrace dict_pattern_fields rbrace')
def dict_pattern(p):
    return [Symbol('table')] + p[1]


@pg.production('dict_pattern_fields : dict_pattern_field')
def fields_one(p):
    return p[0]


@pg.production('dict_pattern_fields : dict_pattern_list_fields dict_pattern_field')
def fields(p):
    return p[0] + p[1]


@pg.production('dict_pattern_list_fields : dict_pattern_list_field')
def list_fields_one(p):
    return p[0]


@pg.production('dict_pattern_list_fields : dict_pattern_list_fields dict_pattern_list_field')
def list_fields(p):
    return p[0] + p[1]


@pg.production('dict_pattern_list_field : dict_pattern_field COMMA')
def list_field(p):
    return p[0]


@pg.production('dict_pattern_field : dict_pattern_key COLON pattern')
def field(p):
    return [p[0], p[2]]


@pg.production('dict_pattern_field : EQUALS NAME')
def field(p):
    s = token_to_symbol(p[1])
    return [s.name, s]


@pg.production('dict_pattern_key : binop_expr')
def key(p):
    return p[0]


@pg.production('id_pattern : NAME')
def id_pattern(p):
    return token_to_symbol(p[0])


@pg.production('id_pattern : AMP')
def id_pattern(p):
    return Symbol('&')


@pg.production('sequence_pattern : LBRACK sequence_pattern_elts pattern RBRACK')
def sequence_pattern(p):
    return [Symbol('make_tuple')] + p[1] + [p[2]]


@pg.production('sequence_pattern : LBRACK pattern RBRACK')
def sequence_pattern_one(p):
    return [Symbol('make_tuple'), p[1]]


@pg.production('sequence_pattern : LBRACK RBRACK')
def sequence_pattern_empty(p):
    return [Symbol('make_tuple')]


@pg.production('sequence_pattern_elts : sequence_pattern_elts sequence_pattern_elt')
def sequence_pattern_elts(p):
    return p[0] + [p[1]]


@pg.production('sequence_pattern_elts : sequence_pattern_elt')
def sequence_pattern_elts_elt(p):
    return [p[0]]


@pg.production('sequence_pattern_elt : pattern COMMA')
def sequence_pattern_elt(p):
    return p[0]


@pg.production('sequence_pattern_named_elts : sequence_pattern_named_elts sequence_pattern_named_elt')
def sequence_pattern_named_elts(p):
    return p[0] + p[1]


@pg.production('sequence_pattern_named_elts : sequence_pattern_named_elt')
def sequence_pattern_named_elts_elt(p):
    return p[0]


@pg.production('sequence_pattern_named_elt : named_pattern COMMA')
def sequence_pattern_named_elt(p):
    return p[0]


@pg.production('named_pattern : NAME EQUALS pattern')
def sequence_pattern_named_pattern(p):
    s = token_to_symbol(p[0])
    return [s.name, p[2]]


@pg.production('sequence_type_pattern : names_lparen sequence_pattern_elts pattern RPAREN')
def sequence_type_pattern(p):
    return [Symbol('sequence_type'), p[0]] + p[1] + [p[2]]


@pg.production('sequence_type_pattern : names_lparen sequence_pattern_named_elts named_pattern RPAREN')
def sequence_type_pattern(p):
    return [Symbol('sequence_type_with_named_member'), p[0]] + p[1] + p[2]


@pg.production('sequence_type_pattern : names_lparen pattern RPAREN')
def sequence_type_pattern_one(p):
    return [Symbol('sequence_type'), p[0], p[1]]


@pg.production('sequence_type_pattern : names_lparen named_pattern RPAREN')
def sequence_type_pattern_one(p):
    return [Symbol('sequence_type_with_named_member'), p[0], p[1]]


@pg.production('and_pattern : pattern OPAND pattern')
def and_pattern(p):
    return [token_to_symbol(p[1]), p[0], p[2]]


@pg.production('or_pattern : pattern OPOR pattern')
def or_pattern(p):
    return [token_to_symbol(p[1]), p[0], p[2]]


#@pg.production('type_pattern : pattern COLON NAME')
#def type_pattern(p):
#    return [Symbol('type'), token_to_symbol(p[2]), p[0]]


@pg.production('type_pattern : pattern COLON binop_expr')
def type_pattern(p):
    return [Symbol('type'), p[2], p[0]]


@pg.production('ref_pattern : CALET NAME')
def ref_pattern(p):
    return [Symbol('ref'), token_to_symbol(p[1])]


# @pg.production('quote_pattern : QUOTE LPAREN pattern RPAREN')
@pg.production('quote_pattern : QUOTE pattern')
def quote_pattern(p):
    return [Symbol('quote'), p[1]]


@pg.production('record_expr : RECORD NAME')
def record_expr(p):
    return [Symbol('record'), token_to_symbol(p[1]), []]


# @pg.production('record_expr : RECORD NAME OPLT NAME')
# def record_expr(p):
#     return [Symbol('record'), token_to_symbol(p[1]), token_to_symbol(p[3]), []]


@pg.production('record_expr : RECORD NAME_LPAREN record_fields RPAREN')
def record_expr(p):
    return [Symbol('record'), namelparen_to_symbol(p[1]), p[2]]


@pg.production('record_expr : RECORD NAME_LPAREN record_fields RPAREN OPLT NAME')
def record_expr(p):
    return [Symbol('record'), namelparen_to_symbol(p[1]), token_to_symbol(p[5]), p[2]]


@pg.production('record_expr : RECORD NAME lbrace record_body rbrace')
def record_expr(p):
    return [Symbol('record'), token_to_symbol(p[1]), []] + p[3]


@pg.production('record_expr : RECORD NAME OPLT NAME lbrace record_body rbrace')
def record_expr(p):
    return [Symbol('record'), token_to_symbol(p[1]), token_to_symbol(p[3]), []] + p[5]


@pg.production('record_expr : RECORD NAME_LPAREN record_fields RPAREN lbrace record_body rbrace')
def record_expr(p):
    return [Symbol('record'), namelparen_to_symbol(p[1]), p[2]] + p[5]


@pg.production('record_expr : RECORD NAME_LPAREN record_fields RPAREN OPLT NAME lbrace record_body rbrace')
def record_expr(p):
    return [Symbol('record'), namelparen_to_symbol(p[1]), token_to_symbol(p[5]), p[2]] + p[7]


# @pg.production('union_expr : UNION suite2')
# def union_expr(p):
#     return [Symbol('union')] + p[1]


# @pg.production('predicate_expr : PREDICATE binop_expr')
# def union_expr(p):
#     return [Symbol('predicate'), p[1]]


@pg.production('record_body : func_expr')
def record_body(p):
    return [p[0]]


@pg.production('record_body : record_body func_expr')
def record_body(p):
    return p[0] + [p[1]]


@pg.production('record_fields : record_field')
def record_expr(p):
    return [p[0]]


@pg.production('record_fields : record_field COMMA record_fields')
def record_expr(p):
    return [p[0]] + p[2]


@pg.production('record_field : id_expr')
def record_expr(p):
    return p[0]


@pg.production('record_field : id_expr COLON binop_expr')
def record_expr(p):
    return [p[0], p[2]]


@pg.production('data_expr : DATA NAME lbrace data_record_expr_list rbrace')
def data_expr(p):
    return [Symbol('data'), token_to_symbol(p[1])] + p[3]


@pg.production('data_record_expr_list : data_record_expr')
def record_expr(p):
    return [p[0]]


@pg.production('data_record_expr_list : data_record_expr data_record_expr_list')
def record_expr(p):
    return [p[0]] + p[1]


@pg.production('data_record_expr : NAME_LPAREN record_fields RPAREN')
def record_expr(p):
    return [namelparen_to_symbol(p[0])] + p[1]


@pg.production('binop_expr : NOT binop_expr')
def binop_expr(p):
    return [token_to_symbol(p[0]), p[1]]


@pg.production('binop_expr : binop_expr OPPLUS binop_expr')
@pg.production('binop_expr : binop_expr OPMINUS binop_expr')
@pg.production('binop_expr : binop_expr OPTIMES binop_expr')
@pg.production('binop_expr : binop_expr PERCENT binop_expr')
@pg.production('binop_expr : binop_expr OPDIV binop_expr')
@pg.production('binop_expr : binop_expr OPLEQ binop_expr')
@pg.production('binop_expr : binop_expr OPGEQ binop_expr')
@pg.production('binop_expr : binop_expr OPEQ binop_expr')
@pg.production('binop_expr : binop_expr OPNEQ binop_expr')
@pg.production('binop_expr : binop_expr OPLT binop_expr')
@pg.production('binop_expr : binop_expr OPGT binop_expr')
@pg.production('binop_expr : binop_expr OPBITOR binop_expr')
@pg.production('binop_expr : binop_expr OPBITXOR binop_expr')
@pg.production('binop_expr : binop_expr OPBITAND binop_expr')
@pg.production('binop_expr : binop_expr OPFLOORDIV binop_expr')
@pg.production('binop_expr : binop_expr OPPOW binop_expr')
@pg.production('binop_expr : binop_expr OPRSHIFT binop_expr')
@pg.production('binop_expr : binop_expr OPLSHIFT binop_expr')
@pg.production('binop_expr : binop_expr OPAND binop_expr')
@pg.production('binop_expr : binop_expr OPOR binop_expr')
@pg.production('binop_expr : binop_expr OPIS binop_expr')
@pg.production('binop_expr : binop_expr IN binop_expr')
@pg.production('binop_expr : binop_expr AS id_expr')
def binop_expr(p):
    return [token_to_symbol(p[1]), p[0], p[2]]


@pg.production('binop_expr : binop_expr INFIX_MACRO_NAME binop_expr')
def binop_expr(p):
    return [Symbol('call_macro'), token_to_symbol(p[1]), p[0], p[2]]


@pg.production('binop_expr : binop_expr INFIX_1_MACRO_NAME binop_expr')
def binop_expr(p):
    return [Symbol('call_macro'), token_to_symbol(p[1]), p[0], p[2]]


@pg.production('binop_expr : binop_expr INFIX_2_MACRO_NAME binop_expr')
def binop_expr(p):
    return [Symbol('call_macro'), token_to_symbol(p[1]), p[0], p[2]]


@pg.production('binop_expr : binop_expr NOT IN binop_expr')
def binop_expr(p):
    return [Symbol('not_in'), p[0], p[3]]


@pg.production('binop_expr : binop_expr PIPELINE binop_expr')
def binop_expr(p):
    return [Symbol('|>'), p[0], p[2]]


@pg.production('binop_expr : binop_expr PIPELINE_BIND binop_expr')
def binop_expr(p):
    left, _, right = p
    input_sym = get_temp_name()
    return [Symbol('|>'), p[0], [Symbol('bind'),
                                 [Symbol('fn'), [input_sym], p[2] + [input_sym]]]]


@pg.production('binop_expr : binop_expr PIPELINE_FIRST binop_expr')
def binop_expr(p):
    return [Symbol('|>1'), p[0], p[2]]


@pg.production('binop_expr : binop_expr PIPELINE_FIRST_BIND binop_expr')
def binop_expr(p):
    left, _, right = p
    input_sym = get_temp_name()
    return [Symbol('|>'), p[0], [Symbol('bind'),
                                 [Symbol('fn'), [input_sym],
                                  [p[2][0], input_sym] + p[2][(1 if len(p[2]) > 1 else len(p[2])):]]]]


@pg.production('binop_expr : expr')
def binop_expr(p):
    return p[0]