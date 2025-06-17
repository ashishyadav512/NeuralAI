import cv2
import numpy as np
import logging
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random
import math

def create_video_from_images(images, output_path, prompt):
    """
    Create a high-quality video from AI-generated images with advanced effects
    """
    try:
        if not images:
            logging.error("No images provided for video creation")
            return False
        
        # Video settings for YouTube quality
        width, height = 1024, 1024
        fps = 15
        duration = 10  # 10 seconds
        total_frames = fps * duration  # 150 frames
        
        # Initialize video writer with high quality codec
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        if not out.isOpened():
            logging.error("Failed to open video writer")
            return False
        
        logging.info(f"Creating {duration}s video with {total_frames} frames at {fps}fps")
        
        # Convert PIL images to OpenCV format
        cv_images = []
        for img in images:
            img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
            cv_img = cv2.cvtColor(np.array(img_resized), cv2.COLOR_RGB2BGR)
            cv_images.append(cv_img)
        
        # Generate video frames with smooth transitions and effects
        for frame_idx in range(total_frames):
            progress = frame_idx / total_frames
            
            # Determine which base images to blend
            img_progress = progress * (len(cv_images) - 1)
            base_idx = int(img_progress)
            blend_factor = img_progress - base_idx
            
            if base_idx >= len(cv_images) - 1:
                current_frame = cv_images[-1].copy()
            else:
                # Smooth blending between consecutive images
                img1 = cv_images[base_idx]
                img2 = cv_images[base_idx + 1]
                current_frame = cv2.addWeighted(img1, 1 - blend_factor, img2, blend_factor, 0)
            
            # Apply advanced visual effects
            current_frame = apply_visual_effects(current_frame, frame_idx, progress, prompt)
            
            # Add engaging hooks and text overlays
            current_frame = add_hook_overlay(current_frame, frame_idx, total_frames, prompt)
            
            # Write frame to video
            out.write(current_frame)
            
            if frame_idx % 30 == 0:  # Log progress every 2 seconds
                logging.info(f"Generated frame {frame_idx}/{total_frames}")
        
        out.release()
        logging.info(f"Video created successfully: {output_path}")
        return True
        
    except Exception as e:
        logging.error(f"Error creating video: {str(e)}")
        return False

def apply_visual_effects(frame, frame_idx, progress, prompt):
    """Apply advanced visual effects for cinematic quality"""
    
    # Convert to float for processing
    frame_float = frame.astype(np.float32) / 255.0
    
    # 1. Dynamic lighting effects
    if "sunset" in prompt.lower() or "golden" in prompt.lower():
        # Golden hour lighting
        golden_overlay = np.zeros_like(frame_float)
        golden_overlay[:, :, 0] = 0.1  # Blue
        golden_overlay[:, :, 1] = 0.3  # Green  
        golden_overlay[:, :, 2] = 0.5  # Red
        frame_float = cv2.addWeighted(frame_float, 0.8, golden_overlay, 0.2, 0)
    
    # 2. Particle effects based on content
    if any(word in prompt.lower() for word in ["water", "rain", "ocean", "sea"]):
        frame_float = add_water_particles(frame_float, frame_idx)
    elif any(word in prompt.lower() for word in ["fire", "flame", "burning"]):
        frame_float = add_fire_particles(frame_float, frame_idx)
    elif any(word in prompt.lower() for word in ["snow", "winter", "ice"]):
        frame_float = add_snow_particles(frame_float, frame_idx)
    else:
        frame_float = add_sparkle_particles(frame_float, frame_idx)
    
    # 3. Cinematic post-processing
    frame_float = apply_cinematic_grade(frame_float, progress)
    
    # 4. Motion blur for realism
    if frame_idx > 0:
        kernel_size = 3
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
        frame_float = cv2.filter2D(frame_float, -1, kernel)
    
    # Convert back to uint8
    frame_processed = (frame_float * 255).astype(np.uint8)
    
    return frame_processed

def add_water_particles(frame, frame_idx):
    """Add realistic water droplet effects"""
    height, width = frame.shape[:2]
    
    # Generate water droplets
    for _ in range(random.randint(5, 15)):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1) 
        
        # Animated droplet position
        y_offset = (frame_idx * 2) % height
        y = (y + y_offset) % height
        
        # Create droplet effect
        radius = random.randint(1, 3)
        intensity = random.uniform(0.1, 0.3)
        
        # Add blue tint for water
        if y-radius >= 0 and y+radius < height and x-radius >= 0 and x+radius < width:
            frame[y-radius:y+radius, x-radius:x+radius, 0] += intensity  # Blue channel
    
    return frame

