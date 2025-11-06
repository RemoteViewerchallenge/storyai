import requests
import os
import base64
import json
from typing import Dict, List, Optional
from dotenv import load_dotenv
from src.services.comfyui_client import generate_image as comfyui_generate_image

load_dotenv()

class HuggingFaceService:
    """Service for interacting with Hugging Face API"""
    
    def __init__(self):
        self.api_key = os.getenv('HUGGINGFACE_API_KEY')
        self.base_url = "https://api-inference.huggingface.co/models"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_story(self, prompt: str, character_context: str, story_history: List[str] = None) -> str:
        """
        Generate story content using Mixtral 8x7B model
        """
        model_url = f"{self.base_url}/mistralai/Mixtral-8x7B-Instruct-v0.1"
        
        # Build the full prompt with character context and history
        full_prompt = self._build_story_prompt(prompt, character_context, story_history)
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": 300,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(model_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '').strip()
            else:
                return result.get('generated_text', '').strip()
                
        except requests.exceptions.RequestException as e:
            print(f"Error generating story: {e}")
            return "I apologize, but I'm having trouble generating the story right now. Please try again."
    
    def generate_image(self, prompt: str, style: str = "anime") -> Optional[bytes]:
        """
        Generate image using Stable Diffusion model
        """
        # Choose model based on style
        model_map = {
            "anime": "runwayml/stable-diffusion-v1-5",
            "fantasy": "stabilityai/stable-diffusion-2-1",
            "realistic": "stabilityai/stable-diffusion-xl-base-1.0"
        }
        
        model_name = model_map.get(style, "runwayml/stable-diffusion-v1-5")
        model_url = f"{self.base_url}/{model_name}"
        
        # Enhance prompt based on style
        enhanced_prompt = self._enhance_image_prompt(prompt, style)
        
        payload = {
            "inputs": enhanced_prompt,
            "parameters": {
                "num_inference_steps": 20,
                "guidance_scale": 7.5,
                "width": 512,
                "height": 512
            }
        }
        
        try:
            response = requests.post(model_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            return response.content
            
        except requests.exceptions.RequestException as e:
            print(f"Error generating image: {e}")
            return None
    
    def _build_story_prompt(self, user_input: str, character_context: str, story_history: List[str] = None) -> str:
        """Build a comprehensive prompt for story generation"""
        
        prompt_parts = [
            "You are a creative storyteller creating an interactive narrative.",
            f"Character: {character_context}",
            "",
            "Story Guidelines:",
            "- Write engaging, descriptive narrative",
            "- Include dialogue when appropriate",
            "- End with a situation that allows user choice",
            "- Keep responses between 100-200 words",
            "- Maintain character consistency",
            ""
        ]
        
        if story_history:
            prompt_parts.extend([
                "Previous story context:",
                *story_history[-3:],  # Include last 3 segments for context
                ""
            ])
        
        prompt_parts.extend([
            f"User action/choice: {user_input}",
            "",
            "Continue the story:"
        ])
        
        return "\n".join(prompt_parts)
    
    def _enhance_image_prompt(self, prompt: str, style: str) -> str:
        """Enhance image prompt based on selected style"""
        
        style_enhancements = {
            "anime": "anime style, manga art, vibrant colors, detailed illustration",
            "fantasy": "fantasy art, magical atmosphere, detailed fantasy illustration, epic scene",
            "realistic": "photorealistic, high quality, detailed, professional photography"
        }
        
        enhancement = style_enhancements.get(style, "")
        return f"{prompt}, {enhancement}"


class ElevenLabsService:
    """Service for interacting with ElevenLabs API"""
    
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
    
    def text_to_speech(self, text: str, voice_type: str = "narrator") -> Optional[bytes]:
        """
        Convert text to speech using ElevenLabs
        """
        # Voice mapping for different character types
        voice_map = {
            "narrator": "21m00Tcm4TlvDq8ikWAM",  # Rachel - calm, clear narrator
            "male_character": "29vD33N1CtxCmqQRPOHJ",  # Drew - friendly male
            "female_character": "21m00Tcm4TlvDq8ikWAM",  # Rachel - female character
            "alien_character": "pNInz6obpgDQGcFmaJgB"  # Adam - unique for alien
        }
        
        voice_id = voice_map.get(voice_type, voice_map["narrator"])
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            return response.content
            
        except requests.exceptions.RequestException as e:
            print(f"Error generating speech: {e}")
            return None
    
    def get_available_voices(self) -> List[Dict]:
        """Get list of available voices"""
        url = f"{self.base_url}/voices"
        headers = {"xi-api-key": self.api_key}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json().get('voices', [])
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching voices: {e}")
            return []

class ComfyUIService:
    """Service for interacting with ComfyUI MCP Server"""

    async def generate_image(self, prompt: str, style: str = "anime") -> Optional[bytes]:
        """
        Generate image using ComfyUI
        """
        try:
            # These values would ideally be configurable
            width = 512
            height = 512
            workflow_id = "basic_api_test"
            model = "sd_xl_base_1.0.safetensors"

            response = await comfyui_generate_image(prompt, width, height, workflow_id, model)

            if response and "image_url" in response:
                image_url = response["image_url"]
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                return image_response.content
            else:
                return None
        except Exception as e:
            print(f"Error generating image with ComfyUI: {e}")
            return None

class AIServiceManager:
    """Manager class for coordinating AI services"""
    
    def __init__(self):
        self.hf_service = HuggingFaceService()
        self.elevenlabs_service = ElevenLabsService()
        self.comfyui_service = ComfyUIService()
    
    async def generate_story_segment(self, user_input: str, character_data: Dict, story_history: List[str] = None) -> Dict:
        """
        Generate a complete story segment with text, image, and audio
        """
        # Generate story text
        character_context = character_data.get('description', '')
        story_text = self.hf_service.generate_story(user_input, character_context, story_history)
        
        # Generate image based on story content
        image_prompt = self._extract_scene_description(story_text, character_data)
        image_style = character_data.get('image_style', 'anime')
        image_data = await self.comfyui_service.generate_image(image_prompt, image_style)
        
        # Generate audio narration
        audio_data = self.elevenlabs_service.text_to_speech(story_text, "narrator")
        
        return {
            'narrative_text': story_text,
            'image_data': image_data,
            'audio_data': audio_data,
            'image_prompt': image_prompt
        }
    
    def _extract_scene_description(self, story_text: str, character_data: Dict) -> str:
        """Extract visual scene description from story text"""
        # Simple scene extraction - in production, this could be more sophisticated
        character_desc = character_data.get('description', '')
        
        # Create a basic scene prompt
        scene_prompt = f"Scene showing {character_desc} in the story context"
        
        # Add story-specific elements (this is simplified)
        if "forest" in story_text.lower():
            scene_prompt += ", in a forest setting"
        elif "city" in story_text.lower():
            scene_prompt += ", in an urban environment"
        elif "house" in story_text.lower() or "home" in story_text.lower():
            scene_prompt += ", in a domestic setting"
        
        return scene_prompt
