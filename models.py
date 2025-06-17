from app import db
from datetime import datetime

class VideoGeneration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    video_filename = db.Column(db.String(200))
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<VideoGeneration {self.id}: {self.prompt[:50]}>'