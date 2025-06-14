import os
import logging
from flask import render_template, request, redirect, url_for, flash, jsonify, send_file
from app import app, db
from models import GeneratedImage
from utils import generate_image_real, validate_prompt
from datetime import datetime

@app.route('/')
def index():
    """Main page with image generation interface"""
    recent_images = GeneratedImage.query.order_by(GeneratedImage.created_at.desc()).limit(4).all()
    return render_template('index.html', recent_images=recent_images)

@app.route('/generate', methods=['POST'])
def generate_image():
    """Handle image generation requests"""
    try:
        prompt = request.form.get('prompt', '').strip()
        
        # Validate prompt
        if not validate_prompt(prompt):
            flash('Please enter a valid prompt (3-500 characters)', 'error')
            return redirect(url_for('index'))
        
        # Generate image using real AI models
        start_time = datetime.now()
        image_filename = generate_image_real(prompt)
        end_time = datetime.now()
        generation_time = int((end_time - start_time).total_seconds())
        
        # Save to database
        new_image = GeneratedImage(
            prompt=prompt,
            image_filename=image_filename,
            generation_time=generation_time
        )
        db.session.add(new_image)
        db.session.commit()
        
        flash(f'Image generated successfully in {generation_time} seconds!', 'success')
        return redirect(url_for('gallery'))
        
    except Exception as e:
        logging.error(f'Error generating image: {str(e)}')
        flash('An error occurred while generating the image. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/gallery')
def gallery():
    """Display gallery of generated images"""
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Images per page
    
    images = GeneratedImage.query.order_by(GeneratedImage.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('gallery.html', images=images)

@app.route('/download/<int:image_id>')
def download_image(image_id):
    """Download generated image"""
    try:
        image = GeneratedImage.query.get_or_404(image_id)
        image_path = os.path.join('static', 'images', image.image_filename)
        
        if os.path.exists(image_path):
            # Get the file extension to determine the correct MIME type
            file_extension = os.path.splitext(image.image_filename)[1].lower()
            download_name = f'generated_image_{image.id}{file_extension}'
            
            return send_file(image_path, as_attachment=True, 
                           download_name=download_name)
        else:
            flash('Image file not found', 'error')
            return redirect(url_for('gallery'))
            
    except Exception as e:
        logging.error(f'Error downloading image: {str(e)}')
        flash('An error occurred while downloading the image', 'error')
        return redirect(url_for('gallery'))

@app.route('/toggle_favorite/<int:image_id>', methods=['POST'])
def toggle_favorite(image_id):
    """Toggle favorite status of an image"""
    try:
        image = GeneratedImage.query.get_or_404(image_id)
        image.is_favorite = not image.is_favorite
        db.session.commit()
        
        return jsonify({
            'success': True,
            'is_favorite': image.is_favorite
        })
        
    except Exception as e:
        logging.error(f'Error toggling favorite: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})

@app.route('/delete/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    """Delete a generated image"""
    try:
        image = GeneratedImage.query.get_or_404(image_id)
        
        # Delete file if it exists
        image_path = os.path.join('static', 'images', image.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        
        # Delete from database
        db.session.delete(image)
        db.session.commit()
        
        flash('Image deleted successfully', 'success')
        return redirect(url_for('gallery'))
        
    except Exception as e:
        logging.error(f'Error deleting image: {str(e)}')
        flash('An error occurred while deleting the image', 'error')
        return redirect(url_for('gallery'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html'), 500
