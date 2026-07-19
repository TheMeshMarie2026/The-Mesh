from prompt_loader import PromptLoader
import yaml

# Load registry
registry_url = "https://raw.githubusercontent.com/<user>/<repo>/main/prompts/registry.yaml"
registry = yaml.safe_load(PromptLoader(registry_url).load())

# Load narrator prompt
file_name = registry["prompts"]["narrator"]["file"]
prompt_url = f"https://raw.githubusercontent.com/<user>/<repo>/main/prompts/{file_name}"
narrator_prompt = PromptLoader(prompt_url).load()
