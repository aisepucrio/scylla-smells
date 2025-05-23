# code_smell_checkers.py

import ast
import os
import re
import subprocess
from typing import List, Tuple
from collections import defaultdict
from funcAux import detect_unused_functions_with_lines, detect_unused_classes_with_lines, contar_linhas_classe

#--------------------------------------------------------------------------------------#
def check_too_many_arguments(file_path, pylint_output):
    """Verifica e retorna as linhas com funções contendo muitos argumentos."""
    too_many_args_matches = re.findall(r"(\d+):\d+: R0913: Too many arguments \((\d+)/[^\)]+\)", pylint_output)
    code_smells = []
    
    for line_number, num_arguments in too_many_args_matches:
        line_number = int(line_number)
        num_arguments = int(num_arguments)
        description = f"A função possui {num_arguments} argumentos, excedendo o limite recomendado."
        code_smells.append((file_path, line_number, line_number, "Too Many Arguments", description))
    
    return code_smells


#--------------------------------------------------------------------------------------#
def check_long_method(file_path, max_lines=67):
    """Verifica e retorna as linhas de funções que excedem um limite de linhas."""

    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    function_start = None
    functions_with_long_methods = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("def "):
            if function_start is not None and (i - function_start) > max_lines:
                linhas = contar_linhas_classe(file_path, function_start)
                functions_with_long_methods.append((file_path, function_start + 1, function_start+linhas , "Long Method"," Total de linhas: " + str(i - function_start)))
                
            function_start = i
    
    if function_start is not None and (len(lines) - function_start) > max_lines:
        linhas = contar_linhas_classe(file_path, function_start)
        functions_with_long_methods.append((file_path, function_start + 1, function_start+linhas, "Long Method","Total de linhas: " + str(len(lines) - function_start)))
        
    
    return functions_with_long_methods

#--------------------------------------------------------------------------------------#

def check_lc(file_path, pylint_output, max_lines=200, max_attributes_methods=40):
    # Encontra padrões de classes e métodos no pylint_output
    class_pattern = re.findall(r"(\d+):\d+: R0902: Too many instance attributes \((\d+)/\d+\)", pylint_output)
    method_pattern = re.findall(r"(\d+):\d+: R0904: Too many public methods \((\d+)/\d+\)", pylint_output)

    # Dicionário para armazenar a soma de atributos e métodos por linha
    class_metrics = {}

    # Processa classes com muitos atributos
    for match in class_pattern:
        line_number = int(match[0])  # linha onde o problema foi encontrado
        attributes_count = int(match[1])  # contagem de atributos

        # Armazena a contagem de atributos
        if line_number not in class_metrics:
            class_metrics[line_number] = {'attributes': 0, 'methods': 0}
        class_metrics[line_number]['attributes'] += attributes_count

    # Processa métodos públicos
    for match in method_pattern:
        line_number = int(match[0])  # linha onde o problema foi encontrado
        methods_count = int(match[1])  # contagem de métodos

        # Armazena a contagem de métodos
        if line_number not in class_metrics:
            class_metrics[line_number] = {'attributes': 0, 'methods': 0}
        class_metrics[line_number]['methods'] += methods_count

    # Lista para armazenar classes com code smells
    code_smells = []

    # Verifica se a soma de atributos e métodos ultrapassa o limite
    for line_number, metrics in class_metrics.items():
        total_count = metrics['attributes'] + metrics['methods']
        linhas = contar_linhas_classe(file_path,line_number-1)
        if total_count > max_attributes_methods:
            code_smells.append(
    (file_path, line_number, line_number + linhas, 
     "Large Class: " , 
     " Total de atributos: " + str(total_count) + ", Total de Linhas: " + str(linhas))
)

        elif linhas > max_lines:
            code_smells.append(
    (file_path, line_number, line_number + linhas, 
     "Large Class: " , 
     " Total de atributos: " + str(total_count) + ", Total de Linhas: " + str(linhas))
)

    return code_smells

#--------------------------------------------------------------------------------------#

def check_dead_code(file_path: str, pylint_output: str) -> List[Tuple[str, int, int, str]]:
    """
    Verifica e retorna trechos de código morto usando a saída do pylint
    e análise estática de funções e classes não utilizadas.

    Args:
        file_path (str): Caminho do arquivo analisado.
        pylint_output (str): Saída do comando pylint.

    Returns:
        List[Tuple[str, int, int, str]]: Lista de trechos de código morto com detalhes.
    """
    # Mapeia códigos pylint para tipos de "dead code"
    dead_code_types = {
        "W0612": "Unused Variable",
        "W0613": "Unused Function Argument",
        "W0611": "Unused Import",
        "R0903": "Unused Class (too simple)",
        "W0614": "Unused Import from wildcard",
        "W0612": "Unused Local Variable",
    }

    # Regex para capturar linhas e códigos do pylint que indicam "dead code"
    dead_code_matches = re.findall(r"(\d+):\d+: ([A-Z]\d+): (.+)", pylint_output)

    # Lista para armazenar os resultados do pylint
    code_smells = []

    for line_number, code, message in dead_code_matches:
        if code in dead_code_types:
            line_number = int(line_number)
            code_smells.append(
                (file_path, line_number, line_number,"Dead Code", f"{dead_code_types[code]}: {message}")
            )

    # Adiciona análise de funções e classes não utilizadas
    unused_functions = detect_unused_functions_with_lines(file_path)
    unused_classes = detect_unused_classes_with_lines(file_path)

    for func_name, line in unused_functions:
        code_smells.append(
            (file_path, line, line,"Dead Code", f"Unused Function: {func_name}")
        )

    for class_name, line in unused_classes:
        code_smells.append(
            (file_path, line, line,"Dead Code", f"Unused Class: {class_name}")
        )

    return code_smells


