from quixbugs import QuixBugsDatasetItem, QuixBugsDataset
from typing import Literal

PROMPT_TYPE = Literal['basic', 'with_lib', 'with_eng']

def prompt_generate(data: QuixBugsDatasetItem, prompt_type: PROMPT_TYPE = 'basic'):
    prompt_templates: dict[PROMPT_TYPE, str] = {
        "basic": """Fix the bugs in the following code:
```{lang}=
{code}
```

Fixed code:
""",
        "with_lib": """Fix the bugs in the following code:
```{lang}=
{code}
```

Here is the library code used in the code above:
```{lang}=
{lib_code}
```

Fixed code:
""",
    }

    lib_code = '\n'.join(data.lib_usage.values())
    
    prompt = prompt_templates[prompt_type].format(lang=data.language, code=data.buggy_code, lib_code=lib_code)

    return prompt

if __name__ == "__main__":
    a = QuixBugsDataset('java')
    b = a['breadth_first_search']
    c = prompt_generate(b, 'with_lib')
