func list_seq() {
  let lis = [1, 2, 3]
  # Sequence pattern
  match lis {
    case [1, 2, x] -> { x }
    case _ -> { None }
  }
}

func result_list_seq() {
  3
}

func match_rest() {
  let lis = [1, 2, 3]
  match lis {
    case [1, &rest] -> { rest }
    case _ -> { None }
  }
}

func result_match_rest() {
  pvector([2, 3])
}

func map_pattern() {
  let foo_map = {'foo' : 'bar'}

  # Mapping pattern
  match foo_map {
    case {'foo' : value} -> { value }
    case _ -> { None }
  }
}

func result_map_pattern() {
  'bar'
}

func type_pattern() {
  # Type pattern
  # <name of variable refers to type> <pattern>: <action>
  match 10 {
    case x:int -> { 'int' }
    case x:float -> { 'float' }
    case x:str -> { 'str' }
    case x:bool -> { 'bool' }
    case _ -> { 'other' }
  }
}

func result_type_pattern() {
  'int'
}


func int_match() {
  match [1, 2, 3] {
    case [1, x:str, 3] -> { 'str' }
    case [1, x:int, 3] -> { 'int' }
    case _ -> { 'other' }
  }
}

func result_int_match() {
  'int'
}

func even_positive() {
  let Positive = predicate(=> $1 > 0)
  let Even = predicate(=> $1 % 2 == 0)
  let EvenAndPositive = predicate(=> ($1 % 2 == 0) and ($1 >= 0))

  match 10 {
    case n:EvenAndPositive -> {
      str(n) + ':Even and Positive'
    }
    case n:Even -> { str(n) + ':Even' }
    case n:Positive -> { str(n) + ':Positive' }
  }
}

func result_even_positive() {
  '10:Even and Positive'
}

func match_100() {
  match ['foo', 100] {
    case [x:predicate(=> $1 == 'foo'),
          value:predicate(=> 0 < $1 and $1 <= 100)] -> value
    case _ -> 10000
  }
}

func result_match_100() {
  100
}

func record_pattern() {
  # Record pattern
  record Person(name, age)

  let foo = Person('foo', 32)

  match foo {
    case Person('bar', age) -> {
      'bar:' + str(age)
    }
    case Person('foo', age) -> {
      'foo:' + str(age)
    }
    case _ -> None
  }
}

func result_record_pattern() {
  'foo:32'
}