def add_fire_particles(frame, frame_idx):
    """Add realistic fire particle effects"""
    height, width = frame.shape[:2]
    
    for _ in range(random.randint(8, 20)):
        x = random.randint(0, width-1)
        y = random.randint(height//2, height-1)  # Fire rises from bottom
        
        # Animated flame movement
        y_offset = -(frame_idx * 3) % (height//2)
        y = max(0, y + y_offset)
        
        radius = random.randint(1, 4)
        intensity = random.uniform(0.2, 0.5)
        
        # Add red/orange tint
        if y-radius >= 0 and y+radius < height and x-radius >= 0 and x+radius < width:
            frame[y-radius:y+radius, x-radius:x+radius, 2] += intensity  # Red
            frame[y-radius:y+radius, x-radius:x+radius, 1] += intensity * 0.5  # Green
    
    return frame

def add_snow_particles(frame, frame_idx):
    """Add realistic snow particle effects"""
    height, width = frame.shape[:2]
    
    for _ in range(random.randint(10, 25)):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        
        # Animated snowfall
        y_offset = (frame_idx * 2) % height
        y = (y + y_offset) % height
        
        radius = random.randint(1, 2)
        intensity = random.uniform(0.3, 0.6)
        
        # Add white particles
        if y-radius >= 0 and y+radius < height and x-radius >= 0 and x+radius < width:
            frame[y-radius:y+radius, x-radius:x+radius] += intensity
    
    return frame

def add_sparkle_particles(frame, frame_idx):
    """Add magical sparkle effects"""
    height, width = frame.shape[:2]
    
    for _ in range(random.randint(3, 8)):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        
        # Twinkling effect
        twinkle = abs(math.sin(frame_idx * 0.2 + x * 0.01 + y * 0.01))
        radius = random.randint(1, 3)
        intensity = twinkle * random.uniform(0.2, 0.4)
        
        # Add golden sparkles
        if y-radius >= 0 and y+radius < height and x-radius >= 0 and x+radius < width:
            frame[y-radius:y+radius, x-radius:x+radius, 1] += intensity  # Green
            frame[y-radius:y+radius, x-radius:x+radius, 2] += intensity  # Red
    
    return frame

def apply_cinematic_grade(frame, progress):
    """Apply professional color grading"""
    
    # Film grain effect
    noise = np.random.normal(0, 0.01, frame.shape)
    frame = frame + noise
    
    # Vignette effect
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    y, x = np.ogrid[:height, :width]
    mask = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
    mask = mask / mask.max()
    
    vignette = 1 - (mask * 0.3)
    vignette = np.expand_dims(vignette, axis=2)
    frame = frame * vignette
    
    # Contrast and saturation boost
    frame = np.clip(frame * 1.1 + 0.05, 0, 1)
    
    return frame

def add_hook_overlay(frame, frame_idx, total_frames, prompt):
    """Add engaging text overlays for viral content"""
    
    # Convert OpenCV frame to PIL for text rendering
    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(frame_pil)
    
    # Define hook messages based on content
    hooks = []
    if any(word in prompt.lower() for word in ["cat", "dog", "animal", "pet"]):
        hooks = ["This is too cute! 😻", "Watch this amazing animal!", "You won't believe this!"]
    elif any(word in prompt.lower() for word in ["beautiful", "stunning", "amazing"]):
        hooks = ["This is breathtaking!", "Watch this incredible view!", "Amazing transformation!"]
    elif any(word in prompt.lower() for word in ["action", "fast", "speed", "racing"]):
        hooks = ["Watch this incredible move!", "This is insane!", "Speed like never before!"]
    else:
        hooks = ["This is amazing!", "Watch this!", "Incredible AI creation!"]
    
    # Show hook text in first 3 seconds
    if frame_idx < total_frames * 0.3:
        hook_text = random.choice(hooks)
        
        # Try to load a font, fallback to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Text positioning with animation
        text_y = 50 + int(10 * math.sin(frame_idx * 0.2))
        
        # Add text shadow
        draw.text((52, text_y + 2), hook_text, font=font, fill=(0, 0, 0, 128))
        # Add main text
        draw.text((50, text_y), hook_text, font=font, fill=(255, 255, 255, 255))
    
    # Add call-to-action in last 2 seconds
    elif frame_idx > total_frames * 0.8:
        cta_text = "Follow for more AI magic! ✨"
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        except:
            font = ImageFont.load_default()
        
        text_y = frame_pil.height - 100
        
        # Add text shadow
        draw.text((52, text_y + 2), cta_text, font=font, fill=(0, 0, 0, 128))
        # Add main text
        draw.text((50, text_y), cta_text, font=font, fill=(255, 255, 255, 255))
    
    # Convert back to OpenCV format
    frame_final = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
    
    return frame_final