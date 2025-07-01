# model/smell.py



class CodeSmell:
    def __init__(self, file_path, start_line, end_line, smell_type, description, metrics=None):
        self.file_path = file_path.replace("\\", "/")
        self.start_line = start_line
        self.end_line = end_line
        self.smell_type = smell_type
        self.description = description
        self.metrics = metrics or {}

    def to_dict(self):
        return {
            "file_path": self.file_path,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "smell_type": self.smell_type,
            "description": self.description,
            **self.metrics.to_dict() # <---- isso aqui expande as métricas como colunas no CSV
        }



