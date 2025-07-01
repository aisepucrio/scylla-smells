class CodeMetrics:
    def __init__(self, LOC=None, NOA=None, NOM=None, DIT=None, LWMC=None, LCOM=None, PAR=None, value=None, type=None):
        self.LOC = LOC
        self.NOA = NOA
        self.NOM = NOM
        self.DIT = DIT
        self.LWMC = LWMC
        self.LCOM = LCOM
        self.PAR = PAR
        self.value = value
        self.type = type

    def to_dict(self):
        return {
            "LOC": self.LOC,
            "NOA": self.NOA,
            "NOM": self.NOM,
            "DIT": self.DIT,
            "LWMC": self.LWMC,
            "LCOM": self.LCOM,
            "PAR": self.PAR,
            "value": self.value,
            "type": self.type,
        }
