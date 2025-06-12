from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

class GeneratedImage(db.Model):
    """Model for storing generated images"""
    __tablename__ = 'generated_images'
    
    id = Column(Integer, primary_key=True)
    prompt = Column(Text, nullable=False)
    image_filename = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_favorite = Column(Boolean, default=False)
    generation_time = Column(Integer, default=0)  # in seconds
    
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
