# Application Architecture Outline

## 1. Overview
This document outlines the proposed architecture for the web-based "Create Your Own Story AI App." The application will leverage Bubble.io for the frontend, Supabase for character data persistence, and Hugging Face/ElevenLabs for AI-driven story generation, image generation, and voice narration. Backend AI services will be hosted on AWS EC2.

## 2. Components

### 2.1. Frontend (Bubble.io)
*   **Purpose:** User interface and user experience for story creation, character selection, and story presentation.
*   **Key Features:**
    *   Welcome Page: Terms agreement, login/signup.
    *   Story Creation Page (Free Tier): Character selection (1st/3rd person, gender, career), image generation preferences (Anime, Fantasy - subscriber, Realistic - subscriber).
    *   Story Presentation Page: AI-generated image canvas, narration text box, player prompt input, mute/sound effects controls, microphone button (TTS input), phone icon (in-story access), end story button.
    *   Subscription Management: Display of subscriber-only features.
*   **Interaction:** Communicates with Supabase via Bubble.io's API connector/plugins and with custom backend AI services via API calls.

### 2.2. Database (Supabase)
*   **Purpose:** Store character traits for continuity, user data, subscription information, and potentially story progress.
*   **Key Features:**
    *   Character Profiles: Store selected traits (gender, career, etc.) and generated avatars.
    *   User Management: Authentication and authorization (though Bubble.io might handle primary user auth).
    *   Subscription Tiers: Manage free vs. paid user access to features.
*   **Interaction:** Accessed by Bubble.io directly via its API connector or Supabase plugins. Backend AI services might also interact with Supabase for reading/writing character data.

### 2.3. Backend AI Services (AWS EC2)
*   **Purpose:** Host and manage the AI models for story generation, image generation, and voice narration. Provides custom API endpoints for Bubble.io to consume.
*   **Key Technologies:**
    *   **Mixtral 8x7B (Hugging Face):** For high-quality, coherent narrative generation. Will receive character traits from Supabase (via the backend service) and append them to prompts to maintain continuity.
    *   **Stable Diffusion (Hugging Face):** For image generation (static for initial setup/locations, dynamic for story progression). Will generate images based on story context and character appearance.
    *   **ElevenLabs:** For quality narrator voice and individualized voices for generated characters. Will convert narration text and character dialogue into audio.
*   **Hosting:** AWS EC2 instances, potentially with GPU instances for AI model inference.
*   **Interaction:** Exposes RESTful APIs for Bubble.io to call. Interacts with Hugging Face and ElevenLabs APIs. May interact with Supabase for character data.

## 3. Data Flow and API Interactions

1.  **User Interaction (Bubble.io):** User selects character traits and preferences on the story creation page.
2.  **Character Data Storage (Bubble.io -> Supabase):** Selected character traits are saved to the Supabase database.
3.  **Story Generation Request (Bubble.io -> AWS EC2 Backend):** When the user initiates story creation, Bubble.io sends a request to the custom backend API on AWS EC2.
4.  **Backend Processing (AWS EC2 Backend):**
    *   Retrieves character traits from Supabase.
    *   Constructs prompts for Mixtral 8x7B, incorporating character continuity.
    *   Calls Mixtral 8x7B (Hugging Face API) for narrative generation.
    *   Calls Stable Diffusion (Hugging Face API) for image generation based on narrative and character appearance.
    *   Calls ElevenLabs API for voice narration and character voices.
    *   Stores generated story segments, images, and audio references (or actual audio files) back into Supabase or a dedicated storage service (e.g., AWS S3).
5.  **Story Presentation (AWS EC2 Backend -> Bubble.io):** The backend sends the generated story content (text, image URLs, audio URLs) back to Bubble.io.
6.  **Display and Playback (Bubble.io):** Bubble.io displays the image, text, and plays the audio. User input (text or TTS) is captured and sent back to the backend for the next story segment generation.
7.  **TTS Input (Bubble.io -> AWS EC2 Backend):** User's voice input (from microphone) is sent to the backend, converted to text, and used to influence the next story segment.

## 4. Hosting Considerations
*   **Bubble.io:** Hosted by Bubble.io.
*   **Supabase:** Cloud-hosted by Supabase.
*   **Backend AI Services:** Hosted on AWS EC2 instances, potentially utilizing services like AWS S3 for storing generated media assets to optimize delivery to Bubble.io.

## 5. Security and Scalability
*   **API Keys:** Securely manage API keys for Hugging Face and ElevenLabs on the AWS EC2 backend.
*   **Authentication:** Bubble.io will handle user authentication for the frontend. Supabase will manage database access control.
*   **Scalability:** AWS EC2 instances can be scaled up or out based on demand for AI inference. Supabase offers scalable database solutions. Bubble.io handles its own scaling.

This architecture provides a clear separation of concerns, allowing each component to be developed, managed, and scaled independently.

