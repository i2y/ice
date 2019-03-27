# use x, y, z from fafa

macro pipeline(head, body, rest) {
  cons(Symbol('|>'),
     cons(car(head),
        cdr(body)))
}

func use_pipeline() {
  pipeline [1, 2, 3] {
    map(=> $1 * 2)
    filter(=> $1 != 2)
    pvector()
  }
}

func result_use_pipeline() {
  [4, 6]
}

let buffer = list()


func write_to_buffer(content) {
  buffer.extend(content)
}

macro div(head, body, rest) {
  from helper import create_tag_macro_body
  create_tag_macro_body('div', head, body)
}

func container_start_tag(tag_name, class_attr) {
  write_to_buffer(['<' + tag_name + ' class="' + str(class_attr) + '">'])
}

func container_end_tag(tag_name) {
  write_to_buffer(['</' + tag_name + '>'])
}

func img_tag(class_attr, src_url) {
  write_to_buffer(['<img class_attr="' + str(class_attr) + '" src="' + src_url + '"/>'])
}

macro img(head, body, rest) {
  if body is None {
    quasi_quote {
      img_tag('', unquote first(head))
    }
  }
  else {
    quasi_quote {
      img_tag(unquote first(head), unquote body)
    }
  }
}

func code_block(lang, code) {
  write_to_buffer([get_highlight_html(lang, code)])
}

macro code(head, body, rest) {
  let [lang] = head
  quasi_quote {
    code_block(unquote lang, unquote body)
  }
}


macro s(head, body, rest) {
  if body is None {
    quasi_quote {
      write_to_buffer([str(unquote first(head))])
    }
  }
  else {
    raise Exception('syntax error')
  }
}

macro p(head, body, rest) {
  if body is None {
    quasi_quote {
      write_to_buffer(['<p>' + str(unquote first(head)) + '</p>'])
    }
  }
  else {
    raise Exception('syntax error')
  }
}

from helper import ui
from py_helper import get_highlight_css, get_highlight_html

func _wrap(html_fragment) {
  '<html><head>'
  + '<meta charset="utf-8" />'
  + '<title>Semantic PDF</title>'
  + '<link rel="stylesheet" href="semantic.css"/>'
  + '<style>' + get_highlight_css() + '</style>'
  + '</head><body>'
  + html_fragment
  + '</body></html>'
}

func _generate(path, body) {
  let joinable_buffer = filter(=> not ($1 is None),
                 buffer)
  ''.join(joinable_buffer)
  |> _wrap
  |> print
}

macro generate(head, body, rest) {
  quasi_quote {
    _generate(unquote first(head),
          unquote body)
  }
}


let username = 'i2y'

# joinable_buffer = filter(buffer) => not ($1 is None)
# ''.join(joinable_buffer) |> print


macro segment(head, body, rest) {
  quasi_quote {
     div ui.segment {
       unquote body
     }
  }
}


macro card(head, body, rest) {
  quasi_quote {
     div ui.card {
       unquote body
     }
  }
}


macro content(head, body, rest) {
  quasi_quote {
     div ui.content {
       unquote body
     }
  }
}


macro header(head, body, rest) {
  quasi_quote {
     div ui.header {
       unquote body
     }
  }
}


generate 'test.pdf' {
  segment {
    if username == 'i2y' {
      p username + '!!!'
      p 'aiueo'
      s 'fafafafafa'
      if False {
        s 'fafafafafafafaf'
      }
      else {
        s "ffffff"
      }
    }
    else {
      p 'error!'
    }
  }

  card {
    content {
      header {
        s 'ほげほげ'
      }
    }
    content {
      code 'python' {
        """
func python():
  x = 3
  return x"""
      }
      div ui.content {
        div ui.sub.header {
          p 'result'
        }
        p '結果'
      }
    }
  }
}

infix_2 macro add(a, b) {
  quasi_quote {
    (unquote a) + (unquote b)
  }
}

infix macro to(a, b) {
  quasi_quote {
    tuple([unquote a, unquote b])
  }
}

macro sub(head, body, rest) {
  1000
}

print(1 add 2)
print(sub 1)
print(100 * 100 to 100 + 200)
print('a' to 100 + 200)
print('a' to 100 add 200 * 100 * 300)

macro fafa(head, body, rest) {
  print(rest)
  2000
}

let y = 10000



fafa 10 {
  1000
}
elif 300 > 200 {
  2000
}
else {
  3000
}

# let y = 5000
# print(y)

fafa 10 {
  1000
}
elif 300 > 200 {
  2000
}
else {
  3000
}

use {
  hoge from hoge_macro
}

hoge True {  3000 }
hogehoge  {
  1000
}

# generate 'fafa.pdf':
#   segment:
#     p 'aiueo'

# generate 'aiue.pdf':
#   div ui.three.column.very.relaxed.grid:
#     div ui.column:
#       p 'aiueo'
#     div ui.vertical.divider:
#       s 'not'
#     div ui.column:
#       p 'aiueo'
#     div ui.vertical.divider:
#       s 'not'
#     div ui.column:
#       p 'aiueo'

record Hoge(x, y)

record F(x, y)
let F(F(x=xxx, y=yyy),
    fafa_y) = F(F(x=1, y=2), 2)
print(xxx)

let [fafa_x] = {'x': 100}.values()
print(fafa_x)

match F(1, 2) {
  case F(fafa3,
       fafa4) -> {
    True
  }
}
print(fafa4)

# z = quote func x(y):
#   return y
# print(z)