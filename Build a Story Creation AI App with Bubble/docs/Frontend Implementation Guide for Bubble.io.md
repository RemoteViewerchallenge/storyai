# Frontend Implementation Guide for Bubble.io

This guide provides detailed instructions for implementing the Story AI frontend in Bubble.io based on the React prototype.

## Overview

The React prototype demonstrates all the required functionality for your Story AI application:
- Welcome page with terms agreement
- Character creation with conditional logic and premium features
- Story presentation with interactive storytelling
- Subscription tier management and feature gating

## Page Structure

### 1. Welcome Page (`index`)

**Elements to Create:**
- Header with "Story AI" title and subtitle
- Three feature cards (Interactive Stories, Dynamic Characters, Voice Narration)
- Terms and Conditions section with scrollable text
- Checkbox for terms agreement
- Continue button (disabled until terms accepted)

**Workflows:**
- When checkbox is checked → Enable continue button
- When continue button is clicked → Navigate to character creation page

**Styling:**
- Use purple gradient background (#8B5CF6 to #A855F7)
- White cards with subtle shadows
- Responsive grid layout for feature cards

### 2. Character Creation Page (`character-creation`)

**Elements to Create:**
- Back button to welcome page
- Character Preview section (right sidebar)
- Story Perspective radio buttons (1st Person, 3rd Person)
- Character Type radio buttons (Male, Female, Alien)
- Character Variant section (conditional - appears when Male/Female selected)
- Career dropdown (Corporate CEO, Hip Hop Artist, Unemployed)
- Image Style radio buttons (Anime, Fantasy, Realistic)
- Create Character button
- Premium upgrade notice

**Conditional Logic:**
- Show Character Variant section only when Male or Female is selected
- Show Male 1/Male 2 options when Male is selected
- Show Female 1/Female 2 options when Female is selected
- Mark Alien, Fantasy, and Realistic as "Premium" for free users
- Disable premium options for free tier users
- Update Character Summary in real-time as selections are made
- Enable Create Character button only when all required fields are filled

**Workflows:**
- When character type changes → Show/hide variant options
- When any selection changes → Update character preview
- When Create Character clicked → Navigate to story presentation page

### 3. Story Presentation Page (`story-presentation`)

**Elements to Create:**
- Header with back button, title, and end story button
- Large image canvas (800x600px) for AI-generated images
- Story text area (scrollable, read-only)
- User input field for story prompts
- Control buttons: Microphone, Phone, Continue Story
- Phone modal overlay (hidden by default)
- Story progress indicator
- Subscription status display

**Phone Modal Elements:**
- Current time and date display
- Contact list with predefined contacts
- Close button

**Workflows:**
- When user enters text and clicks Continue → Simulate story generation
- When microphone clicked → Show voice input notification
- When phone clicked → Show/hide phone modal
- When contact in phone clicked → Show call simulation
- When end story clicked → Confirm and return to character creation

**API Integration Points:**
- Character creation → POST to `/api/characters`
- Story continuation → POST to `/api/stories/{story_id}/continue`
- Image generation → GET from `/api/stories/{story_id}/image`
- Audio generation → GET from `/api/stories/{story_id}/audio`

## Database Structure in Bubble.io

### User Data Type
- email (text)
- subscription_tier (text: "free" or "premium")
- stories_this_month (number)
- created_date (date)

### Character Data Type
- user (User)
- perspective (text: "1st_person" or "3rd_person")
- gender (text: "male", "female", "alien")
- variant (text: "male_1", "male_2", "female_1", "female_2")
- career (text: "corporate_ceo", "hip_hop_artist", "unemployed")
- image_style (text: "anime", "fantasy", "realistic")
- traits (text - JSON string)
- created_date (date)

### Story Data Type
- user (User)
- character (Character)
- title (text)
- current_segment (number)
- status (text: "active", "completed", "paused")
- created_date (date)

### Story Segment Data Type
- story (Story)
- segment_number (number)
- narrative_text (text)
- user_input (text)
- image_url (text)
- audio_url (text)
- created_date (date)

## Subscription Logic

### Free Tier Limitations
- Maximum 5 stories per month
- Only Anime image style available
- Only Male and Female character types
- No Fantasy or Realistic image styles
- No Alien character type

### Premium Features
- Unlimited stories
- All image styles (Anime, Fantasy, Realistic)
- All character types including Alien
- Advanced voice features
- Priority story generation

## Styling Guidelines

### Color Palette
- Primary: #8B5CF6 (Purple)
- Secondary: #A855F7 (Light Purple)
- Background: #F8FAFC (Light Gray)
- Text: #1F2937 (Dark Gray)
- Cards: #FFFFFF (White)
- Borders: #E5E7EB (Light Gray)

### Typography
- Headers: Bold, 24-32px
- Body text: Regular, 16px
- Buttons: Medium, 16px
- Captions: Regular, 14px

### Responsive Design
- Mobile-first approach
- Breakpoints: 768px (tablet), 1024px (desktop)
- Stack elements vertically on mobile
- Use grid layouts for larger screens

## Backend Integration

The React prototype is designed to work with the backend API you already have. Key integration points:

1. **Authentication**: Implement user login/signup flows
2. **Character Management**: Save character configurations to database
3. **Story Generation**: Call AI services for narrative and image generation
4. **Subscription Management**: Check user tier and enforce limitations
5. **Usage Tracking**: Monitor story creation limits for free users

## Testing Checklist

- [ ] Welcome page loads and terms agreement works
- [ ] Character creation shows/hides options correctly
- [ ] Premium features are properly gated for free users
- [ ] Story presentation displays narrative text
- [ ] User input and story continuation works
- [ ] Phone modal opens and closes correctly
- [ ] Navigation between pages works smoothly
- [ ] Responsive design works on mobile and desktop
- [ ] Subscription status displays correctly
- [ ] Usage limits are enforced for free tier

## Deployment Notes

1. Set up your Bubble.io app with the three main pages
2. Configure the database structure as outlined above
3. Implement the workflows and conditional logic
4. Style the elements according to the design guidelines
5. Test all functionality thoroughly
6. Connect to your backend API for production features

The React prototype serves as a complete reference implementation. You can run it locally to see exactly how each feature should behave and look.