# --------------------------------------------------------------------------------------#


def extract_class_name(line_number: int, class_definitions: List[str]) -> str:
    """
    Extrai o nome de uma classe com base na linha onde ela é definida.

    Args:
        line_number (int): Linha onde a classe está definida.
        class_definitions (List[str]): Conteúdo do arquivo com definições de classes.

    Returns:
        str: Nome da classe.
    """
    for i in range(line_number, -1, -1):
        if class_definitions[i].strip().startswith("class "):
            return class_definitions[i].split()[1].split("(")[0]
    return "Unknown"


def calculate_inheritance_depth(class_name: str, class_definitions: List[str]) -> int:
    """
    Calcula a profundidade da árvore de herança de uma classe.

    Args:
        class_name (str): Nome da classe.
        class_definitions (List[str]): Conteúdo do arquivo com definições de classes.

    Returns:
        int: Profundidade da herança.
    """
    for line in class_definitions:
        if f"class {class_name}" in line:
            if "(" in line and ")" in line:
                return 2  # Herda de outra classe
            else:
                return 1  # Não herda de nenhuma classe
    return 1  # Padrão, caso não encontre definição específica

# --------------------------------------------------------------------------------------#
def detect_lazy_classes(file_path):

    """
    Detect lazy classes in a Python file based on the following criteria:
    - Has less than 5 methods XOR less than 5 attributes.
    - OR has inheritance depth less than 2.

    Args:
        file_path (str): Path to the Python file to analyze.

    Returns:
        List[Tuple[str, int, str]]: List of tuples with lazy class details
                                    (class_name, line_number, reason).
    """
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    # Parse the file into an AST
    tree = ast.parse(file_content)
    
    lazy_classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            line_number = node.lineno

            # Count methods in the class
            methods = [
                n for n in node.body if isinstance(n, ast.FunctionDef) and not n.name.startswith('__')
            ]
            num_methods = len(methods)

            # Count attributes in the class
            attributes = [
                n for n in node.body if isinstance(n, ast.Assign)
            ]
            num_attributes = len(attributes)

            # Check inheritance depth
            inheritance_depth = len(node.bases)

            # Lazy class detection rules
            method_attr_condition = (num_methods < 5) ^ (num_attributes < 5)
            inheritance_condition = inheritance_depth < 2

            if method_attr_condition or inheritance_condition:
                reason = []
                if method_attr_condition:
                    reason.append(f"Methods < 5 XOR Attributes < 5 (methods={num_methods}, attributes={num_attributes})")
                if inheritance_condition:
                    reason.append(f"Inheritance depth < 2 (depth={inheritance_depth})")
                lazy_classes.append((file_path, line_number,line_number, "Lazy Class: " + class_name, "; ".join(reason)))
    
    return lazy_classes

def detect_parallel_inheritance(file_path):
    """
    Detect Parallel Inheritance Hierarchy in a Python file based on:
    - Depth of inheritance tree > 3.
    - Number of direct child classes > 4.

    Args:
        file_path (str): Path to the Python file to analyze.

    Returns:
        List[Tuple[str, int, str]]: List of tuples with Parallel Inheritance details
                                    (class_name, line_number, reason).
    """
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    # Parse the file into an AST
    tree = ast.parse(file_content)
    
    # Store class definitions and their base classes
    class_definitions = {}
    class_hierarchy = defaultdict(list)  # Maps base class -> list of child classes

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            line_number = node.lineno

            # Get base classes for the current class
            base_classes = [
                base.id for base in node.bases if isinstance(base, ast.Name)
            ]

            class_definitions[class_name] = {
                "line": line_number,
                "bases": base_classes,
                "children": 0,  # To track the number of direct children
            }

            # Map class to its parents
            for base in base_classes:
                class_hierarchy[base].append(class_name)

    # Calculate depth of inheritance tree and child counts
    for cls_name, cls_info in class_definitions.items():
        # Calculate the inheritance depth
        depth = 0
        current_class = cls_name
        while current_class in class_definitions and class_definitions[current_class]["bases"]:
            depth += 1
            current_class = class_definitions[current_class]["bases"][0]  # Move up the inheritance tree
        
        class_definitions[cls_name]["depth"] = depth

        # Update child count for direct parents
        for base in cls_info["bases"]:
            if base in class_definitions:
                class_definitions[base]["children"] += 1

    # Detect Parallel Inheritance Hierarchies
    parallel_inheritance = []
    for cls_name, cls_info in class_definitions.items():
        depth_condition = cls_info["depth"] > 3
        child_condition = cls_info["children"] > 4

        if depth_condition or child_condition:
            reason = []
            if depth_condition:
                reason.append(f"Inheritance depth > 3 (depth={cls_info['depth']})")
            if child_condition:
                reason.append(f"Number of child classes > 4 (children={cls_info['children']})")
            parallel_inheritance.append((file_path, cls_info["line"],cls_info["line"],"Parallel Inheritance Hierarchies: " + cls_name, "; ".join(reason)))
    
    return parallel_inheritance


