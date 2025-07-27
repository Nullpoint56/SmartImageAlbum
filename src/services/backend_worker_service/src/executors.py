from typing import Callable

from shared.custom_types.enums import JobStepName

STEP_EXECUTORS: dict[str, Callable] = {}


def step(name: str):
    def wrapper(fn: Callable):
        STEP_EXECUTORS[name] = fn
        return fn

    return wrapper
