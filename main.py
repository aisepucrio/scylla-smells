import csv
import glob
from pylint_utils import run_pylint
from code_smell_checkers import (
    check_too_many_arguments,
    check_long_method,
    check_dead_code,
    check_lc,
    detect_lazy_classes,
    detect_parallel_inheritance,
    check_magic_numbers
)


def save_results_to_csv(results, output_file="code_smells.csv"):
    """
    Salva os resultados de code smells em um arquivo CSV.

    Args:
        results (list): Lista de dicionários contendo os resultados das análises.
        output_file (str): Nome do arquivo CSV de saída.
    """
    if not results:
        print("Nenhum resultado para salvar.")
        return

    headers = [
        "arquivo",
        "linha inicial",
        "linha final",
        "code smells",
        "descrição"
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(results)

    print(f"Resultados salvos no arquivo {output_file}")


def check_code_smells_in_directory(directory, output_file="code_smells.csv"):
    """
    Executa as verificações de code smells em todos os arquivos .py do diretório
    e salva os resultados em um arquivo CSV.

    Args:
        directory (str): Caminho para o diretório com arquivos Python.
        output_file (str): Nome do arquivo CSV de saída.
    """
    py_files = glob.glob(f"{directory}/*.py")
    all_results = []

    for file_path in py_files:
        pylint_output = run_pylint(file_path)

        # Verifica cada tipo de code smell
        TMA = check_too_many_arguments(file_path, pylint_output)
        LM = check_long_method(file_path)
        DC = check_dead_code(file_path, pylint_output)
        LC = check_lc(file_path, pylint_output)
        LZ = detect_lazy_classes(file_path)
        PH = detect_parallel_inheritance(file_path)
        MN = check_magic_numbers(file_path) 

        # Coleta os resultados de cada análise
        for smell in TMA + LM + DC + LC  + LZ + PH + MN:
            if len(smell) == 5:
                all_results.append({
                    "arquivo": smell[0].replace("\\", "/"),
                    "linha inicial": smell[1],
                    "linha final": smell[2],
                    "code smells": smell[3],
                    "descrição": smell[4]
                })
            else:
                print(f"A tupla retornada não tem 5 elementos: {smell}")

    save_results_to_csv(all_results, output_file)


# Exemplo de uso
if __name__ == "__main__":
    directory_path = "C:\\Users\\Gabriel\\Documents\\vscode\\testaCode\\arquivos"
    output_csv = "code_smells.csv"
    check_code_smells_in_directory(directory_path, output_csv)
