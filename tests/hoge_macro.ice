macro hoge(head, body, rest) {
  quasi_quote {
    print(unquote first(head))
  }
}

func get_keywords() {
  return {'hoge': ['hogehoge']}
}
