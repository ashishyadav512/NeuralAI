import os
import uuid
import requests
import logging
from datetime import datetime
import json
import time

class FreeVideoGenerator:
    """Free video generation using multiple methods"""
    
    def __init__(self):
        self.videos_dir = os.path.join('static', 'videos')
        os.makedirs(self.videos_dir, exist_ok=True)
        
    def generate_video(self, prompt):
        """
        Generate video using real AI images with animation effects
        Priority: AI image + animation -> Simple animation backup
        """
        try:
            # Method 1: Generate high-quality AI image first, then animate it
            result = self._generate_ai_image_video(prompt)
            if result:
                return result
                
            # Method 2: Fallback to simple animation
            return self._create_simple_video(prompt)
            
        except Exception as e:
            logging.error(f"Error in generate_video: {str(e)}")
            return self._create_fallback_video(prompt)
    
    def _generate_ai_image_video(self, prompt):
        """Generate video by first creating AI image, then animating it"""
        try:
            import requests
            from PIL import Image, ImageEnhance, ImageFilter
            import io
            import uuid
            import math
            
            logging.info(f"Generating AI image video for: {prompt[:50]}...")
            
            # Step 1: Generate high-quality AI image using Pollinations API
            base_url = "https://image.pollinations.ai/prompt/"
            from urllib.parse import quote
            
            encoded_prompt = quote(f"{prompt}, high quality, detailed, cinematic")
            params = {
                'width': 512,
                'height': 512,
                'seed': -1,
                'nologo': 'true'
            }
            
            full_url = f"{base_url}{encoded_prompt}"
            
            logging.info("Generating base AI image...")
            response = requests.get(full_url, params=params, timeout=20)
            
            if response.status_code != 200:
                logging.warning("AI image generation failed, using fallback")
                return None
                
            # Load the AI-generated base image
            base_image = Image.open(io.BytesIO(response.content))
            base_image = base_image.convert('RGB')
            
            logging.info("Creating animated frames from AI image...")
            
            # Step 2: Create animated frames with effects on the AI image
            frames = []
            frame_count = 12  # More frames for smoother animation
            
            for frame_num in range(frame_count):
                # Copy the base AI image
                frame = base_image.copy()
                
                # Animation progress (0 to 1)
                progress = frame_num / frame_count
                
                # Apply different animation effects based on prompt content
                if any(word in prompt.lower() for word in ['fire', 'flame', 'burning', 'dragon']):
                    frame = self._apply_fire_effect(frame, progress)
                elif any(word in prompt.lower() for word in ['water', 'ocean', 'wave', 'rain', 'sea']):
                    frame = self._apply_water_effect(frame, progress)
                elif any(word in prompt.lower() for word in ['wind', 'flying', 'moving', 'floating', 'car', 'running']):
                    frame = self._apply_motion_effect(frame, progress)
                elif any(word in prompt.lower() for word in ['magic', 'spell', 'glow', 'energy', 'fantasy', 'warrior', 'armor', 'sword']):
                    frame = self._apply_glow_effect(frame, progress)
                elif any(word in prompt.lower() for word in ['night', 'dark', 'moon', 'stars', 'city']):
                    frame = self._apply_night_effect(frame, progress)
                elif any(word in prompt.lower() for word in ['portrait', 'face', 'person', 'girl', 'boy', 'man', 'woman']):
                    frame = self._apply_portrait_effect(frame, progress)
                else:
                    # Default subtle animation - breathing/pulsing effect
                    frame = self._apply_breathing_effect(frame, progress)
                
                frames.append(frame)
            
            # Step 3: Save as animated GIF
            filename = f"ai_video_{uuid.uuid4().hex[:8]}.gif"
            filepath = os.path.join(self.videos_dir, filename)
            
            frames[0].save(
                filepath,
                save_all=True,
                append_images=frames[1:],
                duration=200,  # 200ms per frame for smooth animation
                loop=0
            )
            
            logging.info(f"AI image video created: {filename}")
            return filename
            
        except Exception as e:
            logging.error(f"AI image video generation failed: {str(e)}")
            return None
    
    def _apply_breathing_effect(self, image, progress):
        """Apply subtle breathing/pulsing effect"""
        try:
            import math
            from PIL import Image, ImageEnhance
            
            # Subtle zoom in/out effect
            scale_factor = 1.0 + math.sin(progress * 2 * math.pi) * 0.02
            
            width, height = image.size
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            
            # Resize image
            resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Center crop back to original size
            left = (new_width - width) // 2
            top = (new_height - height) // 2
            result = resized.crop((left, top, left + width, top + height))
            
            # Subtle brightness variation
            brightness = 1.0 + math.sin(progress * 2 * math.pi) * 0.05
            enhancer = ImageEnhance.Brightness(result)
            result = enhancer.enhance(brightness)
            
            return result
        except:
            return image
    
    def _apply_glow_effect(self, image, progress):
        """Apply magical glow effect"""
        try:
            import math
            from PIL import ImageEnhance, ImageFilter
            
            # Create glowing effect with brightness and blur
            brightness = 1.1 + math.sin(progress * 4 * math.pi) * 0.15
            
            # Enhance brightness
            enhancer = ImageEnhance.Brightness(image)
            bright_image = enhancer.enhance(brightness)
            
            # Add subtle blur for glow
            if brightness > 1.1:
                blur_radius = (brightness - 1.0) * 2
                bright_image = bright_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            
            return bright_image
        except:
            return image
    
    def _apply_motion_effect(self, image, progress):
        """Apply motion blur effect"""
        try:
            import math
            from PIL import ImageFilter, Image as PILImage
            
            # Subtle motion blur effect
            motion_intensity = abs(math.sin(progress * 4 * math.pi)) * 1.5
            
            if motion_intensity > 0.5:
                # Apply motion blur
                blurred = image.filter(ImageFilter.BLUR)
                # Blend original with blurred
                from PIL import Image as PILImage
                result = PILImage.blend(image, blurred, motion_intensity * 0.3)
                return result
            
            return image
        except:
            return image
    
    def _apply_fire_effect(self, image, progress):
        """Apply fire-like flickering effect"""
        try:
            import math
            from PIL import ImageEnhance
            
            # Flickering brightness and color temperature
            flicker = 1.0 + math.sin(progress * 8 * math.pi) * 0.1 + math.sin(progress * 12 * math.pi) * 0.05
            
            # Enhance brightness with flicker
            enhancer = ImageEnhance.Brightness(image)
            result = enhancer.enhance(flicker)
            
            # Add warmth (increase red/yellow tones)
            enhancer = ImageEnhance.Color(result)
            result = enhancer.enhance(1.1 + flicker * 0.1)
            
            return result
        except:
            return image
    
    def _apply_water_effect(self, image, progress):
        """Apply water-like ripple effect"""
        try:
            # Subtle horizontal wave distortion simulation
            brightness = 1.0 + math.sin(progress * 3 * math.pi) * 0.03
            
            # Apply brightness wave
            enhancer = ImageEnhance.Brightness(image)
            result = enhancer.enhance(brightness)
            
            # Add subtle blue tint
            enhancer = ImageEnhance.Color(result)
            result = enhancer.enhance(1.05)
            
            return result
        except:
            return image
    
    def _apply_night_effect(self, image, progress):
        """Apply night scene effect with twinkling"""
        try:
            import math
            from PIL import ImageEnhance
            
            # Subtle brightness variation like twinkling stars
            twinkle = 1.0 + math.sin(progress * 6 * math.pi) * 0.08 + math.sin(progress * 10 * math.pi) * 0.04
            
            # Apply brightness variation
            enhancer = ImageEnhance.Brightness(image)
            result = enhancer.enhance(twinkle)
            
            # Slightly increase contrast for night effect
            enhancer = ImageEnhance.Contrast(result)
            result = enhancer.enhance(1.05)
            
            return result
        except:
            return image
    
    def _apply_portrait_effect(self, image, progress):
        """Apply subtle portrait animation effect"""
        try:
            import math
            from PIL import ImageEnhance
            
            # Very subtle breathing effect for portraits
            brightness = 1.0 + math.sin(progress * 2 * math.pi) * 0.03
            
            # Apply subtle brightness change
            enhancer = ImageEnhance.Brightness(image)
            result = enhancer.enhance(brightness)
            
            # Slight color enhancement
            enhancer = ImageEnhance.Color(result)
            result = enhancer.enhance(1.02)
            
            return result
        except:
            return image
    
    def _create_simple_video(self, prompt):
        """Create a simple video using basic animation"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import math
            
            logging.info(f"Creating simple video: {prompt[:50]}...")
            
            frames = []
            frame_count = 8  # Reduced frame count for speed
            width, height = 512, 512
            
            # Simple color-based animation
            base_color = (99, 102, 241)  # Primary color
            
            for frame_num in range(frame_count):
                # Create frame with animated background
                img = Image.new('RGB', (width, height), color=base_color)
                draw = ImageDraw.Draw(img)
                
                # Animation progress
                progress = frame_num / frame_count
                
                # Simple animated elements
                center_x, center_y = width // 2, height // 2
                
                # Pulsing circle
                radius = 50 + int(math.sin(progress * 4 * math.pi) * 20)
                draw.ellipse([
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius
                ], fill=(255, 255, 255, 200), outline=(200, 200, 200))
                
                # Moving elements based on prompt
                if 'cat' in prompt.lower():
                    # Simple cat-like shape that moves
                    offset_x = math.sin(progress * 2 * math.pi) * 30
                    cat_x = center_x + offset_x
                    draw.ellipse([cat_x - 20, center_y - 10, cat_x + 20, center_y + 10], fill=(150, 150, 150))
                    # Ears
                    draw.polygon([(cat_x - 15, center_y - 10), (cat_x - 25, center_y - 25), (cat_x - 5, center_y - 15)], fill=(160, 160, 160))
                    draw.polygon([(cat_x + 5, center_y - 15), (cat_x + 25, center_y - 25), (cat_x + 15, center_y - 10)], fill=(160, 160, 160))
                
                # Add text overlay
                try:
                    font = ImageFont.load_default()
                    text = f"AI Video: {prompt[:20]}..."
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    draw.text(((width - text_width) // 2, height - 40), text, fill=(255, 255, 255), font=font)
                except:
                    pass
                
                frames.append(img)
            
            # Save as GIF
            filename = f"video_{uuid.uuid4().hex[:8]}.gif"
            filepath = os.path.join(self.videos_dir, filename)
            
            frames[0].save(
                filepath,
                save_all=True,
                append_images=frames[1:],
                duration=150,  # 150ms per frame
                loop=0
            )
            
            logging.info(f"Simple video created: {filename}")
            return filename
            
        except Exception as e:
            logging.error(f"Simple video creation failed: {str(e)}")
            return None
    
    def _generate_with_pollinations_video(self, prompt):
        """Generate video using Pollinations Video API"""
        try:
            # Create a series of images for video frames
            base_url = "https://image.pollinations.ai/prompt/"
            from urllib.parse import quote
            
            # Generate 5 frames with slight variations (faster generation)
            frames = []
            for i in range(5):
                frame_prompt = f"{prompt}, frame {i+1}, slight variation, cinematic"
                encoded_prompt = quote(frame_prompt)
                
                params = {
                    'width': 512,
                    'height': 512,
                    'seed': i * 100,  # Different seed for each frame
                    'nologo': 'true'
                }
                
                full_url = f"{base_url}{encoded_prompt}"
                
                logging.info(f"Generating video frame {i+1}/5...")
                
                response = requests.get(full_url, params=params, timeout=15)
                
                if response.status_code == 200:
                    frame_filename = f"frame_{i:03d}.jpg"
                    frame_path = os.path.join(self.videos_dir, frame_filename)
                    
                    with open(frame_path, 'wb') as f:
                        f.write(response.content)
                    
                    frames.append(frame_path)
                else:
                    logging.warning(f"Failed to generate frame {i+1}")
                    break
                
                # Small delay to avoid rate limiting
                time.sleep(0.2)
            
            if len(frames) >= 3:  # Need at least 3 frames
                # Convert frames to GIF
                video_filename = self._create_gif_from_frames(frames, prompt)
                
                # Clean up frame files
                for frame_path in frames:
                    try:
                        os.remove(frame_path)
                    except:
                        pass
                
                return video_filename
                
        except Exception as e:
            logging.warning(f"Pollinations video generation failed: {str(e)}")
            return None
    
    def _generate_with_huggingface_video(self, prompt):
        """Generate video using Hugging Face Video Models"""
        try:
            # Use Hugging Face Inference API for video generation
            api_urls = [
                "https://api-inference.huggingface.co/models/ali-vilab/text-to-video-ms-1.7b",
                "https://api-inference.huggingface.co/models/damo-vilab/text-to-video-ms-1.7b"
            ]
            
            for api_url in api_urls:
                try:
                    headers = {
                        "Content-Type": "application/json",
                    }
                    
                    payload = {
                        "inputs": prompt,
                        "parameters": {
                            "num_frames": 16,
                            "fps": 8
                        }
                    }
                    
                    logging.info(f"Generating video with Hugging Face: {prompt[:50]}...")
                    
                    response = requests.post(api_url, headers=headers, json=payload, timeout=120)
                    
                    if response.status_code == 200:
                        # Save the video
                        filename = f"video_{uuid.uuid4().hex[:8]}.mp4"
                        filepath = os.path.join(self.videos_dir, filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        
                        logging.info(f"Successfully generated video: {filename}")
                        return filename
                        
                except Exception as api_error:
                    logging.warning(f"HuggingFace API {api_url} failed: {str(api_error)}")
                    continue
                    
        except Exception as e:
            logging.warning(f"Hugging Face video generation failed: {str(e)}")
            return None
    
    def _generate_animated_gif(self, prompt):
        """Generate animated GIF locally using PIL"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import math
            
            logging.info(f"Generating animated GIF locally: {prompt[:50]}...")
            
            # Create frames for animation
            frames = []
            frame_count = 20
            width, height = 512, 512
            
            # Analyze prompt for animation elements
            analysis = self._analyze_video_prompt(prompt)
            
            for frame_num in range(frame_count):
                # Create frame
                img = Image.new('RGB', (width, height), color=analysis['background_color'])
                draw = ImageDraw.Draw(img)
                
                # Calculate animation progress (0 to 1)
                progress = frame_num / frame_count
                
                # Draw animated elements
                self._draw_animated_frame(draw, analysis, width, height, progress)
                
                frames.append(img)
            
            # Save as animated GIF
            filename = f"video_{uuid.uuid4().hex[:8]}.gif"
            filepath = os.path.join(self.videos_dir, filename)
            
            # Save animated GIF
            frames[0].save(
                filepath,
                save_all=True,
                append_images=frames[1:],
                duration=100,  # 100ms per frame = 10fps
                loop=0
            )
            
            logging.info(f"Successfully generated animated GIF: {filename}")
            return filename
            
        except Exception as e:
            logging.error(f"Animated GIF generation failed: {str(e)}")
            return self._create_fallback_video(prompt)
    
    def _create_gif_from_frames(self, frame_paths, prompt):
        """Create GIF from individual frame images"""
        try:
            from PIL import Image
            
            frames = []
            for frame_path in frame_paths:
                img = Image.open(frame_path)
                # Resize if needed
                img = img.resize((512, 512), Image.Resampling.LANCZOS)
                frames.append(img)
            
            filename = f"video_{uuid.uuid4().hex[:8]}.gif"
            filepath = os.path.join(self.videos_dir, filename)
            
            # Save as animated GIF
            frames[0].save(
                filepath,
                save_all=True,
                append_images=frames[1:],
                duration=200,  # 200ms per frame = 5fps
                loop=0
            )
            
            return filename
            
        except Exception as e:
            logging.error(f"GIF creation from frames failed: {str(e)}")
            return self._create_fallback_video(prompt)
    
    def _analyze_video_prompt(self, prompt):
        """Analyze prompt for video animation elements"""
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
            'cyberpunk': (0, 255, 255),
            'neon': (57, 255, 20),
            'sunset': (255, 94, 77)
        }
        
        background = (99, 102, 241)  # Default
        
        for color, rgb in color_keywords.items():
            if color in prompt_lower:
                background = rgb
                break
        
        # Animation type detection
        animation_type = 'fade'
        animation_keywords = {
            'rotating': 'rotate',
            'spinning': 'rotate',
            'flying': 'fly',
            'floating': 'float',
            'pulsing': 'pulse',
            'glowing': 'glow',
            'moving': 'move',
            'dancing': 'dance',
            'flowing': 'flow'
        }
        
        for keyword, anim_type in animation_keywords.items():
            if keyword in prompt_lower:
                animation_type = anim_type
                break
        
        # Object detection for animation
        objects = []
        object_keywords = {
            'cat': 'animal',
            'car': 'vehicle',
            'city': 'urban',
            'star': 'celestial',
            'fire': 'element',
            'water': 'element',
            'bird': 'animal',
            'tree': 'nature'
        }
        
        for keyword, category in object_keywords.items():
            if keyword in prompt_lower:
                objects.append({'type': keyword, 'category': category})
        
        return {
            'background_color': background,
            'animation_type': animation_type,
            'objects': objects,
            'prompt': prompt
        }
    
    def _draw_animated_frame(self, draw, analysis, width, height, progress):
        """Draw animated frame based on analysis and progress"""
        import math
        
        # Create animated background
        self._draw_animated_background(draw, analysis, width, height, progress)
        
        # Draw animated objects
        for obj in analysis['objects']:
            self._draw_animated_object(draw, obj, width, height, progress, analysis['animation_type'])
        
        # Add animated effects
        self._add_animated_effects(draw, analysis, width, height, progress)
    
    def _draw_animated_background(self, draw, analysis, width, height, progress):
        """Create animated background"""
        import math
        
        r, g, b = analysis['background_color']
        
        # Animated gradient
        for y in range(height):
            ratio = y / height
            
            # Add animation effect
            wave = math.sin(progress * 2 * math.pi + ratio * 4) * 0.2
            
            new_r = int(r * (1 - ratio * 0.3 + wave))
            new_g = int(g * (1 - ratio * 0.3 + wave))
            new_b = int(b * (1 - ratio * 0.3 + wave))
            
            color = (max(0, min(255, new_r)), max(0, min(255, new_g)), max(0, min(255, new_b)))
            draw.line([(0, y), (width, y)], fill=color)
    
    def _draw_animated_object(self, draw, obj, width, height, progress, animation_type):
        """Draw animated objects"""
        import math
        
        center_x, center_y = width // 2, height // 2
        
        if animation_type == 'rotate':
            # Rotating animation
            angle = progress * 2 * math.pi
            offset_x = math.cos(angle) * 50
            offset_y = math.sin(angle) * 50
            pos_x = center_x + offset_x
            pos_y = center_y + offset_y
            
        elif animation_type == 'pulse':
            # Pulsing animation
            scale = 1 + math.sin(progress * 4 * math.pi) * 0.3
            pos_x, pos_y = center_x, center_y
            
        elif animation_type == 'float':
            # Floating animation
            pos_x = center_x
            pos_y = center_y + math.sin(progress * 2 * math.pi) * 30
            
        else:
            # Default fade animation
            pos_x, pos_y = center_x, center_y
        
        # Draw object based on type
        if obj['type'] == 'cat':
            self._draw_animated_cat(draw, pos_x, pos_y, progress, animation_type)
        elif obj['type'] == 'car':
            self._draw_animated_car(draw, pos_x, pos_y, progress, animation_type)
        elif obj['type'] == 'star':
            self._draw_animated_star(draw, pos_x, pos_y, progress, animation_type)
        else:
            self._draw_animated_generic(draw, pos_x, pos_y, progress, animation_type)
    
    def _draw_animated_cat(self, draw, x, y, progress, animation_type):
        """Draw animated cat"""
        import math
        
        # Cat with blinking animation
        blink = math.sin(progress * 8 * math.pi) > 0.8
        
        # Body
        draw.ellipse([x-40, y-10, x+40, y+30], fill=(100, 100, 100))
        
        # Head
        draw.ellipse([x-25, y-40, x+25, y+10], fill=(120, 120, 120))
        
        # Ears
        draw.polygon([(x-20, y-35), (x-30, y-50), (x-10, y-45)], fill=(130, 130, 130))
        draw.polygon([(x+10, y-45), (x+30, y-50), (x+20, y-35)], fill=(130, 130, 130))
        
        # Eyes (blinking)
        if not blink:
            draw.ellipse([x-15, y-25, x-10, y-20], fill=(0, 255, 0))
            draw.ellipse([x+10, y-25, x+15, y-20], fill=(0, 255, 0))
        else:
            draw.line([(x-15, y-22), (x-10, y-22)], fill=(0, 0, 0), width=2)
            draw.line([(x+10, y-22), (x+15, y-22)], fill=(0, 0, 0), width=2)
        
        # Tail (swaying)
        tail_angle = math.sin(progress * 4 * math.pi) * 0.5
        tail_x = x + 35 + math.cos(tail_angle) * 15
        tail_y = y + math.sin(tail_angle) * 10
        draw.ellipse([tail_x-5, tail_y-5, tail_x+5, tail_y+5], fill=(90, 90, 90))
    
    def _draw_animated_car(self, draw, x, y, progress, animation_type):
        """Draw animated car"""
        # Moving car
        car_x = x + (progress - 0.5) * 200
        
        # Car body
        draw.rectangle([car_x-30, y-10, car_x+30, y+10], fill=(255, 0, 0))
        
        # Windows
        draw.rectangle([car_x-20, y-8, car_x+20, y-2], fill=(135, 206, 235))
        
        # Wheels
        draw.ellipse([car_x-25, y+5, car_x-15, y+15], fill=(50, 50, 50))
        draw.ellipse([car_x+15, y+5, car_x+25, y+15], fill=(50, 50, 50))
    
    def _draw_animated_star(self, draw, x, y, progress, animation_type):
        """Draw animated star"""
        import math
        
        # Twinkling star
        brightness = (math.sin(progress * 6 * math.pi) + 1) / 2
        color_val = int(255 * brightness)
        
        # Star shape
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = 20
            else:
                radius = 10
            
            star_x = x + math.cos(angle) * radius
            star_y = y + math.sin(angle) * radius
            points.append((star_x, star_y))
        
        draw.polygon(points, fill=(color_val, color_val, 0))
    
    def _draw_animated_generic(self, draw, x, y, progress, animation_type):
        """Draw generic animated shape"""
        import math
        
        # Pulsing circle
        scale = 1 + math.sin(progress * 4 * math.pi) * 0.3
        radius = int(30 * scale)
        
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                    fill=(139, 92, 246), outline=(99, 102, 241))
    
    def _add_animated_effects(self, draw, analysis, width, height, progress):
        """Add animated particle effects"""
        import math
        import random
        
        # Animated particles
        random.seed(int(progress * 100))  # Consistent randomness
        
        for i in range(15):
            particle_x = random.randint(0, width)
            particle_y = random.randint(0, height)
            
            # Animate particle position
            offset = math.sin(progress * 2 * math.pi + i) * 20
            particle_x += offset
            particle_y += math.cos(progress * 2 * math.pi + i) * 10
            
            # Ensure particles stay in bounds
            particle_x = max(0, min(width, particle_x))
            particle_y = max(0, min(height, particle_y))
            
            size = 2 + math.sin(progress * 4 * math.pi + i) * 1
            alpha = int((math.sin(progress * 3 * math.pi + i) + 1) * 127)
            
            draw.ellipse([
                particle_x - size, particle_y - size,
                particle_x + size, particle_y + size
            ], fill=(255, 255, 255, alpha))
    
    def _create_fallback_video(self, prompt):
        """Create simple fallback video"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            frames = []
            for i in range(10):
                img = Image.new('RGB', (512, 512), color=(99, 102, 241))
                draw = ImageDraw.Draw(img)
                
                # Simple text animation
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
                except:
                    font = ImageFont.load_default()
                
                text = f"Video: {prompt[:20]}...\nFrame {i+1}/10"
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x = (512 - text_width) // 2
                y = (512 - text_height) // 2
                
                draw.text((x, y), text, fill=(255, 255, 255), font=font)
                frames.append(img)
            
            filename = f"video_{uuid.uuid4().hex[:8]}.gif"
            filepath = os.path.join(self.videos_dir, filename)
            
            frames[0].save(
                filepath,
                save_all=True,
                append_images=frames[1:],
                duration=300,
                loop=0
            )
            
            return filename
            
        except Exception as e:
            logging.error(f"Fallback video creation failed: {str(e)}")
            return None