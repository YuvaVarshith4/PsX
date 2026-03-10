# PsX Language Examples

## 📁 Example Files Overview

| File | Purpose | Key Features |
|------|---------|-------------|
| `hello.psx` | Basic introduction | Variables, print, if/else |
| `hello2.psx` | Conditions | If/else logic |
| `hello3.psx` | For loops | Range-based iteration |
| `hello4.psx` | While loops | While & do-while |
| `hello5.psx` | Nested loops | Complex patterns |
| `hello6.psx` | Functions | Functions, callbacks, closures |
| `comprehensive.psx` | All control flow | Complete showcase |
| `meth.psx` | Methods & operators | String, math, array methods |
| `ultimate_mix.psx` | Complete hybrid | All features integrated |

---

## 🚀 Ultimate Mix Example

```psx
// ultimate_mix.psx - The Complete PsX Hybrid Engine Showcase

print("=========================================");
print("🚀 PSX ULTIMATE HYBRID ENGINE SHOWCASE 🚀");
print("=========================================");

// 1. String Manipulation, Type Casting & Arrays
var rawInput = "   Alex:72, Ron:80, John:99, Steve:43   ";
var cleanInput = str.trim(rawInput);
var records = str.split(cleanInput, ",");
print("Total records found: " + len(records));

// 2. Higher-Order Functions, Closures & Arrow Functions
var processRecord = (record) => {
    var parts = str.split(record, ":");
    var name = str.toUpper(parts[0]);
    var score = int(parts[1]) + 3;  // Bonus points
    var status = score >= 50 ? "PASS" : "FAIL";
    return " -> " + name + " (" + score + ") - " + status;
};

// 3. Dynamic Array Operations
var auditLog = ["INIT_AUDIT"];
arr.push(auditLog, "DATA_PROCESSED");
arr.push(auditLog, "PENDING_REVIEW");

// 4. Complex Math & Nested Scoping
func calculateMagicMetric(base, multiplier, offset) {
    var inner = (x) => x * multiplier + offset;
    return math.sqrt(inner(base)) * 2.5;
}

// 5. Standalone Control Flow
var x = 4;
if (x > 5) {
    print(" -> x is greater than 5");
} else {
    print(" -> x is 5 or less");
}

// 6. Increments & Replacements
var counter = 0;
counter++;
counter++;
print("Counter after two ++ operations: " + counter);
```

### Output:
```
=========================================
🚀 PSX ULTIMATE HYBRID ENGINE SHOWCASE 🚀
=========================================

[1] Data Ingestion & String Methods
Raw Input: [   Alex:72, Ron:80, John:99, Steve:43   ]
Total records found: 4

[2] Callbacks & Array Mapping
Processed Results:
 -> ALEX (75) - PASS
 -> RON (82) - PASS
 -> JOHN (100) - PASS
 -> STEVE (44) - FAIL

[3] Dynamic Array Operations
Popped State: ERROR_STATE
Current Audit Log: INIT_AUDIT | DATA_PROCESSED | PENDING_REVIEW

[4] Complex Math & Nested Scoping
Calculated Magic Metric: 26.0

[5] Standalone Control Flow
Testing standalone condition: is x (4) > 5?
 -> x is 5 or less

[6] Increments & Replacements
Counter after two ++ operations: 2
Final Verdict: Building PsX is INCREDIBLE
```

---

## 🎯 Feature-Specific Examples

### String Processing Pipeline
```psx
func processText(text) {
    // Clean and normalize
    var clean = str.trim(text);
    var upper = str.toUpper(clean);
    
    // Split and process
    var words = str.split(upper, " ");
    var processed = [];
    
    for(int i = 0..len(words) - 1, +1) {
        if (len(words[i]) > 3) {
            arr.push(processed, words[i]);
        }
    }
    
    return arr.join(processed, " ");
}

var result = processText("   hello world from psx language   ");
print(result); // "HELLO WORLD FROM PSX LANGUAGE"
```

### Mathematical Calculator
```psx
func calculator(operation, a, b) {
    switch (operation) {
        case "+": return a + b;
        case "-": return a - b;
        case "*": return a * b;
        case "/": return a / b;
        case "^": return a ** b;
        case "%": return a % b;
        default: return "Invalid operation";
    }
}

// Usage
print(calculator("+", 10, 5));  // 15
print(calculator("^", 2, 8));   // 256
print(calculator("%", 10, 3));  // 1
```

### Array Processing with Callbacks
```psx
func processData(data, filterFn, transformFn) {
    var results = [];
    var index = 0;
    
    for(int i = 0..len(data) - 1, +1) {
        var item = data[i];
        if (filterFn(item)) {
            var transformed = transformFn(item);
            results[index] = transformed;
            index++;
        }
    }
    
    return results;
}

var numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Get even numbers and double them
var evenDoubles = processData(
    numbers,
    x => x % 2 == 0,           // Filter: even only
    x => x * 2                 // Transform: double
);

print("Even doubles: " + arr.join(evenDoubles, ", "));
// Output: "4, 8, 12, 16, 20"
```

