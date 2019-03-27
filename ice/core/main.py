import argparse
from pathlib import Path
import sys
import os
from platform import platform, system
import traceback

from ice import __version__, IS_PYPY, GE_PYTHON_34, GE_PYTHON_33
from ice.parser import lex, REPL_CONTINUE, ParsingError
from .builtins import current_error_port, eval_sexp_str, eval_tokens
from .global_env import global_env
from .translation import syntax_table, global_scope, translator


GLOBAL_ENV = 'import_global_env.ice'


def output_code(code):
    import marshal

    marshal.dump(code, sys.stdout.buffer)


def output_pyc(code, buffer=sys.stdout.buffer):
    import marshal
    import struct
    import time

    if GE_PYTHON_34:
        from importlib.util import MAGIC_NUMBER
    else:
        import imp
        MAGIC_NUMBER = imp.get_magic()

    buffer.write(MAGIC_NUMBER)
    timestamp = struct.pack('i', int(time.time()))
    buffer.write(timestamp)
    if GE_PYTHON_33:
        buffer.write(b'0' * 4)
    marshal.dump(code, buffer)
    buffer.flush()


def compile_file(src_path, optimize=-1, show_tokens=False):
    # binding_name_set_stack[0].update(global_env.keys())
    py_ast = translator.translate_file(src_path, show_tokens=show_tokens)
    return compile(py_ast, src_path, 'exec', optimize=optimize)


def load_file(path, env, optimize=-1):
    return exec(compile_file(path, optimize), env)


def execute_compiled_file(path):
    import marshal
    orig_main = sys.modules['__main__']
    sys.modules['__main__'] = global_env
    try:
        with open(path, 'rb') as compiled_file:
            return exec(marshal.load(compiled_file), global_env)
    finally:
        sys.modules['__main__'] = orig_main


def interact(show_tokens=False):
    try:
        import readline
    except ImportError:
        pass

    del global_env['__file__']
    sys.modules['__main__'] = global_env

    while True:
        buffer = ''
        continuation_flag = False
        tokens = []
        while True:
            try:
                if continuation_flag:
                    s = input('... ')
                    if s == '\n':
                        continue
                    buffer = buffer + '\n' + s
                else:
                    s = input('>>> ')
                    if s == '\n':
                        continue
                    buffer = s
            except EOFError:
                print()
                sys.exit()

            try:
                lexer = lex(buffer, repl_mode=True, debug=show_tokens)

                for last in lexer:
                    tokens.append(last)

                if len(tokens) == 0:
                    buffer = ''
                    continue

                if last is REPL_CONTINUE or last.name == 'COLON' or last.name == 'THINARROW':
                    continuation_flag = True
                    tokens = []
                    continue
                else:
                    break
            except Exception:
                traceback.print_exc(file=current_error_port)
                continuation_flag = False
                buffer = ''
                continue
        try:
            eval_tokens(tokens)
        except ParsingError as e:
            print(e, file=current_error_port)
        except Exception:
            traceback.print_exc(file=current_error_port)


def init():
    if hasattr(init, '__called') and init.__called:
        return
    else:
        init.__called = True

    def eval_from_file(path_obj):
        """Evaluate sexpression in given file.
        """
        with path_obj.open() as fobj:
            expr = fobj.read()
        eval_sexp_str(expr)

    expr_path = Path(__file__).absolute().parents[1] / 'sexpressions'
    eval_from_file(expr_path / 'main.expr')
    if not IS_PYPY:
        eval_from_file(expr_path / 'cpython.expr')
    else:
        eval_from_file(expr_path / 'pypy.expr')

    eval_from_file(expr_path / 'del_hidden.expr')

    for syntax in {'for', 'each', 'while', 'break', 'continue'}:
        del syntax_table[syntax]
        del global_env[syntax]
        del global_scope[syntax]

    sys.path.append(os.getcwd())
    from ice.utils.importer import set_importer
    set_importer()


def _pyc_compile(in_file_name, env, out_file_name, show_tokens=False, optimize=-1):
    """Compile a Ice file into a Python bytecode file.
    """
    if not out_file_name:
        out_file = sys.stdout.buffer
    else:
        out_file = open(out_file_name, 'wb')
    target_ast = translator.translate_file(in_file_name, show_tokens=show_tokens)
    import_env_file = Path(__file__).absolute().parents[0] / env
    import_env_ast = translator.translate_file(import_env_file.as_posix())
    target_ast.body = import_env_ast.body + target_ast.body
    output_pyc(compile(target_ast, in_file_name, 'exec', optimize=optimize),
               buffer=out_file)


def pyc_compile(in_file_name, out_file_name=None, show_tokens=False, optimize=-1):
    env = GLOBAL_ENV
    _pyc_compile(in_file_name, env, out_file_name, show_tokens=show_tokens, optimize=optimize)


def parse_args():
    arg_parser = argparse.ArgumentParser(
        description='Ice is a functional programming language.')
    arg_parser.add_argument('-v', '--version', action='version',
                            version=__version__)
    arg_parser.add_argument('-c', '--compile', action='store_true',
                            help='Show marshalled code.')
    arg_parser.add_argument('-pyc', '--pyc-compile', action='store_true',
                            help='Generate Python bytecode from Ice file.')
    arg_parser.add_argument('-o', '--outfile', nargs='?', type=str,
                            help='Name of output file.')
    arg_parser.add_argument('-O', '--optimize', action='store_true',
                            help='Optimize generated bytecode slightly.')
    arg_parser.add_argument('-OO', '--optimize2', action='store_true',
                            help='Remove doc-strings in addition to the -O optimizations.')
    arg_parser.add_argument('-init', '--add-init-code', action='store_true',
                            help='Add Ice init code to Python source code '
                                 'files. This allows running the generated '
                                 'file from the command line with Python.')
    arg_parser.add_argument('-e', '--execute-compiled-file',
                            action='store_true')
    arg_parser.add_argument('file', nargs='?', type=str)
    arg_parser.add_argument('args', nargs='*', type=str)
    arg_parser.add_argument('--show-tokens', dest='tokens',
                            help='Shows the results of the tokenizing step.',
                            action='store_true')

    return arg_parser.parse_args()


def main():
    args = parse_args()
    init()
    if args.file:
        try:
            # env = GLOBAL_ENV

            if not (args.optimize or args.optimize2):
                optimize = 0
            elif args.optimize:
                optimize = 1
            else:
                optimize = 2

            if args.compile:
                output_code(compile_file(args.file,
                                         optimize,
                                         show_tokens=args.tokens))
            elif args.execute_compiled_file:
                execute_compiled_file(args.file)
            elif args.pyc_compile:
                pyc_compile(in_file_name=args.file,
                            out_file_name=args.outfile,
                            show_tokens=args.tokens,
                            optimize=optimize)
            else:
                sys.modules['__main__'] = global_env
                global_env['__file__'] = args.file
                load_file(args.file, global_env, optimize=optimize)
        except ParsingError as e:
                print(e, file=sys.stderr)
        except Exception:
                traceback.print_exc(file=sys.stderr)
        sys.exit(0)
    else:
        interact(args.tokens)


if __name__ == '__main__':
    main()
