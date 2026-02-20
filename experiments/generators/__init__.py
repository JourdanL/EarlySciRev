from .utils.parser import TextParser

from .default import DefaultGenerator

def init_generator(model):
    name = model.lower()
    if "gemma-3" in name:
        generator = DefaultGenerator(model, structured_chat=True)
    else:
        generator = DefaultGenerator(model)
    return generator

