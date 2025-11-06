# Story AI Backend API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, the API uses user_id strings for identification. In production, implement proper authentication with JWT tokens or similar.

## Endpoints

### Health Check
**GET** `/health`

Check the health status of the API and connected services.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-06-27T10:43:00.000Z",
  "services": {
    "database": "connected",
    "huggingface": "configured",
    "elevenlabs": "configured"
  }
}
```

### API Status
**GET** `/status`

Get API status and available endpoints.

**Response:**
```json
{
  "status": "running",
  "message": "Story AI Backend API",
  "version": "1.0.0",
  "endpoints": {
    "characters": "/api/characters",
    "stories": "/api/stories",
    "health": "/api/health"
  }
}
```

---

## Character Management

### Create Character
**POST** `/characters`

Create a new character with AI-generated avatar.

**Request Body:**
```json
{
  "user_id": "bubble_user_123",
  "name": "Alex Adventure",
  "perspective": "1st_person",
  "gender": "male",
  "variant": "male_1",
  "career": "ceo",
  "image_style": "anime"
}
```

**Required Fields:**
- `user_id`: String - Unique identifier for the user
- `perspective`: String - "1st_person" or "3rd_person"
- `gender`: String - "male", "female", or "alien"
- `career`: String - "ceo", "hip_hop_artist", or "unemployed"
- `image_style`: String - "anime", "fantasy", or "realistic"

**Optional Fields:**
- `name`: String - Character name
- `variant`: String - "male_1", "male_2", "female_1", "female_2"

**Response:**
```json
{
  "id": 1,
  "user_id": "bubble_user_123",
  "name": "Alex Adventure",
  "perspective": "1st_person",
  "gender": "male",
  "variant": "male_1",
  "career": "ceo",
  "image_style": "anime",
  "avatar_url": "/static/avatars/avatar_1.png",
  "traits": {
    "personality": ["ambitious", "decisive", "strategic", "confident"],
    "background": "A successful male executive with years of corporate experience.",
    "goals": ["expand business empire", "maintain work-life balance", "mentor others"]
  },
  "created_at": "2025-06-27T10:43:00.000Z",
  "updated_at": "2025-06-27T10:43:00.000Z"
}
```

### Get Character
**GET** `/characters/{character_id}`

Retrieve a specific character by ID.

**Response:**
```json
{
  "id": 1,
  "user_id": "bubble_user_123",
  "name": "Alex Adventure",
  "perspective": "1st_person",
  "gender": "male",
  "variant": "male_1",
  "career": "ceo",
  "image_style": "anime",
  "avatar_url": "/static/avatars/avatar_1.png",
  "traits": {
    "personality": ["ambitious", "decisive", "strategic", "confident"],
    "background": "A successful male executive with years of corporate experience.",
    "goals": ["expand business empire", "maintain work-life balance", "mentor others"]
  },
  "created_at": "2025-06-27T10:43:00.000Z",
  "updated_at": "2025-06-27T10:43:00.000Z"
}
```

---

## Story Management

### Create Story
**POST** `/stories`

Create a new story with initial AI-generated content.

**Request Body:**
```json
{
  "user_id": "bubble_user_123",
  "character_id": 1,
  "partner_id": null,
  "title": "My Epic Adventure"
}
```

**Required Fields:**
- `user_id`: String - Unique identifier for the user
- `character_id`: Integer - ID of the main character

**Optional Fields:**
- `partner_id`: Integer - ID of partner character (premium feature)
- `title`: String - Story title

**Response:**
```json
{
  "story": {
    "id": 1,
    "user_id": "bubble_user_123",
    "character_id": 1,
    "partner_id": null,
    "title": "My Epic Adventure",
    "current_segment": 1,
    "story_context": [],
    "current_image_url": "/static/story_images/story_1_segment_1.png",
    "status": "active",
    "created_at": "2025-06-27T10:43:00.000Z",
    "updated_at": "2025-06-27T10:43:00.000Z"
  },
  "initial_segment": {
    "id": 1,
    "story_id": 1,
    "segment_number": 1,
    "narrative_text": "Your adventure begins in a bustling city...",
    "user_input": "Begin an exciting adventure story.",
    "image_url": "/static/story_images/story_1_segment_1.png",
    "audio_url": "/static/story_audio/story_1_segment_1.mp3",
    "created_at": "2025-06-27T10:43:00.000Z"
  }
}
```

### Continue Story
**POST** `/stories/{story_id}/continue`

Continue a story with user input, generating the next segment.

**Request Body:**
```json
{
  "user_input": "I decide to explore the mysterious alley."
}
```

**Required Fields:**
- `user_input`: String - User's choice or action

**Response:**
```json
{
  "id": 2,
  "story_id": 1,
  "segment_number": 2,
  "narrative_text": "You cautiously enter the dimly lit alley...",
  "user_input": "I decide to explore the mysterious alley.",
  "image_url": "/static/story_images/story_1_segment_2.png",
  "audio_url": "/static/story_audio/story_1_segment_2.mp3",
  "created_at": "2025-06-27T10:43:00.000Z"
}
```

### Get Story
**GET** `/stories/{story_id}`

Retrieve a complete story with all segments.

**Response:**
```json
{
  "story": {
    "id": 1,
    "user_id": "bubble_user_123",
    "character_id": 1,
    "partner_id": null,
    "title": "My Epic Adventure",
    "current_segment": 2,
    "story_context": [],
    "current_image_url": "/static/story_images/story_1_segment_2.png",
    "status": "active",
    "created_at": "2025-06-27T10:43:00.000Z",
    "updated_at": "2025-06-27T10:43:00.000Z"
  },
  "segments": [
    {
      "id": 1,
      "story_id": 1,
      "segment_number": 1,
      "narrative_text": "Your adventure begins in a bustling city...",
      "user_input": "Begin an exciting adventure story.",
      "image_url": "/static/story_images/story_1_segment_1.png",
      "audio_url": "/static/story_audio/story_1_segment_1.mp3",
      "created_at": "2025-06-27T10:43:00.000Z"
    },
    {
      "id": 2,
      "story_id": 1,
      "segment_number": 2,
      "narrative_text": "You cautiously enter the dimly lit alley...",
      "user_input": "I decide to explore the mysterious alley.",
      "image_url": "/static/story_images/story_1_segment_2.png",
      "audio_url": "/static/story_audio/story_1_segment_2.mp3",
      "created_at": "2025-06-27T10:43:00.000Z"
    }
  ]
}
```

### Get User Stories
**GET** `/stories/user/{user_id}`

Retrieve all stories for a specific user.

**Response:**
```json
[
  {
    "id": 1,
    "user_id": "bubble_user_123",
    "character_id": 1,
    "partner_id": null,
    "title": "My Epic Adventure",
    "current_segment": 2,
    "story_context": [],
    "current_image_url": "/static/story_images/story_1_segment_2.png",
    "status": "active",
    "created_at": "2025-06-27T10:43:00.000Z",
    "updated_at": "2025-06-27T10:43:00.000Z"
  }
]
```

---

## Voice Features

### Voice to Text
**POST** `/voice-to-text`

Convert voice input to text (placeholder for future implementation).

**Request Body:**
```json
{
  "audio_data": "base64_encoded_audio"
}
```

**Response:**
```json
{
  "text": "Voice to text conversion not yet implemented",
  "confidence": 0.0
}
```

---

## Error Responses

All endpoints may return the following error responses:

**400 Bad Request:**
```json
{
  "error": "Missing required field: user_id"
}
```

**404 Not Found:**
```json
{
  "error": "Character not found"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal server error message"
}
```

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
SECRET_KEY=your_secret_key_here
```

---

## Integration with Bubble.io

### CORS Configuration
The API is configured to accept requests from any origin (`*`). In production, restrict this to your Bubble.io app domain.

### User Identification
Use Bubble.io's user unique ID as the `user_id` parameter in API calls.

### File Serving
Generated images and audio files are served from the `/static/` directory. Access them via:
- Images: `http://your-api-domain.com/static/avatars/avatar_1.png`
- Audio: `http://your-api-domain.com/static/story_audio/story_1_segment_1.mp3`

### Workflow Integration
1. **Character Creation**: Call `/api/characters` when user completes character selection
2. **Story Start**: Call `/api/stories` when user starts a new story
3. **Story Continuation**: Call `/api/stories/{id}/continue` when user provides input
4. **Story Retrieval**: Call `/api/stories/{id}` to load existing stories

---

## Testing

Use the following curl commands to test the API:

```bash
# Health check
curl http://localhost:5000/api/health

# Create character
curl -X POST http://localhost:5000/api/characters \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "perspective": "1st_person",
    "gender": "male",
    "career": "ceo",
    "image_style": "anime"
  }'

# Create story
curl -X POST http://localhost:5000/api/stories \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "character_id": 1,
    "title": "Test Story"
  }'
```

