import os
import re
from PIL import Image
from diffusers import StableDiffusionPipeline
import gradio as gr
import ollama

# ========== TEXT GENERATION WITH MISTRAL (OLLAMA) ==========

def mistral_generate(prompt, max_tokens=300):
    response = ollama.chat(
        model='mistral',
        messages=[{"role": "user", "content": prompt}],
        options={"num_predict": max_tokens}
    )
    return response['message']['content']

def generate_story(prompt):
    full_prompt = f"""
You are a creative comic story writer. Your job is to take a short idea and expand it into a two-panel story with vivid scenes and natural dialogue.

Use this structure:
Panel 1:
Scene: Describe the setting and what’s happening.
Characters: List the characters.
Dialogue: Write what the characters are saying.

Panel 2:
Scene: Continue the story with a twist or conflict.
Characters: Same or new ones.
Dialogue: Write interesting, story-driving dialogue.

Prompt: {prompt}

Now generate the story:
"""
    result = mistral_generate(full_prompt, max_tokens=300)

    panels = re.findall(r'Panel\s*\d+:\s*(.*?)(?=Panel\s*\d+:|\Z)', result, re.DOTALL)
    panels = [p.strip() for p in panels if p.strip()]

    return panels, result

# ========== IMAGE GENERATION ==========

# Load Stable Diffusion (CPU mode)
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cpu")

def generate_images(panels):
    panel_images = []
    os.makedirs("comic_panels", exist_ok=True)

    for idx, panel_text in enumerate(panels):
        image = pipe(panel_text).images[0]
        image_path = f"comic_panels/panel_{idx+1}.png"
        image.save(image_path)
        panel_images.append(image)

    return panel_images

# ========== COMIC MERGING ==========

def merge_panels(images):
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    merged_img = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
        merged_img.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    merged_path = "comic_panels/final_comic.png"
    merged_img.save(merged_path)
    return merged_img

# ========== COMIC GENERATOR FUNCTION ==========

def create_comic(prompt):
    panels, story_text = generate_story(prompt)
    images = generate_images(panels)
    final_comic = merge_panels(images)
    return story_text, final_comic

# ========== GRADIO WEB UI ==========

with gr.Blocks() as demo:
    gr.Markdown("## 🎨 ComicCrafter AI - Enter your idea and watch it become a comic!")

    with gr.Row():
        user_prompt = gr.Textbox(label="Enter your comic idea", placeholder="e.g. A mouse challenging a cat to a duel")

    generate_btn = gr.Button("Generate Comic 🎬")

    with gr.Row():
        story_output = gr.Textbox(label="Generated Story & Dialogues", lines=12)

    comic_output = gr.Image(label="Final Merged Comic", type="pil")

    generate_btn.click(fn=create_comic, inputs=user_prompt, outputs=[story_output, comic_output])

demo.launch()
