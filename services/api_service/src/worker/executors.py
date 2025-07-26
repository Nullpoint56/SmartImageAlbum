from typing import Callable

STEP_EXECUTORS: dict[str, Callable] = {}

def step(name: str):
    def wrapper(fn: Callable):
        STEP_EXECUTORS[name] = fn
        return fn
    return wrapper
