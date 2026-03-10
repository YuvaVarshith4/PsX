# PsX - The Hybrid Programming Language

## Overview

PsX is a modern, hybrid programming language designed for developers who want the best of multiple worlds. It combines the readability of Python, the flexibility of JavaScript, and the performance mindset of C/C++. PsX is built to be **super-friendly**, **habitual**, and **muscle-memory optimized** for developers coming from popular languages.

## Philosophy

- **Hybrid by Design**: Borrow the best syntax patterns from multiple languages
- **Muscle Memory Friendly**: Use familiar operators and structures
- **Zero Ceremony**: Clean, concise syntax without boilerplate
- **Progressive Power**: Easy to start, powerful when you need it
- **Developer Joy**: Write code that feels natural and intuitive

## Language Features

### 🎯 Core Characteristics

- **Dynamic Typing** with optional type hints
- **First-Class Functions** with arrow syntax
- **Modern Operators** (`++`, `--`, `+=`, `-=`, `*=`, `/=`, `%=`)
- **Built-in Methods** for strings, arrays, and math
- **Comprehensive Control Flow** (if/else, for, while, do-while)
- **Function Closures** and higher-order programming
- **Array Literals** and operations
- **Type Casting** utilities

### 🚀 Unique Hybrid Features

1. **JavaScript-style arrow functions**: `x => x * 2`
2. **Python-style string methods**: `str.trim()`, `str.split()`
3. **C-style operators**: `++`, `--`, `+=`, etc.
4. **Ruby-style range loops**: `for(int i = 0..10, +1)`
5. **Shell-style comments**: `# Comment` and `// Comment`
6. **Universal print function**: `print("Hello")`

---

## Syntax Reference

### 1. Variables and Data Types

```psx
// Variable declaration
var name = "PsX Developer";
var age = 25;
var score = 99.5;
var isActive = true;

// Arrays
var numbers = [1, 2, 3, 4, 5];
var mixed = ["hello", 42, true];

// Type casting
var strNum = "123";
var actualNum = int(strNum);        // String to int
var floatNum = float("45.67");      // String to float
var strVal = str(99);               // Number to string
```

### 2. String Operations

```psx
var text = "   Hello PsX World!   ";

// Built-in string methods
print(str.trim(text));              // "Hello PsX World!"
print(str.toUpper(text));           // "HELLO PSX WORLD!"
print(str.toLower(text));           // "hello psx world!"
print(str.split(text, " "));        // ["Hello", "PsX", "World!"]
print(str.replace(text, "PsX", "JavaScript")); // "Hello JavaScript World!"
```

### 3. Mathematical Operations

```psx
// Basic arithmetic
var result = 10 + 5 * 2 - 3;       // 17
var power = 2 ** 8;                 // 256

// Advanced operators
var x = 10;
x++;                                // 11
x--;                                // 10
x += 5;                             // 15
x -= 2;                             // 13
x *= 3;                             // 39
x /= 2;                             // 19.5
x %= 7;                             // 5.5

// Math functions
print(math.round(99.8));            // 100
print(math.floor(99.8));            // 99
print(math.ceil(99.8));             // 100
print(math.abs(-42));               // 42
print(math.max(10, 50));            // 50
print(math.min(10, 50));            // 10
print(math.rand(1, 100));           // Random number 1-100
```

### 4. Array Operations

```psx
var fruits = ["apple", "banana", "cherry"];

// Array methods
print(len(fruits));                  // 3
print(fruits[1]);                    // "banana"

// Array manipulation
arr.push(fruits, "orange");          // Add to end
var popped = arr.pop(fruits);       // Remove from end
print(arr.join(fruits, ", "));       // "apple, banana, cherry"

// Array assignment
fruits[0] = "avocado";               // Update element
```

### 5. Control Flow

#### If/Else Statements
```psx
var score = 85;

if (score >= 90) {
    print("Grade: A - Excellent!");
} else if (score >= 80) {
    print("Grade: B - Good!");
} else if (score >= 70) {
    print("Grade: C - Average");
} else {
    print("Grade: F - Need improvement");
}
```

#### For Loops
```psx
// Range-based for loop
for(int i = 0..10, +1) {
    print("Count: " + i);
}

// Reverse range
for(int i = 10..0, -2) {
    print("Reverse: " + i);
}

// Nested loops
for(int i = 1..3, +1) {
    for(int j = 1..3, +1) {
        print(i + " * " + j + " = " + (i * j));
    }
}
```

