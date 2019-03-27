import sys
from queue import Queue

from rply import LexerGenerator, Token

REPL_CONTINUE = object()

INFIX_OPERATORS = {'OPPLUS',
                   'OPMINUS',
                   'OPTIMES',
                   'PERCENT',
                   'OPDIV',
                   'OPLEQ',
                   'OPGEQ',
                   'OPEQ',
                   'OPNEQ',
                   'OPLT',
                   'OPGT',
                   'OPBITOR',
                   'OPBITAND',
                   'OPBITXOR',
                   'OPFLOORDIV',
                   'OPPOW',
                   'OPRSHIFT',
                   'OPLSHIFT',
                   'OPAND',
                   'OPOR',
                   'OPIS',
                   'PIPELINE',
                   'PIPELINE_BIND',
                   'PIPELINE_FIRST',
                   'PIPELINE_FIRST_BIND',
                   'PIPELINE_SEND',
                   'PIPELINE_MULTI_SEND'}


def _set_keyword(token):
    if token.name == 'NAME':
        for rule in klg.rules:
            if rule.matches(token.value, 0):
                token.name = rule.name
                break
    elif token.name == 'NAME_LPAREN':
        for rule in klg.rules:
            if rule.matches(token.value, 0):
                token.name = rule.name
                break


def mod_lex(lexer, repl_mode=False):
    paren_openers = {'LPAREN', 'LBRACE', 'LBRACK', 'NAME_LPAREN', 'DOT_NAME_LPAREN'}
    paren_closers = {'RPAREN', 'RBRACE', 'RBRACK', 'NAME_RPAREN', 'DOT_NAME_RPAREN'}

    token_queue = Queue()
    paren_level = 0

    # def handle_newline(token):
    #     text = token.getstr()
    #     indent_str = text.rsplit('\n', 1)[1]
    #     indent = indent_str.count(' ') + indent_str.count('\t') * tab_len
    #     if indent > indent_level[-1]:
    #         indent_level.append(indent)
    #         indent_token = Token('INDENT', indent_str)
    #         indent_token.source_pos = token.getsourcepos()
    #         token_queue.put(indent_token)
    #     else:
    #         while indent < indent_level[-1]:
    #             indent_level.pop()
    #             dedent_token = Token('DEDENT', indent_str)
    #             token_queue.put(dedent_token)
    #         if len(text.rsplit('\n')) > 2:
    #             token_queue.put(Token('NEWLINE', '\n'))
    #     return token

    for token in lexer:
        while not token_queue.empty():
            queued_token = token_queue.get()
            if queued_token.gettokentype() in paren_openers:
                paren_level += 1
            elif queued_token.gettokentype() in paren_closers:
                paren_level -= 1

            if queued_token.gettokentype() == 'NAME' and queued_token.getstr().startswith('&'):
                amp = Token('AMP', '&')
                amp.source_pos = queued_token.getsourcepos()
                comma = Token('COMMA', ',')
                amp.source_pos = queued_token.getsourcepos()
                name = Token('NAME', queued_token.getstr()[1:])
                name.source_pos = queued_token.getsourcepos()
                yield amp
                yield comma
                yield name
            else:
                yield queued_token

        if token.name == 'NAME':
            for rule in klg.rules:
                if rule.matches(token.value, 0):
                    token.name = rule.name
                    break
        if token.name == 'NAME_LPAREN':
            for rule in klg.rules:
                if rule.matches(token.value, 0):
                    token.name = rule.name
                    break
        if token.gettokentype() in INFIX_OPERATORS:
            ahead_token = next(lexer)
            _set_keyword(ahead_token)
            if ahead_token.gettokentype() == 'NEWLINE':
                pass
            else:
                token_queue.put(ahead_token)
        elif token.gettokentype() == 'NEWLINE':
            continue

        if token.gettokentype() in paren_openers:
            paren_level += 1
        elif token.gettokentype() in paren_closers:
            paren_level -= 1

        if token.gettokentype() == 'NAME' and token.getstr().startswith('&'):
            amp = Token('AMP', '&')
            amp.source_pos = token.getsourcepos()
            comma = Token('COMMA', ',')
            amp.source_pos = token.getsourcepos()
            name = Token('NAME', token.getstr()[1:])
            name.source_pos = token.getsourcepos()
            yield amp
            yield comma
            yield name
        else:
            yield token

    if repl_mode and paren_level > 0:
        yield REPL_CONTINUE
    else:
        while not token_queue.empty():
            yield token_queue.get()


