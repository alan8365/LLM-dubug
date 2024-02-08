# LLM debug experiment

This project aims to evaluate the performance of LLM models in debugging code. The project will utilize LLM models to debug the code and compare the results across multiple LLM models. Additionally, the project will assess the performance of LLM models in different programming languages.

## Project modules

- **DataModule**: This module is responsible for handling all data-related tasks. It includes loading the QuixBugs dataset, parsing code snippets, and structuring them for API requests.
- **APIModule**: Manages interactions with various APIs. It sends code snippets and handles responses. This module will have subclasses or separate methods for different APIs, such as OpenAI's GPT-3.5 and GPT-4, and Google's Gemini API.
- **MetricsModule**: This module is responsible for calculating precision and recall. It takes in the original code, repaired code, and the correct solution to compute metrics.
- **MainModule**: Coordinates the workflow, invoking other modules in the correct order and managing the overall process.

## Project Structure

- `src/`: The main source code of the project.
- `docs/`: Documentation for the project.

## Setup

To set up this project, follow these steps:

1. Install Python 3.8 or higher.
2. Clone the repository to your local machine.
3. Navigate to the project directory.
4. Create a virtual environment: `python3 -m venv venv`.
5. Activate the virtual environment: `source venv/bin/activate`.
6. Install the required packages: `pip install -r requirements.txt`.

## Usage

<!-- TODO complete usage -->
To use this project, follow these steps:

## Future Work

- [ ] Clean the structure of folder.