func newline_dot_name_case_1() {
  let obj = object()
  obj.__class__
}


func result_newline_dot_name_case_1() {
  object
}


func newline_dot_name_case_2() {
  let obj = object()
  obj
     .__class__
}

func result_newline_dot_name_case_2() {
  object
}

func newline_dot_name_case_3() {
  let obj = object()
  obj.__class__
     .__class__
}

func result_newline_dot_name_case_3() {
  type
}

func newline_dot_name_case_4() {
  object().__class__
      .__class__
}

func result_newline_dot_name_case_4() {
  type
}

func newline_dot_name_case_5() {
  let obj = object().__class__
            .__class__
  obj
}

func result_newline_dot_name_case_5() {
  type
}

func newline_dot_name_case_6() {
  'foo'.title()
     .__add__('_bar')
}

func result_newline_dot_name_case_6() {
  'Foo_bar'
}

func newline_dot_name_case_7() {
  'foo'.title()
     + '_bar'
     .title()
}

func result_newline_dot_name_case_7() {
  'Foo_Bar'
}

func newline_dot_name_case_8() {
  'foo'.title()
     + '_bar'
     .title()
}

func result_newline_dot_name_case_8() {
  'Foo_Bar'
}

func newline_dot_name_case_9() {
  let lis = [1, 2, 3]
  let lis2 = lis.set(3, 4)
          .set(4, 5)
          .set(0, 10)
  lis + lis2
}

func result_newline_dot_name_case_9() {
  [1, 2, 3, 10, 2, 3, 4, 5]
}