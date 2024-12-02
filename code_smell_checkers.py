# code_smell_checkers.py

import re
from typing import List, Tuple

def check_too_many_arguments(file_path, pylint_output):
    """Verifica e retorna as linhas com funções contendo muitos argumentos."""
    too_many_args_matches = re.findall(r"(\d+):\d+: R0913: Too many arguments", pylint_output)
    code_smells = []
    
    for line_number in too_many_args_matches:
        line_number = int(line_number)
        code_smells.append((file_path, line_number, line_number, "Too Many Arguments","Quando os parâmetros de dados de uma função ou método, são maiores que 5."))
    
    return code_smells

def check_long_method(file_path, max_lines=10):
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
                functions_with_long_methods.append((file_path, function_start + 1, function_start+linhas , "Long Method","Quando um método ou uma função tem mais de uma 30 linhas."))
                
            function_start = i
    
    if function_start is not None and (len(lines) - function_start) > max_lines:
        linhas = contar_linhas_classe(file_path, function_start)
        functions_with_long_methods.append((file_path, function_start + 1, function_start+linhas, "Long Method","Quando um método ou uma função tem mais de uma 30 linhas."))
        
    
    return functions_with_long_methods

def check_dead_code(file_path: str, pylint_output: str) -> List[Tuple[str, int, int, str]]:
    """
    Verifica e retorna trechos de código morto usando a saída do pylint.

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

    code_smells = []

    for line_number, code, message in dead_code_matches:
        if code in dead_code_types:
            line_number = int(line_number)
            code_smells.append(
                (file_path, line_number, line_number, f"{dead_code_types[code]}: {message}")
            )

    return code_smells


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


def check_lc(file_path, pylint_output, max_lines=20, max_attributes_methods=10):
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
     "Large Class: " + " Total de atributos: " + str(total_count) + ", Total de Linhas: " + str(linhas), 
     "Quando uma Classe tiver mais de 200 linhas ou o número de (atributos + métodos) for maior/igual a 40.")
)

        elif linhas > max_lines:
            code_smells.append(
    (file_path, line_number, line_number + linhas, 
     "Large Class: " + str(total_count) + " Total de atributos", 
     "Quando uma Classe tiver mais de 200 linhas ou o número de (atributos + métodos) for maior/igual a 40.")
)


    return code_smells




