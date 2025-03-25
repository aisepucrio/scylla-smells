class SimpleClass:
    def __init__(self):
        self.attribute1 = 1

class AnotherClass:
    def method1(self):
        pass

class SubClass(SimpleClass):
    def __init__(self):
        super().__init__()
