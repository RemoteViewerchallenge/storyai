from flask import Blueprint, jsonify, request, send_file
from flask_cors import cross_origin
from src.db import db
from src.models.character import Character, Story, StorySegment
from src.services.ai_services import AIServiceManager
import os
import base64
import tempfile
import asyncio
from datetime import datetime

story_bp = Blueprint('story', __name__)
ai_manager = AIServiceManager()

@story_bp.route('/characters', methods=['POST'])
@cross_origin()
def create_character():
    """Create a new character"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['user_id', 'perspective', 'gender', 'career', 'image_style']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create character
        character = Character(
            user_id=data['user_id'],
            name=data.get('name'),
            perspective=data['perspective'],
            gender=data['gender'],
            variant=data.get('variant'),
            career=data['career'],
            image_style=data['image_style']
        )
        
        # Set initial traits
        traits = {
            'personality': _generate_personality(data['career']),
            'background': _generate_background(data['career'], data['gender']),
            'goals': _generate_goals(data['career'])
        }
        character.set_traits_dict(traits)
        
        db.session.add(character)
        db.session.commit()
        
        # Generate avatar image
        avatar_prompt = _create_avatar_prompt(character)
        image_data = asyncio.run(ai_manager.comfyui_service.generate_image(avatar_prompt, character.image_style))
        
        if image_data:
            # Save avatar image (in production, use cloud storage)
            avatar_filename = f"avatar_{character.id}.png"
            avatar_path = os.path.join('src', 'static', 'avatars', avatar_filename)
            os.makedirs(os.path.dirname(avatar_path), exist_ok=True)
            
            with open(avatar_path, 'wb') as f:
                f.write(image_data)
            
            character.avatar_url = f"/static/avatars/{avatar_filename}"
            db.session.commit()
        
        return jsonify(character.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@story_bp.route('/characters/<int:character_id>', methods=['GET'])
@cross_origin()
def get_character(character_id):
    """Get character by ID"""
    character = Character.query.get_or_404(character_id)
    return jsonify(character.to_dict())

@story_bp.route('/stories', methods=['POST'])
@cross_origin()
def create_story():
    """Create a new story"""
    try:
        data = request.json
        
        # Validate required fields
        if 'user_id' not in data or 'character_id' not in data:
            return jsonify({'error': 'Missing required fields: user_id, character_id'}), 400
        
        # Verify character exists
        character = Character.query.get(data['character_id'])
        if not character:
            return jsonify({'error': 'Character not found'}), 404
        
        # Create story
        story = Story(
            user_id=data['user_id'],
            character_id=data['character_id'],
            partner_id=data.get('partner_id'),
            title=data.get('title', 'Untitled Story')
        )
        
        db.session.add(story)
        db.session.commit()
        
        # Generate initial story segment
        initial_prompt = "Begin an exciting adventure story."
        character_data = {
            'description': character.get_character_description(),
            'image_style': character.image_style,
            'traits': character.get_traits_dict()
        }
        
        segment_data = asyncio.run(ai_manager.generate_story_segment(initial_prompt, character_data))
        
        # Save initial segment
        segment = StorySegment(
            story_id=story.id,
            segment_number=1,
            narrative_text=segment_data['narrative_text'],
            user_input=initial_prompt
        )
        
        # Save image if generated
        if segment_data['image_data']:
            image_filename = f"story_{story.id}_segment_1.png"
            image_path = os.path.join('src', 'static', 'story_images', image_filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            with open(image_path, 'wb') as f:
                f.write(segment_data['image_data'])
            
            segment.image_url = f"/static/story_images/{image_filename}"
            story.current_image_url = segment.image_url
        
        # Save audio if generated
        if segment_data['audio_data']:
            audio_filename = f"story_{story.id}_segment_1.mp3"
            audio_path = os.path.join('src', 'static', 'story_audio', audio_filename)
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            
            with open(audio_path, 'wb') as f:
                f.write(segment_data['audio_data'])
            
            segment.audio_url = f"/static/story_audio/{audio_filename}"
        
        db.session.add(segment)
        story.current_segment = 1
        db.session.commit()
        
        return jsonify({
            'story': story.to_dict(),
            'initial_segment': segment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@story_bp.route('/stories/<int:story_id>/continue', methods=['POST'])
@cross_origin()
def continue_story(story_id):
    """Continue a story with user input"""
    try:
        data = request.json
        user_input = data.get('user_input', '')
        
        if not user_input:
            return jsonify({'error': 'User input is required'}), 400
        
        # Get story and character
        story = Story.query.get_or_404(story_id)
        character = Character.query.get(story.character_id)
        
        # Get story history
        previous_segments = StorySegment.query.filter_by(story_id=story_id).order_by(StorySegment.segment_number).all()
        story_history = [seg.narrative_text for seg in previous_segments[-3:]]  # Last 3 segments
        
        # Generate next segment
        character_data = {
            'description': character.get_character_description(),
            'image_style': character.image_style,
            'traits': character.get_traits_dict()
        }
        
        segment_data = asyncio.run(ai_manager.generate_story_segment(user_input, character_data, story_history))
        
        # Create new segment
        new_segment_number = story.current_segment + 1
        segment = StorySegment(
            story_id=story.id,
            segment_number=new_segment_number,
            narrative_text=segment_data['narrative_text'],
            user_input=user_input
        )
        
        # Save image if generated
        if segment_data['image_data']:
            image_filename = f"story_{story.id}_segment_{new_segment_number}.png"
            image_path = os.path.join('src', 'static', 'story_images', image_filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            with open(image_path, 'wb') as f:
                f.write(segment_data['image_data'])
            
            segment.image_url = f"/static/story_images/{image_filename}"
            story.current_image_url = segment.image_url
        
        # Save audio if generated
        if segment_data['audio_data']:
            audio_filename = f"story_{story.id}_segment_{new_segment_number}.mp3"
            audio_path = os.path.join('src', 'static', 'story_audio', audio_filename)
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            
            with open(audio_path, 'wb') as f:
                f.write(segment_data['audio_data'])
            
            segment.audio_url = f"/static/story_audio/{audio_filename}"
        
        db.session.add(segment)
        story.current_segment = new_segment_number
        story.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(segment.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@story_bp.route('/stories/<int:story_id>', methods=['GET'])
@cross_origin()
def get_story(story_id):
    """Get story with all segments"""
    story = Story.query.get_or_404(story_id)
    segments = StorySegment.query.filter_by(story_id=story_id).order_by(StorySegment.segment_number).all()
    
    return jsonify({
        'story': story.to_dict(),
        'segments': [segment.to_dict() for segment in segments]
    })

@story_bp.route('/stories/user/<user_id>', methods=['GET'])
@cross_origin()
def get_user_stories(user_id):
    """Get all stories for a user"""
    stories = Story.query.filter_by(user_id=user_id).order_by(Story.updated_at.desc()).all()
    return jsonify([story.to_dict() for story in stories])

@story_bp.route('/voice-to-text', methods=['POST'])
@cross_origin()
def voice_to_text():
    """Convert voice input to text (placeholder for future implementation)"""
    # This would integrate with a speech-to-text service
    # For now, return a placeholder response
    return jsonify({
        'text': 'Voice to text conversion not yet implemented',
        'confidence': 0.0
    })

@story_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'services': {
            'database': 'connected',
            'huggingface': 'configured' if os.getenv('HUGGINGFACE_API_KEY') else 'not_configured',
            'elevenlabs': 'configured' if os.getenv('ELEVENLABS_API_KEY') else 'not_configured'
        }
    })

# Helper functions
def _generate_personality(career):
    """Generate personality traits based on career"""
    personality_map = {
        'ceo': ['ambitious', 'decisive', 'strategic', 'confident'],
        'hip_hop_artist': ['creative', 'expressive', 'passionate', 'street-smart'],
        'unemployed': ['resourceful', 'adaptable', 'searching', 'resilient']
    }
    return personality_map.get(career, ['curious', 'adventurous'])

def _generate_background(career, gender):
    """Generate background story based on career and gender"""
    backgrounds = {
        'ceo': f"A successful {gender} executive with years of corporate experience.",
        'hip_hop_artist': f"An up-and-coming {gender} artist trying to make it in the music industry.",
        'unemployed': f"A {gender} between jobs, looking for new opportunities and adventures."
    }
    return backgrounds.get(career, f"A {gender} ready for adventure.")

def _generate_goals(career):
    """Generate character goals based on career"""
    goals_map = {
        'ceo': ['expand business empire', 'maintain work-life balance', 'mentor others'],
        'hip_hop_artist': ['get record deal', 'write hit songs', 'build fanbase'],
        'unemployed': ['find meaningful work', 'discover new skills', 'make connections']
    }
    return goals_map.get(career, ['explore the world', 'help others'])

def _create_avatar_prompt(character):
    """Create image prompt for character avatar"""
    gender_desc = {
        'male': 'man',
        'female': 'woman',
        'alien': 'alien being'
    }.get(character.gender, 'person')
    
    career_desc = {
        'ceo': 'in business attire, professional',
        'hip_hop_artist': 'in casual street wear, artistic',
        'unemployed': 'in casual clothes, approachable'
    }.get(character.career, 'casual')
    
    return f"Portrait of a {gender_desc} {career_desc}, character avatar, clear background"

