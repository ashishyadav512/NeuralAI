from app import db
from datetime import datetime

class GeneratedImage(db.Model):
    """Model for storing generated images"""
    __tablename__ = 'generated_images'
    
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_favorite = db.Column(db.Boolean, default=False)
    generation_time = db.Column(db.Integer, default=0)  # in seconds
    
    def __repr__(self):
        return f'<GeneratedImage {self.id}: {self.prompt[:50]}...>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'prompt': self.prompt,
            'image_filename': self.image_filename,
            'created_at': self.created_at.isoformat(),
            'is_favorite': self.is_favorite,
            'generation_time': self.generation_time
        }
