import os
import uuid
import requests
import logging
from PIL import Image, ImageDraw, ImageFont
import io
import json
import time
from datetime import datetime

class FreeImageGenerator:
    """Free image generation using multiple methods"""
    
    def __init__(self):
        self.images_dir = os.path.join('static', 'images')
        os.makedirs(self.images_dir, exist_ok=True)
        
    def generate_image(self, prompt):
        """
        Generate image using free methods
        Priority: Hugging Face API -> Pollinations API -> Local generation
        """
        try:
            # Method 1: Try Pollinations API (completely free, no API key needed)
            result = self._generate_with_pollinations(prompt)
            if result:
                return result
                
            # Method 2: Try Hugging Face Inference API (free tier)
            result = self._generate_with_huggingface(prompt)
            if result:
                return result
                
            # Method 3: Local procedural generation based on prompt
            return self._generate_locally(prompt)
            
        except Exception as e:
            logging.error(f"Error in generate_image: {str(e)}")
            return self._generate_locally(prompt)
    
    def _generate_with_pollinations(self, prompt):
        """Generate image using Pollinations API (completely free)"""
        try:
            # Pollinations.ai provides free image generation
            url = "https://image.pollinations.ai/prompt/"
            from urllib.parse import quote
            encoded_prompt = quote(prompt)
            
            # Add quality parameters
            params = {
                'width': 512,
                'height': 512,
                'seed': -1,  # Random seed
                'nologo': 'true'
            }
            
            full_url = f"{url}{encoded_prompt}"
            
            logging.info(f"Generating image with Pollinations API: {prompt[:50]}...")
            
            response = requests.get(full_url, params=params, timeout=30)
            
            if response.status_code == 200:
                # Save the image
                filename = f"generated_{uuid.uuid4().hex[:8]}.jpg"
                filepath = os.path.join(self.images_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                logging.info(f"Successfully generated image: {filename}")
                return filename
                
        except Exception as e:
            logging.warning(f"Pollinations API failed: {str(e)}")
            return None
    
    def _generate_with_huggingface(self, prompt):
        """Generate image using Hugging Face Inference API"""
        try:
            # Use free Hugging Face models
            api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            
            headers = {
                "Content-Type": "application/json",
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "width": 512,
                    "height": 512,
                    "num_inference_steps": 20
                }
            }
            
            logging.info(f"Generating image with Hugging Face API: {prompt[:50]}...")
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                # Save the image
                filename = f"generated_{uuid.uuid4().hex[:8]}.jpg"
                filepath = os.path.join(self.images_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                logging.info(f"Successfully generated image: {filename}")
                return filename
                
        except Exception as e:
            logging.warning(f"Hugging Face API failed: {str(e)}")
            return None
    
    def _generate_locally(self, prompt):
        """Generate image locally using prompt analysis and PIL"""
        try:
            logging.info(f"Generating image locally: {prompt[:50]}...")
            
            # Analyze prompt for visual elements
            analysis = self._analyze_prompt(prompt)
            
            # Create image based on analysis
            img = Image.new('RGB', (512, 512), color=analysis['background_color'])
            draw = ImageDraw.Draw(img)
            
            # Add visual elements based on prompt
            self._draw_elements(draw, analysis, 512, 512)
            
            # Save the image
            filename = f"generated_{uuid.uuid4().hex[:8]}.png"
            filepath = os.path.join(self.images_dir, filename)
            img.save(filepath, 'PNG', quality=95)
            
            logging.info(f"Successfully generated local image: {filename}")
            return filename
            
        except Exception as e:
            logging.error(f"Local generation failed: {str(e)}")
            return self._create_fallback_image(prompt)
    
    def _analyze_prompt(self, prompt):
        """Analyze prompt to determine visual elements"""
        prompt_lower = prompt.lower()
        
        # Color mapping
        color_keywords = {
            'red': (220, 20, 20),
            'blue': (20, 20, 220),
            'green': (20, 220, 20),
            'yellow': (220, 220, 20),
            'purple': (139, 92, 246),
            'orange': (245, 158, 11),
            'pink': (236, 72, 153),
            'black': (30, 30, 30),
            'white': (245, 245, 245),
            'gray': (128, 128, 128),
            'brown': (139, 69, 19),
            'gold': (255, 215, 0),
            'silver': (192, 192, 192)
        }
        
        # Default to gradient background
        background = (99, 102, 241)  # Primary blue
        
        # Check for color keywords
        for color, rgb in color_keywords.items():
            if color in prompt_lower:
                background = rgb
                break
        
        # Object detection
        objects = []
        object_keywords = {
            'cat': 'animal',
            'dog': 'animal',
            'tree': 'nature',
            'flower': 'nature',
            'house': 'building',
            'car': 'vehicle',
            'sun': 'celestial',
            'moon': 'celestial',
            'star': 'celestial',
            'mountain': 'landscape',
            'ocean': 'landscape',
            'forest': 'landscape',
            'city': 'urban',
            'person': 'human',
            'bird': 'animal',
            'fish': 'animal'
        }
        
        for keyword, category in object_keywords.items():
            if keyword in prompt_lower:
                objects.append({'type': keyword, 'category': category})
        
        # Style detection
        style = 'realistic'
        style_keywords = {
            'abstract': 'abstract',
            'cartoon': 'cartoon',
            'realistic': 'realistic',
            'artistic': 'artistic',
            'modern': 'modern',
            'vintage': 'vintage',
            'minimalist': 'minimalist'
        }
        
        for keyword, style_type in style_keywords.items():
            if keyword in prompt_lower:
                style = style_type
                break
        
        return {
            'background_color': background,
            'objects': objects,
            'style': style,
            'prompt': prompt
        }
    
    def _draw_elements(self, draw, analysis, width, height):
        """Draw visual elements based on prompt analysis"""
        try:
            # Create gradient background
            self._draw_gradient_background(draw, analysis['background_color'], width, height)
            
            # Draw objects based on detected elements
            for obj in analysis['objects']:
                self._draw_object(draw, obj, width, height)
            
            # Add decorative elements
            self._add_decorative_elements(draw, analysis, width, height)
            
        except Exception as e:
            logging.warning(f"Error drawing elements: {str(e)}")
    
    def _draw_gradient_background(self, draw, base_color, width, height):
        """Create gradient background"""
        r, g, b = base_color
        
        for y in range(height):
            # Create vertical gradient
            ratio = y / height
            new_r = int(r * (1 - ratio * 0.3))
            new_g = int(g * (1 - ratio * 0.3))
            new_b = int(b * (1 - ratio * 0.3))
            
            color = (max(0, new_r), max(0, new_g), max(0, new_b))
            draw.line([(0, y), (width, y)], fill=color)
    
    def _draw_object(self, draw, obj, width, height):
        """Draw specific objects based on type"""
        obj_type = obj['type']
        
        if obj_type == 'cat':
            self._draw_cat(draw, width, height)
        elif obj_type == 'dog':
            self._draw_dog(draw, width, height)
        elif obj_type == 'tree':
            self._draw_tree(draw, width, height)
        elif obj_type == 'sun':
            self._draw_sun(draw, width, height)
        elif obj_type == 'house':
            self._draw_house(draw, width, height)
        elif obj_type == 'mountain':
            self._draw_mountain(draw, width, height)
        else:
            # Generic shape for unknown objects
            self._draw_generic_shape(draw, width, height)
    
    def _draw_cat(self, draw, width, height):
        """Draw a stylized cat"""
        center_x, center_y = width // 2, height // 2
        
        # Cat body (ellipse)
        body_width, body_height = 120, 80
        draw.ellipse([
            center_x - body_width//2, center_y - body_height//2 + 20,
            center_x + body_width//2, center_y + body_height//2 + 20
        ], fill=(80, 80, 80), outline=(60, 60, 60))
        
        # Cat head (circle)
        head_radius = 50
        draw.ellipse([
            center_x - head_radius, center_y - head_radius - 30,
            center_x + head_radius, center_y + head_radius - 30
        ], fill=(90, 90, 90), outline=(70, 70, 70))
        
        # Cat ears (triangles)
        ear_size = 25
        # Left ear
        draw.polygon([
            (center_x - 30, center_y - 60),
            (center_x - 30 - ear_size, center_y - 80),
            (center_x - 30 + ear_size//2, center_y - 75)
        ], fill=(100, 100, 100))
        
        # Right ear
        draw.polygon([
            (center_x + 30, center_y - 60),
            (center_x + 30 + ear_size, center_y - 80),
            (center_x + 30 - ear_size//2, center_y - 75)
        ], fill=(100, 100, 100))
        
        # Eyes
        draw.ellipse([center_x - 25, center_y - 50, center_x - 15, center_y - 40], fill=(0, 255, 0))
        draw.ellipse([center_x + 15, center_y - 50, center_x + 25, center_y - 40], fill=(0, 255, 0))
        
        # Nose
        draw.polygon([
            (center_x, center_y - 35),
            (center_x - 5, center_y - 25),
            (center_x + 5, center_y - 25)
        ], fill=(255, 192, 203))
        
        # Tail
        draw.arc([center_x + 50, center_y - 10, center_x + 100, center_y + 40], 
                 start=0, end=180, fill=(80, 80, 80), width=8)
    
    def _draw_dog(self, draw, width, height):
        """Draw a stylized dog"""
        center_x, center_y = width // 2, height // 2
        
        # Dog body
        draw.ellipse([center_x - 60, center_y, center_x + 60, center_y + 80], 
                    fill=(139, 69, 19), outline=(101, 67, 33))
        
        # Dog head
        draw.ellipse([center_x - 40, center_y - 60, center_x + 40, center_y + 20], 
                    fill=(160, 82, 45), outline=(139, 69, 19))
        
        # Ears
        draw.ellipse([center_x - 50, center_y - 40, center_x - 20, center_y - 10], 
                    fill=(101, 67, 33))
        draw.ellipse([center_x + 20, center_y - 40, center_x + 50, center_y - 10], 
                    fill=(101, 67, 33))
        
        # Eyes
        draw.ellipse([center_x - 20, center_y - 30, center_x - 10, center_y - 20], fill=(0, 0, 0))
        draw.ellipse([center_x + 10, center_y - 30, center_x + 20, center_y - 20], fill=(0, 0, 0))
        
        # Nose
        draw.ellipse([center_x - 5, center_y - 10, center_x + 5, center_y], fill=(0, 0, 0))
    
    def _draw_tree(self, draw, width, height):
        """Draw a stylized tree"""
        center_x = width // 2
        ground_y = height - 50
        
        # Tree trunk
        trunk_width = 20
        trunk_height = 100
        draw.rectangle([
            center_x - trunk_width//2, ground_y - trunk_height,
            center_x + trunk_width//2, ground_y
        ], fill=(101, 67, 33), outline=(83, 53, 13))
        
        # Tree crown (multiple circles for foliage)
        crown_colors = [(34, 139, 34), (50, 205, 50), (0, 128, 0)]
        
        for i, color in enumerate(crown_colors):
            radius = 50 - i * 10
            offset_y = i * 15
            draw.ellipse([
                center_x - radius, ground_y - trunk_height - radius + offset_y,
                center_x + radius, ground_y - trunk_height + radius + offset_y
            ], fill=color, outline=(0, 100, 0))
    
    def _draw_sun(self, draw, width, height):
        """Draw a stylized sun"""
        sun_x, sun_y = width - 100, 100
        sun_radius = 40
        
        # Sun rays
        ray_length = 20
        for angle in range(0, 360, 45):
            import math
            rad = math.radians(angle)
            start_x = sun_x + (sun_radius + 5) * math.cos(rad)
            start_y = sun_y + (sun_radius + 5) * math.sin(rad)
            end_x = sun_x + (sun_radius + ray_length) * math.cos(rad)
            end_y = sun_y + (sun_radius + ray_length) * math.sin(rad)
            draw.line([(start_x, start_y), (end_x, end_y)], fill=(255, 255, 0), width=3)
        
        # Sun body
        draw.ellipse([
            sun_x - sun_radius, sun_y - sun_radius,
            sun_x + sun_radius, sun_y + sun_radius
        ], fill=(255, 215, 0), outline=(255, 165, 0))
    
    def _draw_house(self, draw, width, height):
        """Draw a stylized house"""
        center_x = width // 2
        ground_y = height - 80
        
        house_width = 120
        house_height = 80
        
        # House body
        draw.rectangle([
            center_x - house_width//2, ground_y - house_height,
            center_x + house_width//2, ground_y
        ], fill=(139, 69, 19), outline=(101, 67, 33))
        
        # Roof
        draw.polygon([
            (center_x - house_width//2 - 10, ground_y - house_height),
            (center_x, ground_y - house_height - 40),
            (center_x + house_width//2 + 10, ground_y - house_height)
        ], fill=(178, 34, 34), outline=(139, 0, 0))
        
        # Door
        door_width = 25
        door_height = 50
        draw.rectangle([
            center_x - door_width//2, ground_y - door_height,
            center_x + door_width//2, ground_y
        ], fill=(101, 67, 33), outline=(83, 53, 13))
        
        # Windows
        window_size = 20
        draw.rectangle([
            center_x - 40, ground_y - 60,
            center_x - 40 + window_size, ground_y - 60 + window_size
        ], fill=(135, 206, 235), outline=(0, 0, 139))
        
        draw.rectangle([
            center_x + 20, ground_y - 60,
            center_x + 20 + window_size, ground_y - 60 + window_size
        ], fill=(135, 206, 235), outline=(0, 0, 139))
    
    def _draw_mountain(self, draw, width, height):
        """Draw stylized mountains"""
        ground_y = height - 50
        
        # Multiple mountain peaks
        mountains = [
            {'peak_x': width // 4, 'height': 150, 'width': 100},
            {'peak_x': width // 2, 'height': 200, 'width': 120},
            {'peak_x': 3 * width // 4, 'height': 180, 'width': 110}
        ]
        
        mountain_colors = [(105, 105, 105), (128, 128, 128), (119, 136, 153)]
        
        for i, mountain in enumerate(mountains):
            color = mountain_colors[i % len(mountain_colors)]
            peak_x = mountain['peak_x']
            peak_height = mountain['height']
            peak_width = mountain['width']
            
            draw.polygon([
                (peak_x - peak_width//2, ground_y),
                (peak_x, ground_y - peak_height),
                (peak_x + peak_width//2, ground_y)
            ], fill=color, outline=(color[0]-20, color[1]-20, color[2]-20))
    
    def _draw_generic_shape(self, draw, width, height):
        """Draw generic decorative shape"""
        center_x, center_y = width // 2, height // 2
        
        # Abstract geometric shape
        draw.ellipse([
            center_x - 40, center_y - 40,
            center_x + 40, center_y + 40
        ], fill=(139, 92, 246), outline=(99, 102, 241))
        
        draw.rectangle([
            center_x - 20, center_y - 60,
            center_x + 20, center_y + 60
        ], fill=(99, 102, 241, 128), outline=(139, 92, 246))
    
    def _add_decorative_elements(self, draw, analysis, width, height):
        """Add decorative elements like stars, patterns"""
        # Add some stars or sparkles
        import random
        
        for _ in range(8):
            x = random.randint(20, width - 20)
            y = random.randint(20, height // 3)
            size = random.randint(2, 5)
            
            draw.ellipse([x-size, y-size, x+size, y+size], 
                        fill=(255, 255, 255, 180))
    
    def _create_fallback_image(self, prompt):
        """Create simple fallback image"""
        try:
            img = Image.new('RGB', (512, 512), color=(99, 102, 241))
            draw = ImageDraw.Draw(img)
            
            # Simple text-based image
            try:
                # Try to use a better font
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Add prompt text
            text = f"Generated:\n{prompt[:30]}..."
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (512 - text_width) // 2
            y = (512 - text_height) // 2
            
            draw.text((x, y), text, fill=(255, 255, 255), font=font)
            
            # Save fallback image
            filename = f"generated_{uuid.uuid4().hex[:8]}.png"
            filepath = os.path.join(self.images_dir, filename)
            img.save(filepath, 'PNG')
            
            return filename
            
        except Exception as e:
            logging.error(f"Fallback creation failed: {str(e)}")
            return "placeholder-1.svg"