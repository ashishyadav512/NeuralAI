import requests
import logging
from PIL import Image
import io
import os
import time

def generate_image(prompt, num_frames=10, size="1024x1024"):
    """
    Generate multiple images for video frames using Pollinations API
    """
    images = []
    
    try:
        for i in range(num_frames):
            # Add frame variation to prompt for motion
            frame_prompt = f"{prompt}, frame {i+1} of {num_frames}, cinematic sequence"
            
            # Use Pollinations AI for unlimited image generation
            from urllib.parse import quote
            url = f"https://image.pollinations.ai/prompt/{quote(frame_prompt)}"
            params = {
                'width': 1024,
                'height': 1024,
                'seed': i * 42,  # Different seed for each frame
                'model': 'flux',
                'enhance': 'true'
            }
            
            logging.info(f"Generating frame {i+1}/{num_frames}")
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                images.append(image)
                logging.info(f"Frame {i+1} generated successfully")
            else:
                logging.error(f"Failed to generate frame {i+1}: {response.status_code}")
                
            # Small delay between requests
            time.sleep(0.5)
            
    except Exception as e:
        logging.error(f"Error generating images: {str(e)}")
        return None
    
    return images if images else None

def save_image_local(image, filename):
    """Save image to local storage"""
    try:
        filepath = os.path.join('static', 'images', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        image.save(filepath)
        return filepath
    except Exception as e:
        logging.error(f"Error saving image: {str(e)}")
        return None