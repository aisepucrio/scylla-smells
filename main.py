import csv
import os
from services.smell_detection import SmellDetector  # <- importa a classe

def save_results_to_csv(results, output_file="code_smells.csv"):
    headers = [
        "file_path", "start_line", "end_line", "smell_type", "description",
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
            metrics = result
            row = {
                **{k: result.get(k, "") for k in ["file_path", "start_line", "end_line", "smell_type", "description"]},
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
    detector = SmellDetector()  # <- instância da classe

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)

                smells = (
                    detector.detect_long_parameter_list(file_path) +
                    detector.detect_long_method(file_path) +
                    detector.detect_large_class(file_path) +
                    detector.detect_data_class(file_path) +
                    detector.detect_lazy_class(file_path) +
                    detector.detect_magic_numbers(file_path)
                )

                for smell in smells:
                    if hasattr(smell, "to_dict"):
                        all_results.append(smell.to_dict())
                    else:
                        print(f"Formato inválido: {smell}")

    save_results_to_csv(all_results, output_file)

if __name__ == "__main__":
    directory_path = "C:\\Users\\Gabriel\\Documents\\vscode\\testaCode\\evaluation"
    output_csv = "data\\code_smells.csv"
    check_code_smells_in_directory(directory_path, output_csv)
