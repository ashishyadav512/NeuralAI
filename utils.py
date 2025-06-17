import re
import uuid
import os
from datetime import datetime

def validate_prompt(prompt):
    """
    Validate and enhance user prompt for better AI generation
    """
    if not prompt or len(prompt.strip()) < 3:
        return "A beautiful cinematic scene"
    
    # Clean up prompt
    cleaned = re.sub(r'[^\w\s\-\.,!?]', '', prompt.strip())
    
    # Enhance prompt for better video generation
    enhancements = [
        "cinematic",
        "high quality",
        "detailed",
        "professional lighting"
    ]
    
    # Add enhancements if not already present
    enhanced = cleaned
    for enhancement in enhancements:
        if enhancement not in enhanced.lower():
            enhanced += f", {enhancement}"
    
    return enhanced

def generate_filename(prefix, extension):
    """
    Generate unique filename with timestamp and UUID
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}_{timestamp}_{unique_id}.{extension}"

def ensure_directory(path):
    """
    Ensure directory exists, create if not
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    return True

def format_file_size(size_bytes):
    """
    Format file size in human readable format
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def get_video_duration(filepath):
    """
    Get video duration in seconds
    """
    try:
        import cv2
        cap = cv2.VideoCapture(filepath)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps
        cap.release()
        return duration
    except:
        return 0