import gradio as gr
from web_summarizer import summarize_website  # Make sure summarize_website returns text

def summarize_with_gradio(url):
    return summarize_website(url)

# Create the Gradio interface
iface = gr.Interface(
    fn=summarize_with_gradio,
    inputs=gr.Textbox(lines=1, placeholder="Enter URL here..."),
    outputs="markdown",
    title="🧠 Web Page Summarizer",
    description="Paste a website URL and get a structured summary using Ollama + LLM.",
)

if __name__ == "__main__":
    iface.launch(share=True)