def mod_mod_lex(lexer, filename):
    for token in lexer:
        if token is REPL_CONTINUE:
            yield token
        else:
            token.filename = filename
            token_str = token.getstr()
            macro_key = (filename, token.getstr())
            if token.gettokentype() == 'NAME' and macro_key in macro_names:
                yield Token('MACRO_NAME', token_str, token.getsourcepos())
            elif token.gettokentype() == 'NAME' and macro_key in infix_macro_names:
                yield Token('INFIX_MACRO_NAME', token_str, token.getsourcepos())
            elif token.gettokentype() == 'NAME' and macro_key in infix_1_macro_names:
                yield Token('INFIX_1_MACRO_NAME', token_str, token.getsourcepos())
            elif token.gettokentype() == 'NAME' and macro_key in infix_2_macro_names:
                yield Token('INFIX_2_MACRO_NAME', token_str,token.getsourcepos())
            elif token.gettokentype() == 'NAME' and macro_key in user_defined_keywords:
                yield Token('USER_DEFINED_KEYWORD', token_str, token.getsourcepos())
            else:
                yield token


def lex(input, repl_mode=False, debug=False, filename='<string>'):
    if debug:
        print(list(mod_mod_lex(mod_lex(lg.build().lex(input), repl_mode))), file=sys.stderr)
    return mod_mod_lex(mod_lex(lg.build().lex(input), repl_mode), filename)


macro_names = []
infix_macro_names = []
infix_1_macro_names = []
infix_2_macro_names = []
user_defined_keywords = []


def add_macro_name(macro_name):
    macro_names.append(macro_name)


def add_infix_macro_name(macro_name):
    infix_macro_names.append(macro_name)


def add_infix_1_macro_name(macro_name):
    infix_1_macro_names.append(macro_name)


def add_infix_2_macro_name(macro_name):
    infix_2_macro_names.append(macro_name)


def add_user_defined_keyword(keyword):
    user_defined_keywords.append(keyword)


lg = LexerGenerator()

lg.add('TQUOTE_STR', r'(?x)"""(?:|[^\\]|\\.|\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})*"""')
lg.add('SQUOTE_STR', r"(?x)'(?:|[^'\\]|\\.|\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})*'")
lg.add('DQUOTE_STR', r'(?x)"(?:|[^"\\]|\\.|\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})*"')

lg.add('TQUOTE_RAW_STR', r'(?x)r"""(?:|[^\\]|\\.|\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})*"""')
lg.add('SQUOTE_RAW_STR', r"(?x)r'(?:|[^'\\]|\\.|\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})*'")
lg.add('DQUOTE_RAW_STR', r'(?x)r"(?:|[^"\\]|\\.|\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})*"')

