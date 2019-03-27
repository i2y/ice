func create_tag_macro_body(tag_name, head, body) {
  let class_name = if len(head) == 0 {
    ''
  }
  else {
    first(head)
  }

  let children = if (body is None) or (len(body) == 0) {
    []
  }
  else {
    cdr(body)
  }

  quasi_quote {
    container_start_tag(unquote tag_name, unquote class_name)
    # write_to_buffer(unquote [quote v] + children)
    unquote_splicing children
    container_end_tag(unquote tag_name)
  }
}


record Attr(name) {
  func __getattr__(self, attr_name) {
    if len(self.name) == 0 {
      Attr(attr_name)
    }
    else {
      Attr(self.name + ' ' + attr_name)
    }
  }

  func __str__(self) {
    self.name
  }
}

let ui = Attr('ui')
