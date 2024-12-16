import ast

def detect_unused_functions_with_lines(file_path):
    """
    Detect functions defined in a Python file that are not called anywhere in the file,
    and include their line numbers.
    
    :param file_path: Path to the Python file to analyze
    :return: A list of tuples (function_name, line_number) for unused functions
    """
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    # Parse the file into an AST
    tree = ast.parse(file_content)
    
    # Extract all function definitions with their line numbers
    function_definitions = {
        node.name: node.lineno for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    }
    
    # Extract all function calls
    function_calls = set(
        node.func.id for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    )
    
    # Find unused functions
    unused_functions = [
        (name, line) for name, line in function_definitions.items() if name not in function_calls
    ]
    
    return unused_functions


def detect_unused_classes_with_lines(file_path):
    """
    Detect classes defined in a Python file that are not instantiated anywhere in the file,
    and include their line numbers.
    
    :param file_path: Path to the Python file to analyze
    :return: A list of tuples (class_name, line_number) for unused classes
    """
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    # Parse the file into an AST
    tree = ast.parse(file_content)
    
    # Extract all class definitions with their line numbers
    class_definitions = {
        node.name: node.lineno for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    }
    
    # Extract all class instantiations (look for calls to a class constructor)
    class_instantiations = set(
        node.func.id for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    )
    
    # Find unused classes
    unused_classes = [
        (name, line) for name, line in class_definitions.items() if name not in class_instantiations
    ]
    
    return unused_classes

def contar_linhas_classe(file_path, linha_inicio):
    """
    Conta o número de linhas de uma classe em um arquivo, incluindo todos os métodos até o fim do bloco da classe.
    
    :param file_path: Caminho para o arquivo de código.
    :param linha_inicio: Índice da linha de início da definição da classe (começando de 0).
    :return: Número de linhas que compõem a definição completa da classe.
    """
    with open(file_path, 'r') as file:
        linhas_codigo = file.readlines()

    # Verifica se a linha de início está dentro do índice do arquivo
    if linha_inicio >= len(linhas_codigo):
        raise ValueError("A linha de início está fora do índice do código fornecido.")

    # Determina o nível de indentação da linha inicial da classe
    linha_inicial = linhas_codigo[linha_inicio]
    indentacao_inicial = len(linha_inicial) - len(linha_inicial.lstrip())

    # Inicializa o contador de linhas
    contador_linhas = 1

    # Itera sobre as linhas após a linha de início
    for linha in linhas_codigo[linha_inicio + 1:]:
        # Calcula a indentação da linha atual
        indentacao_atual = len(linha) - len(linha.lstrip())

        # Verifica se saiu do bloco da classe pela indentação
        if indentacao_atual <= indentacao_inicial and linha.strip() != "":
            break

        contador_linhas += 1

    return contador_linhas




