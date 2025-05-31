# code_smell_checkers.py

import ast
import os
import re
import subprocess
from typing import List, Tuple
from collections import defaultdict
from .funcAux import DIT,LWMC, LCOM ,count_parameters,count_methods,count_attributes,detect_unused_functions_with_lines, detect_unused_classes_with_lines, contar_linhas_classe,calculate_loc_and_total

#--------------------------------------------------------------------------------------#
def check_too_many_arguments(file_path, max_parameters=4):
    """
    Detecta métodos/funções com muitos parâmetros.
    Retorna apenas o total de parâmetros (PAR) nas métricas.
    Args:
        max_parameters (int): Limite de parâmetros (padrão: 3)
    """
    parameters_data = count_parameters(file_path)
    code_smells = []

    # Garante que max_parameters é inteiro
    try:
        max_params = int(max_parameters)
    except (TypeError, ValueError):
        max_params = 3  # Valor padrão se conversão falhar

    for method in parameters_data:
        if method["parameters"]["total"] > max_params:
            code_smells.append({
                "arquivo": file_path.replace("\\", "/"),
                "linha_inicial": method["line"],
                "linha_final": method["line"],
                "code_smell": "Too Many Parameters",
                "descricao": f"Método '{method['name']}' tem {method['parameters']['total']} parâmetros (máx: {max_params})",
                "metricas": {
                    "PAR": method["parameters"]["total"]  # Apenas o total
                }
            })

    return code_smells

#--------------------------------------------------------------------------------------#
def check_long_method(file_path, max_lines=67):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    parameters_data = count_parameters(file_path)  # Obtém dados de PAR
    functions_info = []
    current_function = None

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        if stripped_line.startswith("def "):
            if current_function:
                start_line = current_function["start"]
                end_line = i - 1
                loc, total_lines = calculate_loc_and_total(lines[start_line:end_line])
                
                if total_lines > max_lines:
                    # Encontra PAR do método atual
                    method_par = next(
                        (m["parameters"]["total"] for m in parameters_data 
                         if m["line"] == start_line + 1),
                        0
                    )
                    
                    functions_info.append({
                        "arquivo": file_path.replace("\\", "/"),
                        "linha_inicial": start_line + 1,
                        "linha_final": end_line + 1,
                        "code_smell": "Long Method",
                        "descricao": f"Método muito longo: {total_lines} linhas (máx: {max_lines})",
                        "metricas": {
                            "LOC": total_lines,
                            "PAR": method_par  # Nova métrica adicionada
                        }
                    })

            method_name = stripped_line.split("def ")[1].split("(")[0].strip()
            current_function = {"name": method_name, "start": i}

    # Verificação para a última função (mesma lógica)
    # ... (código existente, com mesma adição de PAR)

    return functions_info
#--------------------------------------------------------------------------------------#

def check_lc(file_path, max_lines=200, max_attributes_methods=40):
    """Verifica classes grandes com thresholds convertidos para inteiros."""
    # Conversão segura dos thresholds
    try:
        max_lines = int(max_lines)
    except (TypeError, ValueError):
        max_lines = 20  # Valor padrão se falhar
        
    try:
        max_attrs_methods = int(max_attributes_methods)
    except (TypeError, ValueError):
        max_attrs_methods = 5  # Valor padrão se falhar

    noa_stats = count_attributes(file_path)
    nom_stats = count_methods(file_path)
    code_smells = []

    for class_name, metrics in nom_stats.items():
        total_attributes = noa_stats.get("total_attributes", 0)
        total_methods = metrics["total_methods"]
        linhas = contar_linhas_classe(file_path, metrics["start_line"] - 1)

        # Agora comparando com inteiros garantidos
        if (total_attributes + total_methods) > max_attrs_methods or linhas > max_lines:
            code_smells.append({
                "arquivo": file_path.replace("\\", "/"),
                "linha_inicial": metrics["start_line"],
                "linha_final": metrics["start_line"] + linhas - 1,
                "code_smell": "Large Class",
                "descricao": f"Atributos: {total_attributes}, Métodos: {total_methods}, Linhas: {linhas}",
                "metricas": {
                    "LOC": linhas,
                    "NOA": total_attributes,
                    "NOM": total_methods
                }
            })

    return code_smells

