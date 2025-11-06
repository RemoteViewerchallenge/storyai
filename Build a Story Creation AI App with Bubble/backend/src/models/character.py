from src.db import db
from datetime import datetime
import json

class Character(db.Model):
    __tablename__ = 'characters'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)  # For Bubble.io user identification
    name = db.Column(db.String(100), nullable=True)
    perspective = db.Column(db.String(20), nullable=False)  # '1st_person' or '3rd_person'
    gender = db.Column(db.String(20), nullable=False)  # 'male', 'female', 'alien'
    variant = db.Column(db.String(20), nullable=True)  # 'male_1', 'male_2', 'female_1', 'female_2'
    career = db.Column(db.String(50), nullable=False)  # 'ceo', 'hip_hop_artist', 'unemployed'
    image_style = db.Column(db.String(20), nullable=False)  # 'anime', 'fantasy', 'realistic'
    avatar_url = db.Column(db.String(500), nullable=True)  # URL to generated avatar
    traits = db.Column(db.Text, nullable=True)  # JSON string of character traits
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'perspective': self.perspective,
            'gender': self.gender,
            'variant': self.variant,
            'career': self.career,
            'image_style': self.image_style,
            'avatar_url': self.avatar_url,
            'traits': json.loads(self.traits) if self.traits else {},
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def get_traits_dict(self):
        """Return traits as dictionary"""
        return json.loads(self.traits) if self.traits else {}
    
    def set_traits_dict(self, traits_dict):
        """Set traits from dictionary"""
        self.traits = json.dumps(traits_dict)
    
    def get_character_description(self):
        """Generate character description for AI prompts"""
        gender_desc = {
            'male': 'man',
            'female': 'woman', 
            'alien': 'alien being'
        }.get(self.gender, 'person')
        
        career_desc = {
            'ceo': 'corporate CEO',
            'hip_hop_artist': 'hip hop artist',
            'unemployed': 'unemployed person'
        }.get(self.career, 'person')
        
        perspective = 'first person' if self.perspective == '1st_person' else 'third person'
        
        return f"A {gender_desc} who is a {career_desc}. Story told in {perspective}."


class Story(db.Model):
    __tablename__ = 'stories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    partner_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)  # For premium users
    title = db.Column(db.String(200), nullable=True)
    current_segment = db.Column(db.Integer, default=0)
    story_context = db.Column(db.Text, nullable=True)  # JSON string of story history
    current_image_url = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'paused'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    character = db.relationship('Character', foreign_keys=[character_id], backref='main_stories')
    partner = db.relationship('Character', foreign_keys=[partner_id], backref='partner_stories')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'character_id': self.character_id,
            'partner_id': self.partner_id,
            'title': self.title,
            'current_segment': self.current_segment,
            'story_context': json.loads(self.story_context) if self.story_context else [],
            'current_image_url': self.current_image_url,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def get_context_list(self):
        """Return story context as list"""
        return json.loads(self.story_context) if self.story_context else []
    
    def set_context_list(self, context_list):
        """Set story context from list"""
        self.story_context = json.dumps(context_list)
    
    def add_story_segment(self, segment_data):
        """Add a new story segment to context"""
        context = self.get_context_list()
        context.append(segment_data)
        self.set_context_list(context)
        self.current_segment += 1


class StorySegment(db.Model):
    __tablename__ = 'story_segments'
    
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    segment_number = db.Column(db.Integer, nullable=False)
    narrative_text = db.Column(db.Text, nullable=False)
    user_input = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    audio_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    story = db.relationship('Story', backref='segments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'story_id': self.story_id,
            'segment_number': self.segment_number,
            'narrative_text': self.narrative_text,
            'user_input': self.user_input,
            'image_url': self.image_url,
            'audio_url': self.audio_url,
            'created_at': self.created_at.isoformat()
        }

