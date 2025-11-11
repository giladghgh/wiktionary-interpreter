class TranslationExceptions(Exception):
    def __init__(self , message):
        super().__init__(message)
        self.error_code = 900





class NoWordException(TranslationExceptions):
    def __init__(self):
        super().__init__("Word(s) not found.")
        self.error_code = 901





class NoTranslationException(TranslationExceptions):
    def __init__(self):
        super().__init__("Translation(s) not found.")
        self.error_code = 902





class NoSpecificTranslationException(TranslationExceptions):
    def __init__(self):
        super().__init__("Specific translation(s) not found.")
        self.error_code = 903