lg.add('NUMBER', r'-?[0-9]+(?:\.[0-9]+)?')
lg.add('OPBITAND', r'\&\&')
lg.add('DOT_NAME_LPAREN', r'\.\&?[_a-zA-Z$][-_a-zA-Z0-9]*\(')
lg.add('DOT_NAME', r'\.\&?[_a-zA-Z$][-_a-zA-Z0-9]*')
# lg.add('NAME_BANG_LPAREN', r'\&?[_a-zA-Z$][-_a-zA-Z0-9]*!\(')
# lg.add('NAME_BANG', r'\&?[_a-zA-Z$][-_a-zA-Z0-9]*!')
lg.add('NAME_LPAREN', r'\&?[_a-zA-Z$][-_a-zA-Z0-9]*\(')
lg.add('NAME', r'\&?[_a-zA-Z$][-_a-zA-Z0-9]*')
lg.add('PIPELINE_FIRST_BIND', r'\|>1\?')
lg.add('PIPELINE_FIRST', r'\|>1')
lg.add('PIPELINE_BIND', r'\|>\?')
lg.add('PIPELINE', r'\|>')
lg.add('OPBITOR', r'\|')
lg.add('OPBITXOR', r'\^\^')
lg.add('OPFLOORDIV', r'//')
lg.add('OPPOW', r'\*\*')
lg.add('OPRSHIFT', r'>>')
lg.add('OPLSHIFT', r'<<')
lg.add('LBRACK', r'\[')
lg.add('RBRACK', r'\]')
lg.add('LBRACE', r'\{')
lg.add('RBRACE', r'\}')
lg.add('LPAREN', r'\(')
lg.add('RPAREN', r'\)')
lg.add('PERCENT', r'%')
lg.add('COMMA', r',')
lg.add('THINARROW', r'->')
lg.add('FATARROW', r'=>')
lg.add('COLON', r':')
lg.add('CALET', r'\^')
lg.add('OPPLUS', r'\+')
lg.add('OPMINUS', r'-')
lg.add('OPTIMES', r'\*')
lg.add('OPDIV', r'/')
lg.add('OPLEQ', r'<=')
lg.add('OPGEQ', r'>=')
lg.add('OPEQ', r'==')
lg.add('OPNEQ', r'!=')
lg.add('OPLT', r'<')
lg.add('OPGT', r'>')
lg.add('EQUALS', r'=')
lg.add('SEMI', r';')
lg.add('AT', r'@')
lg.add('AMP', r'\&')
lg.add('BACKSLASH', r'\\')

lg.add('NEWLINE', r'(?:(?:\r?\n)[\t ]*)+')
lg.ignore(r'[ \t\f\v]+')
lg.ignore(r'#.*(?:\n|\r|\r\n|\n\r|$)')  # comment

klg = LexerGenerator()
klg.add('IMPORT', r'^import$')
klg.add('USE', r'^use$')
# klg.add('UNION', r'^union$')
# klg.add('PREDICATE', r'^predicate$')
klg.add('DO', r'^do$')
klg.add('END', r'^end$')
klg.add('LET', r'^let$')
klg.add('FUNC', r'^func$')
klg.add('TRUE', r'^True$')
klg.add('FALSE', r'^False$')
klg.add('TRY', r'^try$')
klg.add('EXCEPT', r'^except$')
klg.add('AS', r'^as$')
klg.add('FINALLY', r'^finally$')
klg.add('RAISE', r'^raise$')
klg.add('IF', r'^if$')
klg.add('ELSE', r'^else$')
klg.add('ELSEIF', r'^elif$')
klg.add('MATCH', r'^match$')
klg.add('CASE', r'^case$')
klg.add('RECORD', r'^record$')
klg.add('DATA', r'^data$')
klg.add('YIELD', r'^yield$')
klg.add('RETURN', r'^return$')
klg.add('CALL', r'^call$')
klg.add('WITH', r'^with$')
klg.add('MACRO', r'^macro$')
klg.add('INFIX', r'^infix$')
klg.add('INFIX_1', r'^infix_1$')
klg.add('INFIX_2', r'^infix_2$')
klg.add('QUOTE', r'^quote$')
klg.add('QUOTE_LPAREN', r'^quote\($')
klg.add('QUASI_QUOTE', r'^quasi_quote$')
klg.add('QUASI_QUOTE_LPAREN', r'^quasi_quote\($')
klg.add('UNQUOTE', r'^unquote$')
klg.add('UNQUOTE_LPAREN', r'^unquote\($')
klg.add('UNQUOTE_SPLICING', r'^unquote_splicing$')
klg.add('UNQUOTE_SPLICING_LPAREN', r'^unquote_splicing\($')
klg.add('FOR', r'^for$')
klg.add('IN', r'^in$')
klg.add('FROM', r'^from$')
klg.add('OPAND', r'^and$')
klg.add('OPOR', r'^or$')
klg.add('OPIS', r'^is$')
klg.add('NOT', r'^not$')
klg.add('ASSERT', r'^assert$')