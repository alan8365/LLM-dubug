from typing import Literal

# TODO move all types here

LANG = Literal["python", "java"]
CODE_TYPE = Literal["buggy", "correct", "testcase"]
LIB = Literal["Node", "WeightedEdge"]

MODEL_NAME = Literal["gpt-3.5-turbo-0125", "gpt-4", "gemini-1.0-pro"]