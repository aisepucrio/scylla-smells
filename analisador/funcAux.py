import ast
#from radon.visitors import ComplexityVisitor
import inspect

def detect_unused_functions_with_lines(file_path):
    """
    Detect functions defined in a Python file that are not called anywhere in the file,
    and include their line numbers.
    
    :param file_path: Path to the Python file to analyze
    :return: A list of tuples (function_name, line_number) for unused functions
    """
    with open(file_path, 'r', encoding='utf-8') as file:  # Adicione encoding
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
    with open(file_path, 'r', encoding='utf-8') as file:  # Adicione encoding
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
    Conta o número de linhas de uma classe em um arquivo.
    """
    with open(file_path, 'r', encoding='utf-8') as file:  # Adicione encoding='utf-8'
        linhas_codigo = file.readlines()

    if linha_inicio >= len(linhas_codigo):
        raise ValueError("A linha de início está fora do índice do código fornecido.")

    linha_inicial = linhas_codigo[linha_inicio]
    indentacao_inicial = len(linha_inicial) - len(linha_inicial.lstrip())
    contador_linhas = 1

    for linha in linhas_codigo[linha_inicio + 1:]:
        indentacao_atual = len(linha) - len(linha.lstrip())
        if indentacao_atual <= indentacao_inicial and linha.strip() != "":
            break
        contador_linhas += 1

    return contador_linhas


def calculate_loc_and_total(code_lines):
    """Calcula LOC (ignorando linhas vazias/comentários) e total de linhas."""
    total_lines = len(code_lines)
    loc = sum(1 for line in code_lines if line.strip() and not line.strip().startswith("#"))
    return loc, total_lines


def count_attributes(file_path):

    """
    Calcula o NOA (Number of Attributes) em um arquivo Python.
    Retorna um dicionário com:
    - "total_attributes": Número total de atributos (classe + instância).
    - "class_attributes": Número de atributos de classe.
    - "instance_attributes": Número de atributos de instância.
    """
    with open(file_path, 'r', encoding='utf-8') as file:  # Adicione encoding
        tree = ast.parse(file.read(), filename=file_path)

    noa_stats = {
        "total_attributes": 0,
        "class_attributes": 0,
        "instance_attributes": 0
    }

    for node in ast.walk(tree):
        # Atributos de classe (definidos diretamente na classe)
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            noa_stats["class_attributes"] += 1

        # Atributos de instância (definidos em métodos, ex: self.attr)
        elif isinstance(node, ast.FunctionDef):
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Assign):
                    for target in subnode.targets:
                        if (isinstance(target, ast.Attribute) and 
                            isinstance(target.value, ast.Name) and 
                            target.value.id == 'self'):
                            noa_stats["instance_attributes"] += 1

    noa_stats["total_attributes"] = (
        noa_stats["class_attributes"] + noa_stats["instance_attributes"]
    )
    return noa_stats

def count_methods(file_path):
    """
    Calcula o NOM (Number of Methods) por classe em um arquivo Python.
    Retorna um dicionário no formato:
    {
        "class_name": {
            "total_methods": int,
            "public_methods": int,
            "private_methods": int
        }
    }
    """
    with open(file_path, 'r', encoding='utf-8') as file: 
        tree = ast.parse(file.read(), filename=file_path)

    class_methods = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            public_methods = 0
            private_methods = 0

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_name = item.name
                    if method_name.startswith('_'):
                        private_methods += 1
                    else:
                        public_methods += 1

            class_methods[class_name] = {
                "total_methods": public_methods + private_methods,
                "public_methods": public_methods,
                "private_methods": private_methods,
                "start_line": node.lineno  # Linha onde a classe começa
            }

    return class_methods

def count_parameters(file_path):
    """
    Calcula o PAR (Number of Parameters) por método/função em um arquivo Python.
    Retorna uma lista de dicionários no formato:
    [
        {
            "name": "nome_do_metodo",
            "line": linha_do_metodo,
            "parameters": {
                "total": int,
                "args": int,      # Parâmetros posicionais
                "defaults": int,  # Parâmetros com valor padrão
                "kwargs": int     # Parâmetros keyword-only (após *)
            }
        }
    ]
    """
    with open(file_path, 'r', encoding='utf-8') as file:  
        tree = ast.parse(file.read(), filename=file_path)

    methods = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Conta parâmetros posicionais
            args = len(node.args.args)
            # Conta parâmetros com valor padrão
            defaults = len(node.args.defaults)
            # Conta keyword-only (ex.: def foo(a, *, b, c))
            kwonlyargs = len(node.args.kwonlyargs)

            methods.append({
                "name": node.name,
                "line": node.lineno,
                "parameters": {
                    "total": args + kwonlyargs,
                    "args": args,
                    "defaults": defaults,
                    "kwargs": kwonlyargs
                }
            })

    return methods

def LWMC(file_path):
    """
    Calcula a métrica LWMC (Lack of Weighted Methods per Class) simplificada.
    Retorna um dicionário com {nome_da_classe: valor_LWMC}
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        source = file.read()
    
    tree = ast.parse(source)
    results = {}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
            
            # Calcula complexidade simplificada (1 ponto por método)
            # Você pode adicionar lógica mais sofisticada aqui se necessário
            results[class_name] = len(methods)
    
    return results

def LCOM(file_path):
    """
    Calcula a métrica LCOM (Lack of Cohesion in Methods) para cada classe no arquivo.
    Retorna um dicionário no formato {class_name: lcom_value}.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read())
    
    results = {}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
            attributes = set()
            
            # Encontra todos os atributos acessados
            for method in methods:
                for subnode in ast.walk(method):
                    if isinstance(subnode, ast.Attribute) and isinstance(subnode.value, ast.Name) and subnode.value.id == 'self':
                        attributes.add(subnode.attr)
            
            # Calcula LCOM simplificado
            if len(methods) == 0 or len(attributes) == 0:
                results[class_name] = 0.0
            else:
                results[class_name] = 1 - (len(attributes) / (len(methods) * len(attributes)))
    
    return results

def DIT(file_path, class_name=None):
    """
    Calcula a profundidade da árvore de herança.
    Se class_name for especificado, retorna apenas para essa classe.
    Caso contrário, retorna um dicionário {class_name: dit_value}.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read())
    
    classes = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes[node.name] = [base.id for base in node.bases if isinstance(base, ast.Name)]
    
    def calculate_dit(cls_name, depth=0):
        if not classes.get(cls_name):
            return depth
        max_depth = depth
        for parent in classes[cls_name]:
            current_depth = calculate_dit(parent, depth + 1)
            if current_depth > max_depth:
                max_depth = current_depth
        return max_depth
    
    if class_name:
        return calculate_dit(class_name)
    else:
        return {cls: calculate_dit(cls) for cls in classes}
