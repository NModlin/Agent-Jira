import requests

try:
    response = requests.get('http://localhost:11434/api/tags')
    if response.status_code == 200:
        models = response.json().get('models', [])
        print("Available models:")
        for m in models:
            print(f"- {m['name']}")
    else:
        print(f"Error listing models: {response.status_code} {response.text}")
except Exception as e:
    print(f"Error connecting to Ollama: {e}")
