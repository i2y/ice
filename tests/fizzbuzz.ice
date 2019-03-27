func fizzbuzz(n) {
  match [n % 3, n % 5] {
    case [0, 0] -> "fizzbuzz"
    case [0, _] -> "fizz"
    case [_, 0] -> "buzz"
    case _ -> n
  }
}