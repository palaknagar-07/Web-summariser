# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import json
from rich.markdown import Markdown
from rich.console import Console

# Define constants for the Ollama API endpoint and model to use
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"

# Custom headers to mimic a real browser (helps avoid being blocked by some websites)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

# Website class handles fetching and cleaning text content from a given URL
class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get the page title or fallback if not found
        self.title = soup.title.string if soup.title else "No title found"

        # Remove non-informative elements like scripts, styles, images, and inputs
        for tag in soup(['script', 'style', 'img', 'input']):
            tag.decompose()

        # Extract the remaining visible text from the cleaned page
        self.text = soup.get_text(separator="\n", strip=True)

# Builds a structured Markdown prompt for the LLM to summarize
def build_prompt(website):
    return f"""
You are a helpful assistant. Your task is to summarize the following web page titled **{website.title}**.

### Format the output in Markdown with the following structure:

# Summary of: {website.title}

## Overview
Provide a concise 1–2 sentence overview of the page content.

## Key Points
List 3–5 important points as bullet points.

## Additional Details
Mention any interesting subtopics, statistics, quotes, or extra insights from the article.

---
### Web Page Content:
{website.text}
"""

# Sends the prompt to the Ollama LLM and collects the streamed Markdown summary
def summarize_with_ollama(prompt, model=OLLAMA_MODEL):
    response = requests.post(OLLAMA_URL, json={
        "model": model,
        "stream": True,  
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }, stream=True)

    # Check if the response was successful
    if response.status_code != 200:
        raise Exception(f"Ollama API Error: {response.status_code} - {response.text}")

    full_content = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode('utf-8'))
                full_content += data.get("message", {}).get("content", "")
            except json.JSONDecodeError as e:
                print("JSON Decode Error:", e)
                print("Raw line:", line)

    return full_content

# Coordinates fetching the webpage, building the prompt, summarizing it, and displaying it
def summarize_website(url):
    website = Website(url)
    prompt = build_prompt(website)
    summary = summarize_with_ollama(prompt)

    # Display the markdown summary beautifully in the terminal
    console = Console()
    console.print(Markdown(f"# Summary of: {website.title}\n\n{summary}"))

# Entry point for the script; change the URL here to summarize other websites
if __name__ == "__main__":
    test_url = "https://www.geeksforgeeks.org/courses?source=google&medium=cpc&device=c&keyword=gfg&matchtype=p&campaignid=20039445781&adgroup=147845288105&gad_source=1&gad_campaignid=20039445781&gbraid=0AAAAAC9yBkAOvteXzweNhZtiVC3RWSwOq&gclid=CjwKCAjwpMTCBhA-EiwA_-MsmdVG8CFesFmYUvq6biJYyUwF1DK7S_1rAqLJkcbP4_dwa3SYC-oVUhoCkRQQAvD_BwE"
    summarize_website(test_url)
