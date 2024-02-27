import os

from dotenv import load_dotenv

from ..api.api import CodeRepairAPIModule
from ..data.data import DataModule



if __name__ == "__main__":
    data_module = DataModule("../../datasets/QuixBugs")
    data_module.traverse_and_pair_directories()
    processed_data = data_module.get_data()

    load_dotenv()

    # api_key = os.getenv("GOOGLE_API_KEY")
    api_key = os.getenv("OPENAI_API_KEY")

    api_module = CodeRepairAPIModule(api_type="OpenAI", api_key=api_key, model_name='gpt35')
    payload = api_module.prepare_request("def greet(name): print('Hello, ' & name)", "Python")
    response = api_module.make_api_call(payload)
    print(response)
