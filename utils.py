import os
import uuid
import random
import logging
from datetime import datetime
import shutil

def validate_prompt(prompt):
    """
    Validate the user prompt for image generation
    
    Args:
        prompt (str): The user's text prompt
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not prompt or not isinstance(prompt, str):
        return False
    
    # Remove extra whitespace
    prompt = prompt.strip()
    
    # Check length constraints
    if len(prompt) < 3 or len(prompt) > 500:
        return False
    
    # Check for basic content (not just whitespace/special chars)
    if not any(c.isalnum() for c in prompt):
        return False
    
    # Filter out potentially harmful content (basic check)
    harmful_keywords = ['<script', '<?php', 'javascript:', 'data:', 'vbscript:']
    prompt_lower = prompt.lower()
    
    for keyword in harmful_keywords:
        if keyword in prompt_lower:
            return False
    
    return True

def generate_image_mock(prompt):
    """
    Mock image generation function - returns a placeholder image filename
    In production, this would be replaced with actual AI model integration
    
    Args:
        prompt (str): The text prompt for image generation
        
    Returns:
        str: The filename of the generated/placeholder image
    """
    try:
        # Log the generation request
        logging.info(f"Generating image for prompt: {prompt[:50]}...")
        
        # For MVP, return one of the placeholder images randomly
        placeholder_images = [
            'placeholder-1.svg',
            'placeholder-2.svg', 
            'placeholder-3.svg',
            'placeholder-4.svg'
        ]
        
        # Select a random placeholder
        selected_image = random.choice(placeholder_images)
        
        # In a real implementation, you would:
        # 1. Process the prompt through an AI model (Stable Diffusion, etc.)
        # 2. Generate the actual image
        # 3. Save it with a unique filename
        # 4. Return the filename
        
        # For now, we'll copy the placeholder to a unique filename
        unique_filename = f"generated_{uuid.uuid4().hex[:8]}_{selected_image}"
        
        # Ensure the static/images directory exists
        images_dir = os.path.join('static', 'images')
        os.makedirs(images_dir, exist_ok=True)
        
        # Copy placeholder to unique filename (simulating generation)
        source_path = os.path.join(images_dir, selected_image)
        dest_path = os.path.join(images_dir, unique_filename)
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
        else:
            # If placeholder doesn't exist, create a simple SVG
            create_fallback_image(dest_path, prompt)
        
        logging.info(f"Image generated successfully: {unique_filename}")
        return unique_filename
        
    except Exception as e:
        logging.error(f"Error in generate_image_mock: {str(e)}")
        # Return a fallback image filename
        return create_fallback_image_filename(prompt)

def create_fallback_image(filepath, prompt):
    """
    Create a simple SVG fallback image when placeholders aren't available
    
    Args:
        filepath (str): Path where to save the SVG
        prompt (str): The prompt text to include in the image
    """
    try:
        # Create a simple SVG with the prompt
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#6366F1;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#8B5CF6;stop-opacity:1" />
        </linearGradient>
    </defs>
    <rect width="512" height="512" fill="url(#bg)"/>
    <circle cx="256" cy="200" r="60" fill="rgba(255,255,255,0.2)"/>
    <rect x="180" y="300" width="152" height="80" rx="8" fill="rgba(255,255,255,0.2)"/>
    <text x="256" y="420" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="16" font-weight="bold">
        AI Generated
    </text>
    <text x="256" y="440" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-family="Arial, sans-serif" font-size="12">
        {prompt[:30]}{'...' if len(prompt) > 30 else ''}
    </text>
</svg>'''
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
            
    except Exception as e:
        logging.error(f"Error creating fallback image: {str(e)}")

def create_fallback_image_filename(prompt):
    """
    Create a unique filename for fallback images
    
    Args:
        prompt (str): The prompt text
        
    Returns:
        str: Unique filename for the fallback image
    """
    unique_id = uuid.uuid4().hex[:8]
    filename = f"fallback_{unique_id}.svg"
    
    try:
        images_dir = os.path.join('static', 'images')
        os.makedirs(images_dir, exist_ok=True)
        filepath = os.path.join(images_dir, filename)
        create_fallback_image(filepath, prompt)
        return filename
    except Exception as e:
        logging.error(f"Error creating fallback filename: {str(e)}")
        return "placeholder-1.svg"  # Ultimate fallback

def clean_old_generated_images(days_old=30):
    """
    Clean up old generated images to save disk space
    
    Args:
        days_old (int): Remove images older than this many days
    """
    try:
        images_dir = os.path.join('static', 'images')
        if not os.path.exists(images_dir):
            return
        
        cutoff_time = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        
        for filename in os.listdir(images_dir):
            if filename.startswith('generated_') or filename.startswith('fallback_'):
                filepath = os.path.join(images_dir, filename)
                
                try:
                    file_time = os.path.getmtime(filepath)
                    if file_time < cutoff_time:
                        os.remove(filepath)
                        logging.info(f"Cleaned up old image: {filename}")
                except OSError as e:
                    logging.warning(f"Could not remove {filename}: {str(e)}")
                    
    except Exception as e:
        logging.error(f"Error cleaning old images: {str(e)}")

def get_image_info(filename):
    """
    Get information about a generated image
    
    Args:
        filename (str): The image filename
        
    Returns:
        dict: Image information including size, creation time, etc.
    """
    try:
        filepath = os.path.join('static', 'images', filename)
        
        if not os.path.exists(filepath):
            return None
        
        stat = os.stat(filepath)
        
        return {
            'filename': filename,
            'size_bytes': stat.st_size,
            'created_at': datetime.fromtimestamp(stat.st_ctime),
            'modified_at': datetime.fromtimestamp(stat.st_mtime),
            'file_extension': os.path.splitext(filename)[1],
            'exists': True
        }
        
    except Exception as e:
        logging.error(f"Error getting image info for {filename}: {str(e)}")
        return None

def format_prompt_for_ai(prompt):
    """
    Format and enhance the user prompt for better AI generation results
    
    Args:
        prompt (str): Raw user prompt
        
    Returns:
        str: Enhanced prompt for AI model
    """
    # Clean the prompt
    formatted_prompt = prompt.strip()
    
    # Add quality enhancers for better results (when using real AI models)
    quality_terms = [
        "high quality", "detailed", "professional", "8k", "masterpiece",
        "best quality", "ultra detailed", "photorealistic"
    ]
    
    # Check if prompt already contains quality terms
    has_quality = any(term in formatted_prompt.lower() for term in quality_terms)
    
    if not has_quality and len(formatted_prompt) < 400:  # Don't add if prompt is already long
        formatted_prompt += ", high quality, detailed, professional"
    
    return formatted_prompt
