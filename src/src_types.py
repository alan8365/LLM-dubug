from typing import Literal

# TODO move all types here

LANG = Literal["python", "java"]
CODE_TYPE = Literal["buggy", "correct", "testcase"]
LIB = Literal["Node", "WeightedEdge"]

MODEL_NAME = Literal[
    "gpt-3.5-turbo-0125",
    "gpt-4-turbo-2024-04-09",
    "gpt-4o",
    "gemini-1.0-pro",
    "gemini-1.5-pro",
    "claude-3-opus-20240229",
]
PROMPT_TYPE = Literal["basic", "with_lib", "with_step", "with_location"]
