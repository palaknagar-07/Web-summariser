import requests

# Define API constants
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

# Define messages
messages = [
    {"role": "user", "content": "how many times the letter a appeares in this sentence Explain"}
]

# Create the payload
payload = {
    "model": MODEL,
    "messages": messages,
    "stream": False
}

# Send the request to Ollama API
response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)

# Print the model's response
print(response.json()['message']['content'])