#### While Loops
```psx
var count = 0;
while(count < 5) {
    print("While: " + count);
    count = count + 1;
}
```

#### Do-While Loops
```psx
var doCount = 0;
do {
    print("Do-While: " + doCount);
    doCount = doCount + 1;
} while(doCount < 3);
```

### 6. Functions

#### Regular Functions
```psx
// Basic function
func add(a, b) {
    return a + b;
}

// Function without parameters
func greet() {
    print("Hello from PsX!");
}

// Function without return value
func printSquare(n) {
    var square = n * n;
    print("Square of " + n + " is " + square);
}

// Recursive function
func factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
```

#### Arrow Functions
```psx
// Single expression
var multiply = (a, b) => a * b;

// Single parameter (no parentheses)
var double = x => x * 2;

// No parameters
var getRandom = () => math.rand(1, 100);

// Multi-line body
var complexCalc = (x, y) => {
    var temp = x + y;
    return temp * 2;
};
```

#### Higher-Order Functions & Callbacks
```psx
// Function that takes another function
func calculate(operation, a, b) {
    print("Performing operation...");
    return operation(a, b);
}

// Using callbacks
var sum = calculate((x, y) => x + y, 10, 5);
var diff = calculate(subtract, 10, 5);

// Function factory (closure)
func createMultiplier(factor) {
    return x => x * factor;
}

var triple = createMultiplier(3);
print(triple(8));                   // 24
```

### 7. Type Checking

```psx
var value = 42;
print(typeOf(value));               // "int"

var text = "hello";
print(typeOf(text));                // "string"

var arr = [1, 2, 3];
print(typeOf(arr));                 // "list"
```

---

## Language Design Principles

### 1. Muscle Memory Optimization

PsX uses operators and syntax patterns that developers already know:

- **C/C++/JavaScript**: `++`, `--`, `+=`, `-=`, `*=`, `/=`, `%=`
- **Python**: `len()`, `str.upper()`, `str.lower()`
- **JavaScript**: `=>` arrow functions, array methods
- **Shell**: `#` and `//` comments
- **Ruby**: Range syntax `0..10`

### 2. Zero Ceremony

No unnecessary boilerplate:

```psx
// No type declarations needed
var name = "PsX";

// No semicolons required for simple statements
print("Hello")

// But semicolons work when you want them
print("Hello");  // Also valid
```

### 3. Progressive Power

Start simple, grow powerful:

```psx
// Beginner level
var x = 10;
print(x);

// Intermediate level
func add(a, b) {
    return a + b;
}

// Advanced level
var processor = data => {
    return data
        .filter(x => x > 0)
        .map(x => x * 2)
        .reduce((a, b) => a + b, 0);
};
```

---

## Standard Library

### String Methods
- `str.trim(string)` - Remove whitespace
- `str.toUpper(string)` - Convert to uppercase
- `str.toLower(string)` - Convert to lowercase
- `str.split(string, delimiter)` - Split into array
- `str.replace(string, old, new)` - Replace substring

### Math Functions
- `math.round(number)` - Round to nearest integer
- `math.floor(number)` - Round down
- `math.ceil(number)` - Round up
- `math.abs(number)` - Absolute value
- `math.max(a, b)` - Maximum of two numbers
- `math.min(a, b)` - Minimum of two numbers
- `math.rand(min, max)` - Random number in range

### Array Methods
- `len(array)` - Get array length
- `arr.push(array, element)` - Add element to end
- `arr.pop(array)` - Remove and return last element
- `arr.join(array, separator)` - Join elements into string

### Type Functions
- `int(value)` - Convert to integer
- `float(value)` - Convert to float
- `str(value)` - Convert to string
- `typeOf(value)` - Get type name

---

## Examples and Use Cases

### 1. Data Processing Pipeline
```psx
func processUserData(name, age, scores) {
    var formattedName = str.toUpper(str.trim(name));
    var average = 0;
    
    for(int i = 0..len(scores) - 1, +1) {
        average = average + scores[i];
    }
    average = average / len(scores);
    
    var grade;
    if (average >= 90) grade = "A";
    else if (average >= 80) grade = "B";
    else if (average >= 70) grade = "C";
    else grade = "F";
    
    return formattedName + " - Grade: " + grade + " - Avg: " + math.round(average);
}
```