#--------------------------------------------------------------------------------------#
def check_data_class(file_path, lwmc_threshold=50, lcom_threshold=0.8):
    """
    Detecta classes com alta complexidade (LWMC) ou baixa coesão (LCOM).
    """
    # Obtém métricas das classes
    noa_stats = count_attributes(file_path)
    nom_stats = count_methods(file_path)
    lwmc_stats = LWMC(file_path)
    
    # Obter LCOM - verifica se é dicionário ou valor único
    lcom_value = LCOM(file_path)
    if isinstance(lcom_value, dict):
        lcom_stats = lcom_value
    else:
        # Se LCOM retornar um único valor, cria um dicionário com esse valor para todas as classes
        lcom_stats = {class_name: lcom_value for class_name in nom_stats.keys()}
    
    code_smells = []
    
    for class_name in nom_stats.keys():
        # Obtém a linha de início da classe
        start_line = nom_stats[class_name]["start_line"]
        
        # Calcula LOC usando contar_linhas_classe com linha_inicio
        loc = contar_linhas_classe(file_path, start_line - 1)  # -1 porque linha_inicio começa em 0
        
        
        noa = noa_stats.get(class_name, {}).get("total_attributes", 0)
        nom = nom_stats[class_name]["total_methods"]
        lwmc = lwmc_stats.get(class_name, 0)
        lcom = lcom_stats.get(class_name, 0.0)
        
        if lwmc > lwmc_threshold or lcom > lcom_threshold:
            code_smells.append({
                "arquivo": file_path.replace("\\", "/"),
                "linha_inicial": start_line,
                "linha_final": start_line + loc - 1,
                "code_smell": "Data Class",
                "descricao": f"LWMC={lwmc}, LCOM={lcom:.2f}",
                "metricas": {
                    "LWMC": lwmc,
                    "LCOM": lcom,
                    "LOC": loc,
                    "NOA": noa,
                    "NOM": nom,
                    "PAR": 0 # Pode ser calculado se necessário
                }
            })
    
    return code_smells
# --------------------------------------------------------------------------------------#

def check_lazy_class(file_path):
    """
    Detecta classes 'preguiçosas' (que fazem pouco) baseado em:
    ((NOM < 5) AND (NOA < 5)) OR (DIT < 2)
    """
    noa_stats = count_attributes(file_path)
    nom_stats = count_methods(file_path)
    
    code_smells = []
    
    for class_name in nom_stats.keys():
        nom = nom_stats[class_name]["total_methods"]
        noa = noa_stats.get(class_name, {}).get("total_attributes", 0)
        dit = DIT(file_path, class_name)  # Assumindo que DIT retorna um valor por classe
        
        start_line = nom_stats[class_name]["start_line"]
        loc = contar_linhas_classe(file_path, start_line - 1)
        
        if (nom < 5 and noa < 5) or dit < 2:
            code_smells.append({
                "arquivo": file_path.replace("\\", "/"),
                "linha_inicial": start_line,
                "linha_final": start_line + loc - 1,
                "code_smell": "Lazy Class",
                "descricao": f"NOM={nom}, NOA={noa}, DIT={dit}",
                "metricas": {
                    "NOM": nom,
                    "NOA": noa,
                    "DIT": dit,  # Incluindo DIT
                    "LOC": loc,
                    "LWMC": 0,    # Pode ser calculado
                    "LCOM": 0.0    # Pode ser calculado
                }
            })
    
    return code_smells

# --------------------------------------------------------------------------------------#
def check_magic_numbers(file_path):
    """
    Detecta números mágicos no código (números literais sem significado claro).
    Exceções: 0, 1, -1 são considerados aceitáveis.
    Retorna lista de detecções no formato padrão.
    """
    MAGIC_NUMBER_EXCEPTIONS = {0, 1, -1}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    code_smells = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Num) and node.n not in MAGIC_NUMBER_EXCEPTIONS:
            # Verifica se é um número literal "mágico"
            parent = getattr(node, 'parent', None)  # Usando atributo parent se disponível
            
            # Ignora números em definições de constantes
            if isinstance(parent, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id.isupper()
                for target in parent.targets
            ):
                continue
                
            # Ignora números em argumentos padrão de funções
            if isinstance(parent, ast.arg):
                continue
                
            # Obtém a linha do número mágico
            line_number = node.lineno
            
            code_smells.append({
                "arquivo": file_path.replace("\\", "/"),
                "linha_inicial": line_number,
                "linha_final": line_number,
                "code_smell": "Magic Number",
                "descricao": f"Número mágico encontrado: {node.n}",
                "metricas": {
                    "value": node.n,
                    "type": type(node.n).__name__
                }
            })
    
    return code_smells
# --------------------------------------------------------------------------------------#
