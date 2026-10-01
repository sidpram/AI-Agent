## AI-Agent
# check python version : python --version

### Download and Install Ollama
> ollama pull qwen3:1.7b
> ollama run qwen3:1.7b

# #Create a Virtual Enviroment: 
Now the library required for this project will be saved locally in AI-Agent

### Create AI-Agent dir
Open the integrated terminal in VS Code and run:
python -m venv .venv
This creates a new folder named .venv. 

#### Activate the .venv
.venv\Scripts\activate
Now the cmd chnages from PS dir> to (.venv) PS dir>

### Install the Required Python Library
We'll use a single Python package that provides an OpenAI-compatible client. Since Ollama supports this standard, the same code can later work with many other AI providers.
Run:
pip install openai python-dotenv


#### Creating the Configuration .env File
Inside the Day01 folder, create: .env
Add the following contents:
BASE_URL= http://localhost:11434/v1
API_KEY= ollama
MODEL= qwen3:1.7b

