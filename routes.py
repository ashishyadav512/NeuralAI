from flask import render_template, request, jsonify, send_file, flash, redirect, url_for
from app import app, db
from models import VideoGeneration
import os
import logging
from datetime import datetime
from image_generator import generate_image
from video_generator import create_video_from_images
from utils import validate_prompt, generate_filename

@app.route('/')
def index():
    recent_videos = VideoGeneration.query.order_by(VideoGeneration.created_at.desc()).limit(6).all()
    return render_template('index.html', recent_videos=recent_videos)

@app.route('/generate', methods=['POST'])
def generate_video():
    try:
        prompt = request.form.get('prompt', '').strip()
        
        if not prompt:
            flash('Please enter a prompt for video generation.', 'error')
            return redirect(url_for('index'))
        
        # Validate and enhance prompt
        enhanced_prompt = validate_prompt(prompt)
        
        # Create database record
        video_gen = VideoGeneration(
            prompt=enhanced_prompt,
            status='generating'
        )
        db.session.add(video_gen)
        db.session.commit()
        
        # Generate images for video frames
        logging.info(f"Generating images for prompt: {enhanced_prompt}")
        images = generate_image(enhanced_prompt, num_frames=10)
        
        if not images:
            video_gen.status = 'failed'
            db.session.commit()
            flash('Failed to generate images. Please try again.', 'error')
            return redirect(url_for('index'))
        
        # Create video from images
        video_filename = generate_filename('video', 'mp4')
        video_path = os.path.join('static', 'videos', video_filename)
        
        # Ensure videos directory exists
        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        
        logging.info(f"Creating video: {video_path}")
        success = create_video_from_images(images, video_path, enhanced_prompt)
        
        if success:
            video_gen.video_filename = video_filename
            video_gen.status = 'completed'
            video_gen.completed_at = datetime.utcnow()
            db.session.commit()
            
            flash('Video generated successfully!', 'success')
        else:
            video_gen.status = 'failed'
            db.session.commit()
            flash('Failed to create video. Please try again.', 'error')
        
        return redirect(url_for('index'))
        
    except Exception as e:
        logging.error(f"Error generating video: {str(e)}")
        flash('An error occurred while generating the video.', 'error')
        return redirect(url_for('index'))

@app.route('/video/<filename>')
def serve_video(filename):
    video_path = os.path.join('static', 'videos', filename)
    if os.path.exists(video_path):
        return send_file(video_path)
    else:
        return "Video not found", 404

@app.route('/api/status/<int:video_id>')
def get_status(video_id):
    video_gen = VideoGeneration.query.get_or_404(video_id)
    return jsonify({
        'id': video_gen.id,
        'status': video_gen.status,
        'prompt': video_gen.prompt,
        'video_filename': video_gen.video_filename,
        'created_at': video_gen.created_at.isoformat() if video_gen.created_at else None
    })