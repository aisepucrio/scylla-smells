
# **Scylla: A Tool for Detecting Code Smells in Python**

Scylla is a static analysis tool designed to detect **code smells** in Python source code. It aims to support both researchers and developers by identifying poor design practices that impact maintainability and code quality.

The tool currently detects the following code smells:

1. **Long Method**
2. **Long Parameter List**
3. **Large Class**
4. **Lazy Class**
5. **Data Class**
6. **Magic Number**

> Scylla is open source and designed with modularity, explainability, and extensibility in mind.

---

## **Technologies Used**

- **[Pylint](https://pylint.pycqa.org/):** Integrated for detection of unused variables, imports, and some metrics like number of arguments.
- **AST (Abstract Syntax Tree):** Used to analyze Python code structure and extract methods, classes, inheritance, etc.
- **Python 3.10+**

---

## **Code Smells Detected**

### 1. **Long Method**
- **Description:** Methods with too many lines of code hinder readability and maintainability.
- **Threshold:** Methods with more than **67 lines**.
- **Detection:** Counted via AST traversal and line analysis.

### 2. **Long Parameter List**
- **Description:** Functions or methods with too many input parameters.
- **Threshold:** **5 or more parameters**.
- **Detection:** Detected using Pylint’s message `R0913`, cross-verified with AST.

### 3. **Large Class**
- **Description:** Classes with too many methods or attributes.
- **Thresholds:**
  - More than **200 lines**, or
  - Total number of methods and attributes **≥ 40**
- **Detection:** Combined analysis using AST and Pylint messages `R0902`, `R0904`.

### 4. **Lazy Class**
- **Description:** Classes with too few responsibilities.
- **Thresholds:**
  - Less than **5 methods** and less than **5 attributes**, or
  - Inheritance depth **< 2**
- **Detection:** AST-based structural analysis.

### 5. **Data Class**
- **Description:** Classes that only store data with no meaningful behavior.
- **Thresholds:**  
  - **LWMC > 50** or **LCOM > 0.8**
- **Detection:** Uses Radon and LCOM external metrics.

### 6. **Magic Number**
- **Description:** Usage of literal numbers in code without symbolic constants.
- **Detection:** Any numeric literal other than `0`, `1`, or `-1` not assigned to a variable.

---

## **How to Use**

### 1. **Install Dependencies**
```bash
pip install pylint
```

### 2. **Run the Tool**
You can analyze a specific file or a folder (non-recursive).
```bash
Change the path to where you want Scylla to analyze inside the main file, line 85
python main.py
```

### 3. **Output**
- A CSV file will be generated containing:
  - File name
  - Start and end lines
  - Code smell type
  - Description

> JSON output support is currently under development.

---

## **Architecture**

Scylla is organized into four main modules:
- `main.py` — central controller
- `smells/` — detection engine (heuristic logic)
- `pylint_wrapper/` — handles static analysis from Pylint
- `utils/` — helper functions

The analysis workflow follows:  
**Input → Static Analysis → Smell Detection → Report Generation**


---

## **Demo Video**

📺 Watch the video demo:  
[https://doi.org/10.5281/zenodo.15500180](https://doi.org/10.5281/zenodo.15500180)

---

## **Contributors**
- Gabriel Gervasio  
- Jessica Ribas  
- Guilherme Cunha  
- Joanne Carneiro  
- Juliana Alves Pereira
