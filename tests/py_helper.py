from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

__builtins__['ice_eval'] = eval
__builtins__['eval'] = py_eval


def get_highlight_css():
    return HtmlFormatter(style='colorful').get_style_defs('.highlight')
    # return HtmlFormatter(style='arduino').get_style_defs('.highlight')


def get_highlight_html(lang, code):
    lexer = get_lexer_by_name(lang)
    formatter = HtmlFormatter()
    return highlight(code, lexer, formatter)
