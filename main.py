# main.py

from pylint_utils import run_pylint
from code_smell_checkers import check_too_many_arguments, check_long_method, check_dead_code,check_lc
import glob

def check_code_smells_in_directory(directory):
    """Executa as verificações de code smells em todos os arquivos .py do diretório."""
    py_files = glob.glob(f"{directory}/*.py")
    
    for file_path in py_files:
        pylint_output = run_pylint(file_path)
        
        # Verifica cada tipo de code smell
        too_many_args_smells = check_too_many_arguments(file_path, pylint_output)
        long_method_smells = check_long_method(file_path)
        dead_code_smells = check_dead_code(file_path, pylint_output)
        lc = check_lc(file_path, pylint_output)
        
        # Exibe todos os code smells encontrados
        for smell in (too_many_args_smells + long_method_smells + dead_code_smells + lc):
            print(smell)

        print("/--------------------------------------------------------------------------------------------------------------------------/\n\n\n")

# Exemplo de uso
if __name__ == "__main__":
    directory_path = "C:\\Users\\Gabriel\\Documents\\vscode\\testaCode\\arquivos"
    check_code_smells_in_directory(directory_path)
