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
                'width': 1024,
                'height': 1024,
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
            
            # Step 2: Generate multiple AI images for different action stages
            logging.info("Generating action sequence images...")
            
            # Create action-based prompts for different stages
            action_prompts = self._generate_action_sequence_prompts(prompt)
            
            # Generate only key action images (reduced from full sequence for speed)
            action_images = [base_image]  # Start with base image
            
            # Generate MULTIPLE distinct action frames for true motion sequences
            logging.info("Generating multiple action sequence frames for realistic motion...")
            
            # Generate only 2-3 critical motion frames for optimal performance
            if action_prompts:
                max_frames = min(3, len(action_prompts))
                for i in range(1, max_frames):  # Skip first frame, generate 2-3 key motion frames
                    if i >= len(action_prompts):
                        break
                    
                action_prompt = action_prompts[i]
                logging.info(f"Generating motion frame {i}: {action_prompt[:60]}...")
                
                try:
                    encoded_action = quote(f"{action_prompt}, high quality, detailed, cinematic, dynamic motion")
                    response = requests.get(f"{base_url}{encoded_action}", params=params, timeout=12)
                    
                    if response.status_code == 200:
                        action_image = Image.open(io.BytesIO(response.content)).convert('RGB')
                        action_images.append(action_image)
                        logging.info(f"Successfully generated motion frame {i}")
                    else:
                        logging.warning(f"Failed to generate frame {i}, using enhanced base image")
                        # Create a variation of base image with motion blur for fallback
                        enhanced_base = self._create_motion_variant(base_image, i)
                        action_images.append(enhanced_base)
                except Exception as e:
                    logging.warning(f"Error generating frame {i}: {str(e)}")
                    # Create motion variant as fallback
                    enhanced_base = self._create_motion_variant(base_image, i)
                    action_images.append(enhanced_base)
            
            logging.info(f"Generated {len(action_images)} distinct motion frames")
            
            # Step 3: Create ultra-smooth transitions with more frames for longer videos
            frames = []
            frame_count = 90  # Much longer video - 6 seconds at 15 FPS
            
            logging.info("Creating ultra-smooth motion sequence...")
            
            # Create smooth interpolation between all action images
            for frame_num in range(frame_count):
                overall_progress = frame_num / (frame_count - 1)
                
                if len(action_images) == 1:
                    # Single image - apply cinematic effects
                    frame = action_images[0].copy()
                    frame = self._apply_advanced_motion_simulation(frame, overall_progress, prompt)
                else:
                    # Multiple images - create smooth interpolation
                    # Map progress to image sequence with smooth curves
                    image_progress = overall_progress * (len(action_images) - 1)
                    current_index = int(image_progress)
                    blend_ratio = image_progress - current_index
                    
                    # Use smooth easing function for more natural motion
                    blend_ratio = self._smooth_ease_function(blend_ratio)
                    
                    current_index = min(current_index, len(action_images) - 1)
                    next_index = min(current_index + 1, len(action_images) - 1)
                    
                    if current_index == next_index:
                        frame = action_images[current_index].copy()
                    else:
                        # Advanced blending with motion compensation
                        frame = self._advanced_blend_with_motion(
                            action_images[current_index], 
                            action_images[next_index], 
                            blend_ratio,
                            overall_progress,
                            prompt
                        )
                
                # Apply motion-specific effects
                frame = self._apply_action_motion_effects(frame, overall_progress, prompt)
                
                # Apply context-specific animation effects
                overall_progress = frame_num / frame_count
                
                # Apply different animation effects based on prompt content
                if any(word in prompt.lower() for word in ['fire', 'flame', 'burning', 'dragon']):
                    frame = self._apply_fire_effect(frame, overall_progress)
                elif any(word in prompt.lower() for word in ['water', 'ocean', 'wave', 'rain', 'sea']):
                    frame = self._apply_water_effect(frame, overall_progress)
                elif any(word in prompt.lower() for word in ['wind', 'flying', 'moving', 'floating', 'car', 'running']):
                    frame = self._apply_motion_effect(frame, overall_progress)
                elif any(word in prompt.lower() for word in ['magic', 'spell', 'glow', 'energy', 'fantasy', 'warrior', 'armor', 'sword']):
                    frame = self._apply_glow_effect(frame, overall_progress)
                elif any(word in prompt.lower() for word in ['night', 'dark', 'moon', 'stars', 'city']):
                    frame = self._apply_night_effect(frame, overall_progress)
                elif any(word in prompt.lower() for word in ['portrait', 'face', 'person', 'girl', 'boy', 'man', 'woman']):
                    frame = self._apply_portrait_effect(frame, overall_progress)
                else:
                    # Default subtle animation - breathing/pulsing effect
                    frame = self._apply_breathing_effect(frame, overall_progress)
                
                frames.append(frame)
            
            # Step 3: Save as MP4 video using OpenCV
            filename = f"ai_video_{uuid.uuid4().hex[:8]}.mp4"
            filepath = os.path.join(self.videos_dir, filename)
            
            # Convert PIL images to OpenCV format and create video
            import cv2
            import numpy as np
            
            # Get frame dimensions
            height, width = frames[0].size[::-1]  # PIL uses (width, height), OpenCV uses (height, width)
            
            # Try multiple codecs for maximum compatibility
            fourcc_options = ['mp4v', 'XVID', 'MJPG']
            fps = 15.0
            out = None
            
            for codec in fourcc_options:
                try:
                    fourcc = cv2.VideoWriter_fourcc(*codec)
                    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))
                    if out.isOpened():
                        logging.info(f"Using codec: {codec}")
                        break
                    else:
                        out.release()
                        out = None
                except:
                    if out:
                        out.release()
                        out = None
                    continue
            
            if out is None:
                logging.error("Failed to initialize video writer with any codec")
                return self._create_fallback_video(prompt)
            
            # Convert frames and write to video
            frames_written = 0
            for frame in frames:
                try:
                    # Convert PIL image to OpenCV format (BGR)
                    frame_array = np.array(frame)
                    frame_bgr = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
                    out.write(frame_bgr)
                    frames_written += 1
                except Exception as e:
                    logging.error(f"Error writing frame {frames_written}: {e}")
                    break
            
            # Release video writer
            out.release()
            
            # Verify file was created and has content
            if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
                logging.error(f"Video file not created properly: {filepath}")
                return self._create_fallback_video(prompt)
            
            logging.info(f"Successfully wrote {frames_written} frames to video")
            
            # Step 4: Add engaging hooks and background music
            logging.info("Adding engaging hooks and background music...")
            hook_enhanced_filename = self._add_engaging_hooks(filepath, prompt)
            final_filename = self._add_background_music(hook_enhanced_filename, prompt)
            
            logging.info(f"AI image video with hooks and music created: {final_filename}")
            return final_filename
            
        except Exception as e:
            logging.error(f"AI image video generation failed: {str(e)}")
            return None
    
    def _blend_images(self, image1, image2, alpha):
        """Blend two images together for smooth transitions"""
        try:
            from PIL import Image as PILImage
            return PILImage.blend(image1, image2, 1.0 - alpha)
        except:
            return image1
    
    def _smooth_ease_function(self, t):
        """Apply smooth easing function for natural motion curves"""
        # Smooth hermite interpolation (ease-in-out)
        return t * t * (3.0 - 2.0 * t)
    
    def _advanced_blend_with_motion(self, image1, image2, blend_ratio, overall_progress, prompt):
        """Advanced blending with motion compensation for realistic transitions"""
        try:
            import math
            from PIL import Image as PILImage, ImageEnhance, ImageFilter
            
            # Apply motion-aware blending
            if any(word in prompt.lower() for word in ['cutting', 'swinging', 'chopping']):
                # Fast action - use sharp transition with motion blur
                if 0.3 < blend_ratio < 0.7:
                    # Add motion blur during fast movement
                    blurred1 = image1.filter(ImageFilter.BLUR)
                    blurred2 = image2.filter(ImageFilter.BLUR)
                    image1 = PILImage.blend(image1, blurred1, 0.3)
                    image2 = PILImage.blend(image2, blurred2, 0.3)
            
            elif any(word in prompt.lower() for word in ['dancing', 'flowing']):
                # Flowing motion - enhance colors during transition
                enhancer1 = ImageEnhance.Color(image1)
                enhancer2 = ImageEnhance.Color(image2)
                image1 = enhancer1.enhance(1.0 + math.sin(overall_progress * 4 * math.pi) * 0.1)
                image2 = enhancer2.enhance(1.0 + math.sin(overall_progress * 4 * math.pi) * 0.1)
            
            # Perform smooth blending
            return PILImage.blend(image1, image2, blend_ratio)
            
        except:
            return PILImage.blend(image1, image2, blend_ratio)
    
    def _apply_advanced_motion_simulation(self, image, progress, prompt):
        """Simulate realistic motion effects on single image"""
        try:
            import math
            from PIL import Image as PILImage, ImageEnhance, ImageFilter, ImageOps
            
            prompt_lower = prompt.lower()
            
            # Simulate different types of motion based on prompt
            if any(word in prompt_lower for word in ['cutting', 'swinging']):
                # Simulate pendulum motion for cutting/swinging
                swing_angle = math.sin(progress * 2 * math.pi) * 15  # 15 degree swing
                
                # Apply subtle rotation effect
                if abs(swing_angle) > 5:
                    # Add motion blur during fast swing
                    blurred = image.filter(ImageFilter.BLUR)
                    image = PILImage.blend(image, blurred, abs(swing_angle) / 30)
            
            elif any(word in prompt_lower for word in ['walking', 'running']):
                # Simulate walking rhythm with up-down motion
                vertical_offset = math.sin(progress * 6 * math.pi) * 3
                
                # Add slight motion blur for realism
                if abs(vertical_offset) > 1:
                    blurred = image.filter(ImageFilter.BLUR)
                    image = PILImage.blend(image, blurred, 0.1)
            
            elif any(word in prompt_lower for word in ['jumping']):
                # Simulate jump arc
                jump_height = -4 * (progress - 0.5) ** 2 + 1  # Parabolic arc
                
                if jump_height > 0.3:
                    # Brighten during peak of jump
                    enhancer = ImageEnhance.Brightness(image)
                    image = enhancer.enhance(1.0 + jump_height * 0.1)
            
            elif any(word in prompt_lower for word in ['dancing']):
                # Simulate flowing dance movement
                flow_x = math.sin(progress * 4 * math.pi) * 2
                flow_y = math.cos(progress * 6 * math.pi) * 1
                
                # Add color enhancement for dynamic feel
                enhancer = ImageEnhance.Color(image)
                color_boost = 1.0 + abs(flow_x) * 0.05
                image = enhancer.enhance(color_boost)
            
            # Apply subtle zoom breathing for all motions
            zoom_factor = 1.0 + math.sin(progress * 2 * math.pi) * 0.02
            width, height = image.size
            new_width = int(width * zoom_factor)
            new_height = int(height * zoom_factor)
            
            if zoom_factor != 1.0:
                resized = image.resize((new_width, new_height), PILImage.Resampling.LANCZOS)
                
                # Center crop
                left = (new_width - width) // 2
                top = (new_height - height) // 2
                
                if left >= 0 and top >= 0:
                    image = resized.crop((left, top, left + width, top + height))
            
            return image
            
        except:
            return image
    
    def _create_motion_variant(self, base_image, variant_index):
        """Create motion variants of base image for fallback"""
        try:
            from PIL import ImageEnhance, ImageFilter
            
            # Apply different transformations based on variant index
            if variant_index == 1:
                # Add motion blur and slight brightness boost
                blurred = base_image.filter(ImageFilter.BLUR)
                enhancer = ImageEnhance.Brightness(blurred)
                return enhancer.enhance(1.1)
            elif variant_index == 2:
                # Add color enhancement and sharpness
                enhancer = ImageEnhance.Color(base_image)
                enhanced = enhancer.enhance(1.2)
                sharpener = ImageEnhance.Sharpness(enhanced)
                return sharpener.enhance(1.1)
            else:
                # Add contrast enhancement
                enhancer = ImageEnhance.Contrast(base_image)
                return enhancer.enhance(1.1)
                
        except:
            return base_image.copy()
    
    def _generate_action_sequence_prompts(self, original_prompt):
        """Generate sequence of prompts for different action stages"""
        prompt_lower = original_prompt.lower()
        
        # Detect action type and create appropriate sequence (reduced for speed)
        if any(word in prompt_lower for word in ['cutting', 'cut', 'chopping', 'sawing']):
            if 'tree' in prompt_lower:
                return [
                    f"{original_prompt}, person raising axe above head ready to cut",
                    f"{original_prompt}, person swinging axe down toward tree",
                    f"{original_prompt}, axe hitting tree bark, wood chips flying"
                ]
        
        elif any(word in prompt_lower for word in ['walking', 'running', 'moving']):
            return [
                f"{original_prompt}, starting position",
                f"{original_prompt}, mid-step with one foot forward",
                f"{original_prompt}, full stride in motion",
                f"{original_prompt}, completing step"
            ]
        
        elif any(word in prompt_lower for word in ['jumping', 'leap']):
            return [
                f"{original_prompt}, crouching before jump",
                f"{original_prompt}, beginning to leap up",
                f"{original_prompt}, at highest point of jump",
                f"{original_prompt}, landing from jump"
            ]
        
        elif any(word in prompt_lower for word in ['dancing', 'dance']):
            return [
                f"{original_prompt}, beginning dance pose with arms at sides",
                f"{original_prompt}, arms raised gracefully, starting to move",
                f"{original_prompt}, spinning with dress flowing, mid-twirl motion",
                f"{original_prompt}, arms extended, one leg lifted in dance position",
                f"{original_prompt}, head tilted back, arms flowing, peak dance moment",
                f"{original_prompt}, completing spin, arms coming down gracefully"
            ]
        
        elif any(word in prompt_lower for word in ['waterfall', 'water']):
            return [
                f"{original_prompt}, approaching the water's edge",
                f"{original_prompt}, stepping into water, creating splash",
                f"{original_prompt}, hands reaching toward falling water",
                f"{original_prompt}, water droplets around her, arms raised",
                f"{original_prompt}, spinning in shallow water, creating ripples",
                f"{original_prompt}, laughing with water drops sparkling around"
            ]
            return [
                f"{original_prompt}, starting dance pose",
                f"{original_prompt}, arms extended in dance move",
                f"{original_prompt}, spinning in dance motion",
                f"{original_prompt}, finishing dance pose"
            ]
        
        elif any(word in prompt_lower for word in ['fighting', 'punching', 'boxing']):
            return [
                f"{original_prompt}, guard position ready to fight",
                f"{original_prompt}, throwing a punch",
                f"{original_prompt}, punch connecting",
                f"{original_prompt}, pulling back after hit"
            ]
        
        elif any(word in prompt_lower for word in ['eating', 'drinking']):
            return [
                f"{original_prompt}, reaching for food/drink",
                f"{original_prompt}, bringing to mouth",
                f"{original_prompt}, taking a bite/sip",
                f"{original_prompt}, finishing eating/drinking"
            ]
        
        elif any(word in prompt_lower for word in ['waving', 'wave']):
            return [
                f"{original_prompt}, hand at side",
                f"{original_prompt}, raising hand to wave",
                f"{original_prompt}, hand waving left",
                f"{original_prompt}, hand waving right"
            ]
        
        else:
            # Default action sequence for any activity
            return [
                f"{original_prompt}, beginning action",
                f"{original_prompt}, mid-action in progress",
                f"{original_prompt}, action at peak intensity",
                f"{original_prompt}, completing action"
            ]
    
    def _apply_action_motion_effects(self, image, progress, prompt):
        """Apply motion blur and effects specific to the action"""
        try:
            import math
            from PIL import ImageFilter, ImageEnhance
            
            prompt_lower = prompt.lower()
            
            # Apply action-specific motion effects
            if any(word in prompt_lower for word in ['cutting', 'chopping', 'swinging']):
                # Sharp, quick motion blur for cutting actions
                if 0.3 < progress < 0.7:  # During the swing
                    motion_intensity = math.sin((progress - 0.3) * math.pi / 0.4) * 2
                    if motion_intensity > 0.5:
                        blurred = image.filter(ImageFilter.BLUR)
                        image = self._blend_images(image, blurred, motion_intensity * 0.4)
            
            elif any(word in prompt_lower for word in ['running', 'walking']):
                # Continuous motion blur for movement
                motion_intensity = abs(math.sin(progress * 4 * math.pi)) * 1.2
                if motion_intensity > 0.3:
                    blurred = image.filter(ImageFilter.BLUR)
                    image = self._blend_images(image, blurred, motion_intensity * 0.3)
            
            elif any(word in prompt_lower for word in ['jumping', 'leap']):
                # Vertical motion effects
                if 0.2 < progress < 0.8:  # During jump
                    enhancer = ImageEnhance.Brightness(image)
                    image = enhancer.enhance(1.1)
            
            elif any(word in prompt_lower for word in ['dancing']):
                # Flowing motion with brightness variation
                flow = math.sin(progress * 6 * math.pi) * 0.1
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(1.0 + flow)
            
            elif any(word in prompt_lower for word in ['fighting', 'punching']):
                # Sharp impact effects
                if 0.4 < progress < 0.6:  # During impact
                    enhancer = ImageEnhance.Contrast(image)
                    image = enhancer.enhance(1.2)
            
            return image
            
        except:
            return image
    
    def _apply_camera_movement(self, image, progress, prompt):
        """Apply cinematic camera effects like zoom, pan, and rotate"""
        try:
            import math
            from PIL import Image as PILImage, ImageOps
            
            width, height = image.size
            
            # Determine camera movement based on prompt content
            if any(word in prompt.lower() for word in ['flying', 'soaring', 'above', 'aerial']):
                # Aerial/flying scenes - zoom out effect
                scale = 1.2 - (progress * 0.3)  # Start zoomed in, zoom out
                new_width = int(width * scale)
                new_height = int(height * scale)
                
            elif any(word in prompt.lower() for word in ['approaching', 'coming', 'close', 'near']):
                # Approaching scenes - zoom in effect
                scale = 1.0 + (progress * 0.4)  # Gradually zoom in
                new_width = int(width * scale)
                new_height = int(height * scale)
                
            elif any(word in prompt.lower() for word in ['moving', 'walking', 'running', 'traveling']):
                # Movement scenes - slight pan effect
                pan_offset = int(math.sin(progress * 2 * math.pi) * 20)
                # Create slight horizontal movement
                result = ImageOps.expand(image, border=(abs(pan_offset), 0), fill=(0, 0, 0))
                if pan_offset > 0:
                    result = result.crop((pan_offset, 0, width + pan_offset, height))
                else:
                    result = result.crop((0, 0, width, height))
                return result
                
            else:
                # Default subtle zoom breathing effect
                scale = 1.0 + math.sin(progress * 2 * math.pi) * 0.05
                new_width = int(width * scale)
                new_height = int(height * scale)
            
            # Apply scaling
            if scale != 1.0:
                resized = image.resize((new_width, new_height), PILImage.Resampling.LANCZOS)
                
                # Center crop to original size
                left = (new_width - width) // 2
                top = (new_height - height) // 2
                
                if left < 0 or top < 0:
                    # If scaling down, pad the image
                    result = PILImage.new('RGB', (width, height), (0, 0, 0))
                    paste_x = max(0, -left)
                    paste_y = max(0, -top)
                    result.paste(resized, (paste_x, paste_y))
                    return result
                else:
                    return resized.crop((left, top, left + width, top + height))
            
            return image
            
        except Exception as e:
            return image
    
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
            import math
            from PIL import ImageEnhance
            
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
            
            # Save as MP4 video using OpenCV
            filename = f"video_{uuid.uuid4().hex[:8]}.mp4"
            filepath = os.path.join(self.videos_dir, filename)
            
            # Convert frames to OpenCV format
            import cv2
            import numpy as np
            
            height, width = frames[0].size[::-1]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = 8.0
            out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))
            
            for frame in frames:
                frame_array = np.array(frame)
                frame_bgr = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
                out.write(frame_bgr)
            
            out.release()
            
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
    
    def _add_engaging_hooks(self, video_path, prompt):
        """Add compelling text overlays and hooks to make videos viral-ready"""
        try:
            import cv2
            import numpy as np
            from PIL import Image, ImageDraw, ImageFont
            
            # Generate hook text based on video content
            hook_text = self._generate_hook_text(prompt)
            
            # Load video
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Create output video with hooks
            hook_filename = video_path.replace('.mp4', '_with_hooks.mp4')
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(hook_filename, fourcc, fps, (width, height))
            
            frame_count = 0
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Add hook overlay based on timing
                enhanced_frame = self._add_hook_overlay(frame, hook_text, frame_count, total_frames, prompt)
                out.write(enhanced_frame)
                frame_count += 1
            
            cap.release()
            out.release()
            
            logging.info(f"Added engaging hooks to video: {hook_text}")
            return hook_filename
            
        except Exception as e:
            logging.error(f"Failed to add hooks: {str(e)}")
            return video_path
    
    def _generate_hook_text(self, prompt):
        """Generate compelling hook text based on video content"""
        prompt_lower = prompt.lower()
        
        # Generate attention-grabbing hooks based on content
        if any(word in prompt_lower for word in ['dancing', 'dance']):
            hooks = [
                "This dance will blow your mind! 🔥",
                "Watch this incredible move!",
                "You won't believe this dance!",
                "This is pure magic! ✨",
                "Wait for the spin!"
            ]
        elif any(word in prompt_lower for word in ['waterfall', 'nature', 'forest']):
            hooks = [
                "Nature's pure magic! 🌊",
                "This place is unreal!",
                "Paradise found! 🌿",
                "Mother Nature's masterpiece!",
                "Wait for the reveal!"
            ]
        elif any(word in prompt_lower for word in ['cat', 'kitten', 'pet']):
            hooks = [
                "This cat is too cute! 😻",
                "You need to see this!",
                "Cutest thing ever!",
                "This will make your day!",
                "Watch till the end!"
            ]
        elif any(word in prompt_lower for word in ['action', 'fighting', 'martial']):
            hooks = [
                "Incredible skills! 💪",
                "This is insane!",
                "Watch this power move!",
                "Mind-blowing technique!",
                "You won't believe this!"
            ]
        elif any(word in prompt_lower for word in ['cooking', 'chef', 'food']):
            hooks = [
                "This cooking hack is genius! 👨‍🍳",
                "You need to try this!",
                "This will change everything!",
                "Secret technique revealed!",
                "Watch this magic happen!"
            ]
        else:
            hooks = [
                "You won't believe this!",
                "This is incredible!",
                "Watch till the end!",
                "Something amazing happens!",
                "This will blow your mind!"
            ]
        
        import random
        return random.choice(hooks)
    
    def _add_hook_overlay(self, frame, hook_text, frame_num, total_frames, prompt):
        """Add hook text overlay to frame with timing and effects"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import cv2
            import numpy as np
            
            # Convert frame to PIL Image
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            draw = ImageDraw.Draw(pil_image)
            
            # Get frame dimensions
            width, height = pil_image.size
            
            # Show hook text during first 2 seconds (30 frames at 15 fps)
            if frame_num < 30:
                # Calculate text position and size
                font_size = max(32, width // 25)
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                # Get text dimensions
                bbox = draw.textbbox((0, 0), hook_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # Position text at top center
                x = (width - text_width) // 2
                y = height // 10
                
                # Add background rectangle for better readability
                padding = 20
                rect_coords = [
                    x - padding, y - padding,
                    x + text_width + padding, y + text_height + padding
                ]
                
                # Animate background opacity
                alpha = int(255 * (1 - frame_num / 30))  # Fade out over time
                
                # Create semi-transparent background
                overlay = Image.new('RGBA', pil_image.size, (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)
                overlay_draw.rectangle(rect_coords, fill=(0, 0, 0, min(180, alpha)))
                
                # Combine overlay with image
                pil_image = Image.alpha_composite(pil_image.convert('RGBA'), overlay).convert('RGB')
                draw = ImageDraw.Draw(pil_image)
                
                # Add text with color based on content
                text_color = self._get_hook_text_color(prompt)
                draw.text((x, y), hook_text, font=font, fill=text_color)
            
            # Add call-to-action in final frames
            elif frame_num > total_frames - 20:  # Last 20 frames
                cta_text = "👍 Like & Follow for more!"
                font_size = max(24, width // 35)
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                bbox = draw.textbbox((0, 0), cta_text, font=font)
                text_width = bbox[2] - bbox[0]
                
                # Position at bottom center
                x = (width - text_width) // 2
                y = height - height // 8
                
                # Add semi-transparent background
                padding = 15
                overlay = Image.new('RGBA', pil_image.size, (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)
                overlay_draw.rectangle([
                    x - padding, y - padding,
                    x + text_width + padding, y + font_size + padding
                ], fill=(0, 0, 0, 150))
                
                pil_image = Image.alpha_composite(pil_image.convert('RGBA'), overlay).convert('RGB')
                draw = ImageDraw.Draw(pil_image)
                draw.text((x, y), cta_text, font=font, fill=(255, 255, 255))
            
            # Convert back to OpenCV format
            frame_array = np.array(pil_image)
            return cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
            
        except Exception as e:
            logging.error(f"Error adding hook overlay: {str(e)}")
            return frame
    
    def _get_hook_text_color(self, prompt):
        """Get appropriate text color based on content mood"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['dancing', 'party', 'celebration']):
            return (255, 100, 150)  # Pink/magenta for energetic content
        elif any(word in prompt_lower for word in ['nature', 'waterfall', 'peaceful']):
            return (100, 255, 150)  # Green for nature content
        elif any(word in prompt_lower for word in ['action', 'fighting', 'power']):
            return (255, 150, 100)  # Orange/red for action content
        elif any(word in prompt_lower for word in ['cute', 'cat', 'adorable']):
            return (255, 200, 100)  # Yellow for cute content
        else:
            return (255, 255, 255)  # White for general content

    def _add_background_music(self, video_path, prompt):
        """Add appropriate background music to the video"""
        try:
            import numpy as np
            from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
            import math
            
            # Generate background music based on prompt mood
            music_filename = self._generate_background_music(prompt)
            
            if music_filename:
                # Load video and audio
                video = VideoFileClip(video_path)
                audio = AudioFileClip(os.path.join(self.videos_dir, music_filename))
                
                # Adjust audio length to match video
                if audio.duration > video.duration:
                    audio = audio.subclip(0, video.duration)
                else:
                    # Loop audio if it's shorter than video
                    loops_needed = math.ceil(video.duration / audio.duration)
                    audio_list = [audio] * loops_needed
                    audio = CompositeAudioClip(audio_list).subclip(0, video.duration)
                
                # Set volume to 30% for background music
                audio = audio.volumex(0.3)
                
                # Combine video with audio
                final_video = video.set_audio(audio)
                
                # Save new video with music
                music_video_filename = video_path.replace('.mp4', '_with_music.mp4')
                final_video.write_videofile(music_video_filename, codec='libx264', audio_codec='aac', verbose=False, logger=None)
                
                # Clean up
                video.close()
                audio.close()
                final_video.close()
                
                return os.path.basename(music_video_filename)
            
            return os.path.basename(video_path)
            
        except Exception as e:
            logging.error(f"Failed to add background music: {str(e)}")
            return os.path.basename(video_path)
    
    def _generate_background_music(self, prompt):
        """Generate background music based on prompt mood"""
        try:
            import numpy as np
            from scipy.io.wavfile import write
            
            # Analyze prompt for mood
            prompt_lower = prompt.lower()
            
            # Determine music style based on content
            if any(word in prompt_lower for word in ['dancing', 'party', 'celebration', 'joyful']):
                return self._create_upbeat_music()
            elif any(word in prompt_lower for word in ['peaceful', 'calm', 'meditation', 'waterfall', 'nature']):
                return self._create_peaceful_music()
            elif any(word in prompt_lower for word in ['action', 'fighting', 'adventure', 'cutting']):
                return self._create_dramatic_music()
            else:
                return self._create_gentle_music()
                
        except Exception as e:
            logging.error(f"Music generation failed: {str(e)}")
            return None
    
    def _create_upbeat_music(self):
        """Create upbeat dance music"""
        try:
            import numpy as np
            from scipy.io.wavfile import write
            
            duration = 8  # seconds
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Create upbeat rhythm with multiple harmonics
            frequency = 120  # BPM converted to Hz
            music = np.sin(2 * np.pi * frequency * t) * 0.3
            music += np.sin(2 * np.pi * frequency * 2 * t) * 0.2
            music += np.sin(2 * np.pi * frequency * 3 * t) * 0.1
            
            # Add drum-like beat
            beat = np.sin(2 * np.pi * 2 * t) * 0.4
            music += beat
            
            # Apply envelope for natural sound
            envelope = np.exp(-t * 0.1)
            music *= envelope
            
            filename = "upbeat_music.wav"
            filepath = os.path.join(self.videos_dir, filename)
            write(filepath, sample_rate, (music * 32767).astype(np.int16))
            
            return filename
            
        except Exception as e:
            logging.error(f"Upbeat music creation failed: {str(e)}")
            return None
    
    def _create_peaceful_music(self):
        """Create peaceful ambient music"""
        try:
            import numpy as np
            from scipy.io.wavfile import write
            
            duration = 8
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Create peaceful tones
            music = np.sin(2 * np.pi * 60 * t) * 0.3  # Low frequency
            music += np.sin(2 * np.pi * 90 * t) * 0.2  # Harmonic
            music += np.sin(2 * np.pi * 45 * t) * 0.1  # Sub-harmonic
            
            # Add gentle waves effect
            waves = np.sin(2 * np.pi * 0.5 * t) * 0.1
            music += waves
            
            filename = "peaceful_music.wav"
            filepath = os.path.join(self.videos_dir, filename)
            write(filepath, sample_rate, (music * 32767).astype(np.int16))
            
            return filename
            
        except Exception as e:
            logging.error(f"Peaceful music creation failed: {str(e)}")
            return None
    
    def _create_dramatic_music(self):
        """Create dramatic action music"""
        try:
            import numpy as np
            from scipy.io.wavfile import write
            
            duration = 8
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Create dramatic rising tones
            music = np.sin(2 * np.pi * 80 * t) * 0.4
            music += np.sin(2 * np.pi * 120 * t) * 0.3
            music += np.sin(2 * np.pi * 160 * t) * 0.2
            
            # Add intensity build-up
            intensity = t / duration  # Gradually increase
            music *= intensity
            
            filename = "dramatic_music.wav"
            filepath = os.path.join(self.videos_dir, filename)
            write(filepath, sample_rate, (music * 32767).astype(np.int16))
            
            return filename
            
        except Exception as e:
            logging.error(f"Dramatic music creation failed: {str(e)}")
            return None
    
    def _create_gentle_music(self):
        """Create gentle background music"""
        try:
            import numpy as np
            from scipy.io.wavfile import write
            
            duration = 8
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Create gentle melody
            music = np.sin(2 * np.pi * 70 * t) * 0.3
            music += np.sin(2 * np.pi * 105 * t) * 0.2
            music += np.sin(2 * np.pi * 140 * t) * 0.1
            
            filename = "gentle_music.wav"
            filepath = os.path.join(self.videos_dir, filename)
            write(filepath, sample_rate, (music * 32767).astype(np.int16))
            
            return filename
            
        except Exception as e:
            logging.error(f"Gentle music creation failed: {str(e)}")
            return None

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