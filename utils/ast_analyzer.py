# utils/ast_analyzer.py
import ast

class ASTAnalyzer:
    def count_parameters(self, file_path):
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
    

    def calculate_loc_and_total(self, code_lines):
        """
        Calcula LOC (ignorando linhas vazias/comentários) e total de linhas.
        
        Args:
            code_lines (list): Lista de strings representando linhas de código
            
        Returns:
            tuple: (loc, total_lines) onde:
                - loc: linhas de código válidas
                - total_lines: total de linhas
        """
        total_lines = len(code_lines)
        loc = sum(1 for line in code_lines if line.strip() and not line.strip().startswith("#"))
        return loc, total_lines
    

    def count_attributes(self, file_path):
        """Conta atributos de classe e instância"""
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read(), filename=file_path)

        stats = {"total_attributes": 0, "class_attributes": 0, "instance_attributes": 0}

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        stats["class_attributes"] += sum(1 for t in item.targets if isinstance(t, ast.Name))
            
            elif isinstance(node, ast.FunctionDef):
                stats["instance_attributes"] += sum(
                    1 for n in ast.walk(node) 
                    if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Attribute) and 
                        isinstance(t.value, ast.Name) and 
                        t.value.id == 'self' 
                        for t in n.targets)
                )

        stats["total_attributes"] = stats["class_attributes"] + stats["instance_attributes"]
        return stats

    def count_methods(self, file_path):
        """Conta métodos por classe"""
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read(), filename=file_path)

        class_methods = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = {
                    "total_methods": 0,
                    "public_methods": 0,
                    "private_methods": 0,
                    "start_line": node.lineno
                }
                
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods["total_methods"] += 1
                        if item.name.startswith('_'):
                            methods["private_methods"] += 1
                        else:
                            methods["public_methods"] += 1
                
                class_methods[node.name] = methods
        
        return class_methods


    def count_class_loc(self, file_path, start_line):
        """
        Conta o número de linhas de uma classe a partir de sua linha de início.
        
        Args:
            file_path (str): Caminho do arquivo Python
            start_line (int): Número da linha onde a classe começa (base 0)
            
        Returns:
            int: Número total de linhas da classe
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if start_line >= len(lines):
            return 0

        # Determina a indentação da linha inicial da classe
        class_line = lines[start_line]
        base_indent = len(class_line) - len(class_line.lstrip())
        line_count = 1  # Já conta a linha inicial

        # Percorre as linhas seguintes
        for line in lines[start_line + 1:]:
            current_indent = len(line) - len(line.lstrip())
            
            # Verifica se saiu do bloco da classe
            if current_indent <= base_indent and line.strip():
                break
                
            line_count += 1

        return line_count
    
    def calculate_lcom(self, file_path):
        """
        Calcula a métrica LCOM (Lack of Cohesion in Methods).
        Retorna um dicionário {class_name: lcom_value}.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())
        
        results = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                attributes = set()
                
                for method in methods:
                    for subnode in ast.walk(method):
                        if isinstance(subnode, ast.Attribute) and \
                        isinstance(subnode.value, ast.Name) and \
                        subnode.value.id == 'self':
                            attributes.add(subnode.attr)
                
                results[node.name] = 0.0 if not methods or not attributes else \
                                1 - (len(attributes) / (len(methods) * len(attributes)))
        
        return results

    def calculate_lwmc(self, file_path):
        """Versão com cálculo de complexidade ciclomática"""
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())
        
        results = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                total_complexity = 0
                for method in [n for n in node.body if isinstance(n, ast.FunctionDef)]:
                    total_complexity += self.calculate_cyclomatic_complexity(method)
                results[node.name] = total_complexity
        
        return results
    

    def calculate_dit(self, file_path, class_name=None):
        """
        Calcula a profundidade da árvore de herança (DIT).
        
        Args:
            file_path: caminho do arquivo Python
            class_name: nome da classe específica (opcional)
        
        Returns:
            int/dict: profundidade para a classe ou dicionário {class_name: dit}
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())

        # Mapeamento de classes e seus pais
        class_hierarchy = {
            node.name: [base.id for base in node.bases 
                    if isinstance(base, ast.Name)]
            for node in ast.walk(tree) 
            if isinstance(node, ast.ClassDef)
        }

        def _calculate_depth(cls, depth=0):
            parents = class_hierarchy.get(cls, [])
            if not parents:
                return depth
            return max(_calculate_depth(p, depth + 1) for p in parents)

        if class_name:
            return _calculate_depth(class_name)
        return {cls: _calculate_depth(cls) for cls in class_hierarchy}
    
    def parse_file(self, file_path):
        """
        Faz o parse do arquivo e retorna a AST.
        
        Args:
            file_path (str): Caminho do arquivo Python
            
        Returns:
            ast.Module: Árvore de sintaxe abstrata
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return ast.parse(file.read(), filename=file_path)
        
        
    def calculate_cyclomatic_complexity(self, node):
        # Exemplo muito simples: conta número de ifs, fors, whiles
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.BoolOp)):
                complexity += 1
        return complexity


    # Outras funções de análise de AST...