# Importing Gradio for creating a simple web UI
import gradio as gr

# Importing the summarize_website function from our custom module
from summarizer import summarize_website # This function should return a text summary

# Wrapper function to use with Gradio interface
def summarize_with_gradio(url):
    return summarize_website(url)

# Setting up the Gradio interface
iface = gr.Interface(
    fn=summarize_with_gradio,
    inputs=gr.Textbox(lines=1, placeholder="Enter URL here..."),
    outputs="markdown",
    title="Web Page Summarizer",
    description="Paste a website URL and get a structured summary using Ollama + LLM.",
)

#Launch the app if this script is run directly
if __name__ == "__main__":
    iface.launch(share=True)
