import csv
import os  # Adicione esta importação
from .code_smell_checkers import (
    check_too_many_arguments,
    check_long_method,
    check_lazy_class,
    check_lc,
    check_data_class,
    check_magic_numbers
)


def save_results_to_csv(results, output_file="code_smells.csv"):
    headers = [
        "arquivo", "linha_inicial", "linha_final", "code_smell", "descricao",
        "LOC", "NOA", "NOM", "DIT",
        "LWMC", "LCOM",
        "PAR",
        "magic_number_value",
        "magic_number_type"
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        
        for result in results:
            metrics = result.get("metricas", {})
            row = {
                **{k: result[k] for k in ["arquivo", "linha_inicial", "linha_final", "code_smell", "descricao"]},
                "LOC": metrics.get("LOC", ""),
                "NOA": metrics.get("NOA", ""),
                "NOM": metrics.get("NOM", ""),
                "DIT": metrics.get("DIT", ""),
                "LWMC": metrics.get("LWMC", ""),
                "LCOM": metrics.get("LCOM", ""),
                "PAR": metrics.get("PAR", ""),
                "magic_number_value": metrics.get("value", ""),
                "magic_number_type": metrics.get("type", "")
            }
            writer.writerow(row)


def check_code_smells_in_directory(directory, output_file="code_smells.csv"):
    all_results = []

    # Percorre recursivamente todos os subdiretórios
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                smells = (
                    check_too_many_arguments(file_path) +
                    check_long_method(file_path) +
                    check_lc(file_path) +
                    check_data_class(file_path) +
                    check_lazy_class(file_path) +
                    check_magic_numbers(file_path)
                )

                for smell in smells:
                    if isinstance(smell, dict):
                        all_results.append(smell)
                    else:
                        print(f"Formato inválido: {smell}")

    save_results_to_csv(all_results, output_file)


if __name__ == "__main__":
    directory_path = "C:\\Users\\Gabriel\\Documents\\vscode\\metricas\\arquivos"
    output_csv = "code_smells.csv"
    check_code_smells_in_directory(directory_path, output_csv)