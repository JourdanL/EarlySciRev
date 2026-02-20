import re

class TextParser:
    def __init__(self):
        pass

    def parse(self, text):
        t = text.strip().lower()
        if "yes" in t:
            return True
        elif "no" in t:
            return False
        else:
            return text