### Function Factory & Closures
```psx
func createMultiplier(factor) {
    return (number) => {
        return number * factor;
    };
}

func createGreeter(greeting) {
    return (name) => {
        var formattedName = str.toUpper(str.trim(name));
        return greeting + ", " + formattedName + "!";
    };
}

// Usage
var triple = createMultiplier(3);
var helloGreeter = createGreeter("Hello");

print(triple(8));                    // 24
print(helloGreeter("  john  "));     // "Hello, JOHN!"
```

### Recursive Algorithms
```psx
// Fibonacci sequence
func fibonacci(n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

// Factorial calculation
func factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

// Palindrome checker
func isPalindrome(str) {
    var clean = str.toLower(str.trim(str));
    var reversed = "";
    
    for(int i = len(clean) - 1..0, -1) {
        reversed = reversed + clean[i];
    }
    
    return clean == reversed;
}

// Test
print("Fibonacci(10): " + fibonacci(10));     // 55
print("Factorial(5): " + factorial(5));         // 120
print("Is 'Racecar' palindrome: " + isPalindrome("Racecar")); // true
```

### Complex Data Structures
```psx
// Student grade processing
func processStudentGrades(students) {
    var results = [];
    
    for(int i = 0..len(students) - 1, +1) {
        var student = students[i];
        var name = student[0];
        var grades = student[1];
        
        // Calculate average
        var sum = 0;
        for(int j = 0..len(grades) - 1, +1) {
            sum = sum + grades[j];
        }
        var average = sum / len(grades);
        
        // Assign grade
        var letterGrade;
        if (average >= 90) letterGrade = "A";
        else if (average >= 80) letterGrade = "B";
        else if (average >= 70) letterGrade = "C";
        else if (average >= 60) letterGrade = "D";
        else letterGrade = "F";
        
        // Store result
        results[i] = {
            "name": name,
            "average": math.round(average),
            "grade": letterGrade
        };
    }
    
    return results;
}

// Usage
var studentData = [
    ["Alice", [85, 92, 78, 90]],
    ["Bob", [76, 88, 91, 82]],
    ["Charlie", [92, 95, 89, 94]]
];

var processed = processStudentGrades(studentData);
for(int i = 0..len(processed) - 1, +1) {
    var result = processed[i];
    print(result["name"] + ": " + result["average"] + " (" + result["grade"] + ")");
}
```

---

## 🔥 Real-World Use Cases

### Data Analysis Pipeline
```psx
func analyzeSalesData(salesRecords) {
    var totalSales = 0;
    var productSales = {};
    
    for(int i = 0..len(salesRecords) - 1, +1) {
        var record = salesRecords[i];
        var product = record["product"];
        var amount = record["amount"];
        
        totalSales = totalSales + amount;
        
        if (product in productSales) {
            productSales[product] = productSales[product] + amount;
        } else {
            productSales[product] = amount;
        }
    }
    
    return {
        "total": totalSales,
        "byProduct": productSales,
        "average": totalSales / len(salesRecords)
    };
}
```

### Configuration Manager
```psx
func createConfigManager(defaults) {
    var config = {};
    
    // Copy defaults
    for(key in defaults) {
        config[key] = defaults[key];
    }
    
    return {
        "get": (key) => config[key],
        "set": (key, value) => { config[key] = value; },
        "reset": (key) => { config[key] = defaults[key]; },
        "getAll": () => config
    };
}

// Usage
var appConfig = createConfigManager({
    "debug": false,
    "version": "1.0.0",
    "timeout": 30
});

appConfig.set("debug", true);
print("Debug mode: " + appConfig.get("debug"));
```

### Simple Web Server Simulation
```psx
func createServer() {
    var routes = {};
    
    func addRoute(path, handler) {
        routes[path] = handler;
    }
    
    func handleRequest(path, data) {
        if (path in routes) {
            return routes[path](data);
        } else {
            return "404 Not Found";
        }
    }
    
    return {
        "addRoute": addRoute,
        "handleRequest": handleRequest
    };
}

// Usage
var server = createServer();
server.addRoute("/hello", (name) => "Hello, " + name + "!");
server.addRoute("/square", (num) => str(int(num) * int(num)));

print(server.handleRequest("/hello", "PsX"));    // "Hello, PsX!"
print(server.handleRequest("/square", "5"));      // "25"
```

---

## 📚 Learning Path

1. **Start with `hello.psx`** - Basic syntax
2. **Try `comprehensive.psx`** - Control flow
3. **Explore `hello6.psx`** - Functions
4. **Master `meth.psx`** - Built-in methods
5. **Conquer `ultimate_mix.psx`** - Everything together

Each example builds on the previous one, creating a complete learning journey from basics to advanced features.

---

**PsX Examples - From Hello World to Real-World Applications** 🎯
