# PsX Quick Reference Card

## 🚀 One-Page Syntax Guide

### Variables & Types
```psx
var name = "PsX"           // String
var age = 25               // Integer  
var score = 99.5           // Float
var active = true          // Boolean
var items = [1, 2, 3]      // Array
```

### Type Casting
```psx
int("123")      // → 123
float("45.67")  // → 45.67
str(99)         // → "99"
typeOf(value)   // → "int", "float", "string", "list"
```

### String Methods
```psx
str.trim("  hello  ")        // "hello"
str.toUpper("hello")         // "HELLO"
str.toLower("HELLO")         // "hello"
str.split("a,b,c", ",")      // ["a", "b", "c"]
str.replace("hi", "i", "a")  // "ha"
```

### Math Functions
```psx
math.round(99.8)     // 100
math.floor(99.8)     // 99
math.ceil(99.8)      // 100
math.abs(-42)        // 42
math.max(10, 50)     // 50
math.min(10, 50)     // 10
math.rand(1, 100)    // Random 1-100
```

### Array Operations
```psx
len([1, 2, 3])       // 3
arr.push(arr, 4)     // Add to end
arr.pop(arr)         // Remove from end
arr.join(arr, ",")   // "1,2,3"
arr[0]               // First element
```

### Operators
```psx
// Arithmetic
+, -, *, /, %, **

// Assignment
=, +=, -=, *=, /=, %=

// Increment/Decrement
x++, x--, ++x, --x

// Comparison
==, !=, >, <, >=, <=

// Logical
&&, ||, ! (coming soon)
```

### Control Flow
```psx
// If/Else
if (condition) {
    // code
} else if (condition) {
    // code  
} else {
    // code
}

// For Loop
for(int i = 0..10, +1) {
    print(i);
}

// While Loop
while (condition) {
    // code
}

// Do-While
do {
    // code
} while (condition);
```

### Functions
```psx
// Regular Function
func add(a, b) {
    return a + b;
}

// Arrow Function
var multiply = (a, b) => a * b;
var double = x => x * 2;
var greet = () => "Hello";

// Higher-Order Function
func calculate(op, a, b) {
    return op(a, b);
}
```

### Built-in Functions
```psx
print("Hello")        // Output
len(array)           // Array length  
typeOf(value)        // Get type
```

---

## 🎯 Language Philosophy

- **Hybrid**: Best of JavaScript + Python + C++
- **Muscle Memory**: Familiar operators from popular languages
- **Zero Ceremony**: Clean, minimal syntax
- **Progressive**: Easy start, powerful when needed

---

## 🔥 Quick Examples

### Hello World
```psx
print("Hello, PsX!");
```

### Basic Math
```psx
var x = 10;
x += 5;
print(x * 2);  // 30
```

### Array Processing
```psx
var nums = [1, 2, 3, 4, 5];
for(int i = 0..len(nums) - 1, +1) {
    print(nums[i] * 2);
}
```

### Function Example
```psx
var square = x => x * x;
print(square(5));  // 25
```

---

## 📁 File Structure
```
PsX/
├── src/
│   ├── lexer_mix.py      # Tokenizer
│   ├── parser_mix.py     # Parser  
│   ├── runtime_mix.py    # Interpreter
│   └── main_mix.py       # Entry point
├── examples/
│   ├── hello.psx         # Basic
│   ├── hello6.psx        # Functions
│   ├── meth.psx          # Methods
│   └── ultimate_mix.psx  # Complete
└── PSX_DOCUMENTATION.md  # Full docs
```

---

## 🚀 Run Code
```bash
python src/main_mix.py examples/ultimate_mix.psx
```

---

**PsX - Write Code That Feels Like Home** 🏠
