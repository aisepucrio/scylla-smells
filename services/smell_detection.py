# services/smell_detection.py
from model.code_metrics import CodeMetrics
from model.smell import CodeSmell
from utils.ast_analyzer import ASTAnalyzer
import ast

class SmellDetector:
    def __init__(self):
        self.ast_analyzer = ASTAnalyzer()

    def detect_long_parameter_list(self, file_path, max_params=4):
        metrics = CodeMetrics()
        parameters = self.ast_analyzer.count_parameters(file_path)
        smells = []
        
        for method in parameters:
            if method["parameters"]["total"] > max_params:
                metrics.PAR = method["parameters"]["total"]
                smells.append(CodeSmell(
                    file_path=file_path,
                    smell_type="Too Many Parameters",
                    description=f"Método '{method['name']}' tem {method['parameters']['total']} parâmetros",
                    start_line=method["line"],
                    end_line=method["line"],
                    metrics=metrics
                ))
        return smells
    
    def detect_long_method(self, file_path, max_lines=67):

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        parameters_data = self.ast_analyzer.count_parameters(file_path)
        smells = []
        current_function = None

        for i, line in enumerate(lines):
            stripped_line = line.strip()

            if stripped_line.startswith("def "):
                if current_function:
                    start_line = current_function["start"]
                    end_line = i - 1
                    loc, total_lines = self.ast_analyzer.calculate_loc_and_total(lines[start_line:end_line])
                    
                    if total_lines > max_lines:
                        method_par = next(
                            (m["parameters"]["total"] for m in parameters_data 
                             if m["line"] == start_line + 1),
                            0
                        )
                        
                        metrics = CodeMetrics()
                        metrics.LOC = total_lines
                        metrics.PAR = method_par
                        
                        smells.append(CodeSmell(
                            file_path=file_path.replace("\\", "/"),
                            smell_type="Long Method",
                            description=f"Method too long: {total_lines} lines (max: {max_lines})",
                            start_line=start_line + 1,
                            end_line=end_line + 1,
                            metrics=metrics
                        ))

                method_name = stripped_line.split("def ")[1].split("(")[0].strip()
                current_function = {"name": method_name, "start": i}

        # Verificação para a última função
        if current_function:
            start_line = current_function["start"]
            end_line = len(lines) - 1
            loc, total_lines = self.ast_analyzer.calculate_loc_and_total(lines[start_line:end_line])
            
            if total_lines > max_lines:
                method_par = next(
                    (m["parameters"]["total"] for m in parameters_data 
                     if m["line"] == start_line + 1),
                    0
                )
                
                metrics = CodeMetrics()
                metrics.LOC = total_lines
                metrics.PAR = method_par
                
                smells.append(CodeSmell(
                    file_path=file_path.replace("\\", "/"),
                    smell_type="Long Method",
                    description=f"Método muito longo: {total_lines} linhas (máx: {max_lines})",
                    start_line=start_line + 1,
                    end_line=end_line + 1,
                    metrics=metrics
                ))

        return smells

    def detect_large_class(self, file_path, max_lines=200, max_attributes_methods=40):
        """
        Detecta classes grandes baseado em tamanho e complexidade.
        
        Args:
            file_path: caminho do arquivo
            max_lines: limite máximo de linhas
            max_attributes_methods: limite de atributos+métodos
        """
        try:
            max_lines = int(max_lines)
            max_attrs = int(max_attributes_methods)
        except (TypeError, ValueError):
            max_lines, max_attrs = 200, 40  # Valores padrão

        noa_stats = self.ast_analyzer.count_attributes(file_path)
        nom_stats = self.ast_analyzer.count_methods(file_path)
        smells = []

        for class_name, metrics in nom_stats.items():
            total_attrs = noa_stats.get("total_attributes", 0)
            total_methods = metrics["total_methods"]
            loc = self.ast_analyzer.count_class_loc(file_path, metrics["start_line"] - 1)

            if (total_attrs + total_methods) > max_attrs or loc > max_lines:
                smell_metrics = CodeMetrics()
                smell_metrics.LOC = loc
                smell_metrics.NOA = total_attrs
                smell_metrics.NOM = total_methods

                smells.append(CodeSmell(
                    file_path=file_path.replace("\\", "/"),
                    smell_type="Large Class",
                    description=f"Atributos: {total_attrs}, Métodos: {total_methods}, Linhas: {loc}",
                    start_line=metrics["start_line"],
                    end_line=metrics["start_line"] + loc - 1,
                    metrics=smell_metrics
                ))
        
        return smells
    
    def detect_data_class(self, file_path, lwmc_threshold=50, lcom_threshold=0.8):
        """
        Detecta classes com alta complexidade (LWMC) ou baixa coesão (LCOM).
        """
        noa_stats = self.ast_analyzer.count_attributes(file_path)
        nom_stats = self.ast_analyzer.count_methods(file_path)
        lwmc_stats = self.ast_analyzer.calculate_lwmc(file_path)
        lcom_stats = self.ast_analyzer.calculate_lcom(file_path)
        
        smells = []
        
        for class_name in nom_stats.keys():
            start_line = nom_stats[class_name]["start_line"]
            loc = self.ast_analyzer.count_class_loc(file_path, start_line - 1)
            
            metrics = CodeMetrics()
            metrics.LOC = loc
            metrics.NOA = noa_stats.get(class_name, {}).get("total_attributes", 0)
            metrics.NOM = nom_stats[class_name]["total_methods"]
            metrics.LWMC = lwmc_stats.get(class_name, 0)
            metrics.LCOM = lcom_stats.get(class_name, 0.0)
            
            if metrics.LWMC > lwmc_threshold or metrics.LCOM > lcom_threshold:
                smells.append(CodeSmell(
                    file_path=file_path.replace("\\", "/"),
                    smell_type="Data Class",
                    description=f"LWMC={metrics.LWMC}, LCOM={metrics.LCOM:.2f}",
                    start_line=start_line,
                    end_line=start_line + loc - 1,
                    metrics=metrics
                ))
        
        return smells
    
    def detect_lazy_class(self, file_path):
        """
        Detecta classes 'preguiçosas' baseado em:
        ((NOM < 5) AND (NOA < 5)) OR (DIT < 2)
        """
        noa_stats = self.ast_analyzer.count_attributes(file_path)
        nom_stats = self.ast_analyzer.count_methods(file_path)
        smells = []

        for class_name, metrics in nom_stats.items():
            nom = metrics["total_methods"]
            noa = noa_stats.get(class_name, {}).get("total_attributes", 0)
            dit = self.ast_analyzer.calculate_dit(file_path, class_name)
            
            if (nom < 5 and noa < 5) or dit < 2:
                loc = self.ast_analyzer.count_class_loc(file_path, metrics["start_line"] - 1)
                
                smell_metrics = CodeMetrics()
                smell_metrics.NOM = nom
                smell_metrics.NOA = noa
                smell_metrics.DIT = dit
                smell_metrics.LOC = loc
                
                smells.append(CodeSmell(
                    file_path=file_path.replace("\\", "/"),
                    smell_type="Lazy Class",
                    description=f"NOM={nom}, NOA={noa}, DIT={dit}",
                    start_line=metrics["start_line"],
                    end_line=metrics["start_line"] + loc - 1,
                    metrics=smell_metrics
                ))
        
        return smells
    

    def detect_magic_numbers(self, file_path):
        """
        Detecta números mágicos no código (números literais sem significado claro).
        Exceções padrão: 0, 1, -1
        
        Args:
            file_path (str): Caminho do arquivo a analisar
            
        Returns:
            list[CodeSmell]: Lista de detecções de números mágicos
        """
        MAGIC_NUMBER_EXCEPTIONS = {0, 1, -1}
        tree = self.ast_analyzer.parse_file(file_path)
        smells = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Num) and node.n not in MAGIC_NUMBER_EXCEPTIONS:
                parent = getattr(node, 'parent', None)
                
                if self._is_valid_magic_number(parent):
                    metrics = CodeMetrics()
                    metrics.value = node.n
                    metrics.type = type(node.n).__name__
                    
                    smells.append(CodeSmell(
                        file_path=file_path.replace("\\", "/"),
                        smell_type="Magic Number",
                        description=f"Número mágico encontrado: {node.n}",
                        start_line=node.lineno,
                        end_line=node.lineno,
                        metrics=metrics
                    ))
        
        return smells

    def _is_valid_magic_number(self, parent_node):
        """
        Verifica se um número deve ser considerado mágico.
        
        Args:
            parent_node (ast.AST): Nó pai do número na AST
            
        Returns:
            bool: True se for um número mágico válido para reportar
        """
        if parent_node is None:
            return True
            
        # Ignora números em constantes (nomes em maiúsculo)
        if isinstance(parent_node, ast.Assign):
            return not any(
                isinstance(target, ast.Name) and target.id.isupper()
                for target in parent_node.targets
            )
            
        # Ignora números em argumentos padrão
        return not isinstance(parent_node, ast.arg)