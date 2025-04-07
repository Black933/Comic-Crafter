# Comic-Crafter

ComicCrafter AI is a locally running Python-based application that transforms user ideas into engaging two-panel comic strips using AI. It combines natural language generation (via the Mistral model with Ollama) and image generation (via Stable Diffusion in CPU mode) to create complete mini-comics with both story and visuals — all without relying on cloud APIs.

Features:
🧠 AI Story Generation with Mistral (via Ollama)

🖼️ Image Generation using Stable Diffusion (Diffusers Library)

🧩 Panel Merging to form a final comic strip

🖥️ Fully Offline & Local Execution (no API keys or cloud dependencies)

💻 Lightweight Gradio Interface for a seamless user experience


Objective:
To build an AI-powered application that helps users quickly convert ideas into short illustrated comic strips locally, even on machines with limited hardware resources (like 8GB RAM and no GPU).

Tech Stack:
Python 3.10+

Gradio – for the web interface

Diffusers & Stable Diffusion v1.5 – for CPU-based image generation

Ollama + Mistral 7B GGUF – for local text generation


How It Works:
Input Prompt: User provides a comic idea (e.g., "A mouse challenges a cat to a duel").

Story Generation: The Mistral model generates a two-panel story with scenes, characters, and dialogue.

Image Rendering: Stable Diffusion generates panel images based on scene descriptions.

Comic Merging: Both images are stitched side-by-side to create a final comic.

Output: The generated story and comic image are displayed together.



Challenges Faced:
Local deployment of large models on 8GB RAM

Streamlit UI failed due to resource issues, switched to Gradio for better performance

Stable Diffusion in CPU mode is slow, but functional

Ollama required custom model placement and handling due to memory constraints

Conclusion:
Despite running on a low-spec device (8GB RAM, no GPU), ComicCrafter AI demonstrates that creative AI applications can function efficiently using only local tools. It’s a compact yet powerful tool for storytelling and creativity.
