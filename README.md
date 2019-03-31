Ice
====
Ice is a dynamically typed programming language.

Its interpreter is written in Python3. The interpreter translates a program written in Ice to Python3's AST / bytecode.

**The implementation is based on [mochi](https://github.com/i2y/mochi).**

## Features
- Tail recursion optimization (self tail recursion only), and no loop syntax
- Re-assignments are not allowed in function definition.
- Basic collection type is a persistent data structure. (using Pyrsistent)
- Pipeline operator
- Syntax sugar of anonymous function definition
- Macro

## Examples
### Factorial
```
func factorial(n, m) {
    if n == 1 {
        m
    } else {
        factorial(n - 1, n * m)
    }
}


factorial(10000, 1)
# => 28462596809170545189064132121198688...
```

### FizzBuzz
```
func fizzbuzz(n) {
  match [n % 3, n % 5] {
    case [0, 0] -> "fizzbuzz"
    case [0, _] -> "fizz"
    case [_, 0] -> "buzz"
    case _ -> n
  }
}

range(1, 31)
|> map(fizzbuzz)
|> pvector()
|> print()
```

### Flask
```
from flask import Flask

let app = Flask('demo')

@app.route('/')
func hello() {
    'Hello World!'
}

app.run()
```

## Requirements
See requirements.txt


## Installation
```sh
$ pip3 install ice
```

## Usage

### REPL
```sh
$ ice
>>>
```

### loading and running a file
```sh
$ cat foo.ice
print('foo')
$ ice foo.ice
foo
```

### generating .pyc
```sh
$ ls
foo.ice
$ cat foo.ice
print('foo')
$ ice
>>> import foo
foo
>>> exit()
$ ls
foo.ice foo.pyc
$ python3 foo.pyc
foo
```

Or

```sh
$ ice -pyc foo.ice > foo.pyc
$ python3 foo.pyc
foo
```

## Examples for each feature

### Persistent data structures
```
[1, 2, 3]
# => pvector([1, 2, 3])

v(1, 2, 3)
# => pvector([1, 2, 3])

let vec = [1, 2, 3]
let vec2 = vec.set(0, 8)
# => pvector([8, 2, 3]
vec
# => pvector([1, 2, 3])
let [x, y, z] = vec
x # => 1
y # => 2
z # => 3

get(vec, 0) # => 1
get(vec, 0, 2) # => [1, 2]

vec[0] # => 1
vec[0:2] # => [1, 2]

{'x': 100, 'y': 200}
# => pmap({'y': 200, 'x': 100})

let ma = {'x': 100, 'y': 200}
ma.get('x') # => 100
ma.x # => 100
ma['x'] # => 100
let ma2 = ma.set('x', 10000)
# => pmap({'y': 200, 'x': 10000})
ma # => pmap({'y': 200, 'x': 100})
get(ma, 'y') # => 200
ma['y'] # => 200

m(x=100, y=200)
# => pmap({'y': 200, 'x': 100})

s(1, 2, 3)
# => pset([1, 2, 3])

b(1, 2, 3)
# => pbag([1, 2, 3])
```

### Function definitions
```python
func hoge(x) {
    'hoge' + str(x)
}

hoge(3)
# => hoge3
```


### Bindings
```
let x = 3000
# => 3000

let [a, b] = [1, 2]
a
# => 1
b
# => 2

let [c, &d] = [1, 2, 3]
c
# => 1
d
# => pvector([2, 3])
```

### Data types
```
data Point {
    Point2D(x, y)
    Point3D(x, y, z)
}

let p1 = Point2D(x=1, y=2)
# => Point2D(x=1, y=2)

let p2 = Point2D(3, 4)
# => Point2D(x=3, y=4)

p1.x
# => 1
```

## TODO
- **Improve documentation**

## License
MIT License

## Contributors
https://github.com/i2y/ice/graphs/contributors
