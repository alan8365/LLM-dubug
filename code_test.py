import io
import sys
from pathlib import Path

import pandas as pd
import pytest

from utils import get_all_function, copy_to_custom_folder, extract_test_info_from_pytest_log

model_name = 'gpt4'

root_path = Path('/Users/lucyxu/PycharmProjects/debug/')
target_path = root_path / 'datasets' / 'QuixBugs' / 'python_testcases'
generated_code_path = Path('generated_code') / model_name

# Copy file
all_result = []

i = 1
copy_to_custom_folder(generated_code_path, i)

stdout_bak = sys.stdout  # backup stdout
sys.stdout = io.StringIO()

# pytest.main(['--custom', 'python_testcases'])
pytest.main(['--custom', target_path])

output = sys.stdout.getvalue()
sys.stdout.close()
sys.stdout = stdout_bak  # restore stdout

result = extract_test_info_from_pytest_log(output)

# Result to df
function_list = get_all_function()

d = {
    'pass': [False] * 40,
    'fail_test_case': [''] * 40,
}
df = pd.DataFrame(index=function_list, data=d)

for item in result:
    function_name = item['function_name']
    test_text = item['test_text']
    test_result = item['test_result']
    fail_test_case = item['fail_test_case']

    df.loc[function_name, 'pass'] = True if test_result == 'pass' else False
    df.loc[function_name, 'fail_test_case'] = str(fail_test_case)

# df to csv
result_dir = Path('results')
result_dir.mkdir(exist_ok=True)

df.to_csv(result_dir / f'{model_name}_{i}_result.csv')

print(output)
