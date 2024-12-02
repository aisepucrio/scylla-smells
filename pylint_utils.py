# pylint_utils.py

import subprocess

def run_pylint(file_path):
    """Executa o pylint com configurações personalizadas e captura a saída."""
    result = subprocess.run(
        ["pylint", file_path, "--max-public-methods=0", "--max-attributes=0"],
        text=True,
        capture_output=True
    )
    return result.stdout