### 2. Functional Programming
```psx
var numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Process even numbers and square them
var evenSquares = numbers
    .filter(x => x % 2 == 0)
    .map(x => x * 2);

print("Even doubles: " + arr.join(evenSquares, ", "));
```

### 3. Algorithm Implementation
```psx
func fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

func isPalindrome(str) {
    var clean = str.toLower(str.trim(str));
    var reversed = "";
    
    for(int i = len(clean) - 1..0, -1) {
        reversed = reversed + clean[i];
    }
    
    return clean == reversed;
}
```

---

## Why PsX?

### For JavaScript Developers
- Arrow functions feel familiar: `x => x * 2`
- Array methods work naturally: `arr.push()`, `arr.pop()`
- Operators are the same: `++`, `--`, `+=`

### For Python Developers
- String methods are intuitive: `str.trim()`, `str.upper()`
- Dynamic typing feels natural
- Clean, readable syntax

### For C/C++ Developers
- Performance-oriented operators
- Familiar control structures
- Type casting functions

### For Beginners
- No complex syntax to learn
- Progressive learning curve
- Immediate feedback with `print()`

---

## Getting Started

### Installation
```bash
# Clone the repository
git clone https://github.com/YuvaVarshith4/PsX.git

# Run a PsX file
python src/main_mix.py examples/ultimate_mix.psx
```

### First Program
```psx
// hello.psx
var message = "Hello, PsX!";
print(message);

var numbers = [1, 2, 3, 4, 5];
for(int i = 0..len(numbers) - 1, +1) {
    print("Square of " + numbers[i] + " is " + (numbers[i] * numbers[i]));
}
```

### Running Examples
```bash
# Basic examples
python src/main_mix.py examples/hello.psx
python src/main_mix.py examples/comprehensive.psx

# Advanced features
python src/main_mix.py examples/hello6.psx      # Functions
python src/main_mix.py examples/meth.psx         # Methods & operators
python src/main_mix.py examples/ultimate_mix.psx # Complete showcase
```

---

## Language Comparison

| Feature | PsX | JavaScript | Python | C++ |
|---------|-----|------------|---------|-----|
| Arrow Functions | `x => x * 2` | `x => x * 2` | `lambda x: x * 2` | N/A |
| String Methods | `str.trim()` | `str.trim()` | `str.strip()` | N/A |
| Array Length | `len(arr)` | `arr.length` | `len(arr)` | `arr.size()` |
| Increment | `x++` | `x++` | `x += 1` | `x++` |
| Range Loop | `for(i = 0..10, +1)` | `for(let i=0; i<10; i++)` | `for i in range(10)` | `for(int i=0; i<10; i++)` |
| Comments | `#` and `//` | `//` and `/* */` | `#` | `//` and `/* */` |

---

## Future Roadmap

### Phase 1: Core Language ✅
- [x] Basic syntax and operators
- [x] Control flow structures
- [x] Functions and closures
- [x] Arrays and strings
- [x] Standard library

### Phase 2: Advanced Features
- [ ] Object-oriented programming
- [ ] Module system
- [ ] Error handling
- [ ] File I/O operations
- [ ] Regular expressions

### Phase 3: Ecosystem
- [ ] Package manager
- [ ] Standard library expansion
- [ ] Web framework
- [ ] Database connectors
- [ ] Testing framework

---

## Contributing

PsX is open-source and welcomes contributions! Here's how to get involved:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Keep the language simple and intuitive
- Maintain backward compatibility
- Write comprehensive tests
- Document new features
- Follow the hybrid design principles

---

## Community

- **GitHub**: https://github.com/YuvaVarshith4/PsX
- **Issues**: Report bugs and request features
- **Discussions**: Language design and usage
- **Examples**: Share your PsX code

---

## License

PsX is licensed under the MIT License. See LICENSE file for details.

---

## Acknowledgments

PsX stands on the shoulders of giants. We thank:
- JavaScript for arrow functions and dynamic nature
- Python for readability and standard library design
- C/C++ for performance-oriented operators
- Ruby for elegant range syntax
- Shell scripting for comment styles

---

**PsX - Where Multiple Languages Meet in Perfect Harmony** 🚀

*Write code that feels like home, no matter where you come from.*
