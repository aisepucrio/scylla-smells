# controller/analysis_controller.py
from services.smell_detection import SmellDetector
from model.code_analysis import CodeAnalysis

class AnalysisController:
    def __init__(self):
        self.detector = SmellDetector()
        self.analysis = CodeAnalysis()

    def analyze_file(self, file_path):
        detectors = [
            self.detector.detect_too_many_args,
            self.detector.detect_long_method,
            # ... outros detectores
        ]
        
        for detector in detectors:
            smells = detector(file_path)
            for smell in smells:
                self.analysis.add_smell(smell.to_dict())  # Método to_dict() no model