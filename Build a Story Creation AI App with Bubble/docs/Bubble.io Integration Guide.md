# Bubble.io Integration Guide

This guide provides step-by-step instructions for integrating the Story AI Backend with your Bubble.io frontend application.

## Prerequisites

- Deployed Story AI Backend (see DEPLOYMENT_GUIDE.md)
- Active Bubble.io account with app creation privileges
- Basic familiarity with Bubble.io's visual editor

## Step 1: API Connector Setup

1. **Add API Connector Plugin**
   - Go to your Bubble.io app's Plugins tab
   - Install the "API Connector" plugin if not already installed

2. **Create New API**
   - Open the API Connector
   - Click "Add another API"
   - Name it "Story AI Backend"
   - Set the API root URL to your backend URL (e.g., `https://your-domain.com/api`)

3. **Configure Authentication**
   - Authentication type: None (for current version)
   - Add shared headers if needed:
     - Content-Type: application/json

## Step 2: Define API Calls

### Character Creation Call
```
Name: Create Character
Use as: Action
Method: POST
URL: /characters
Body type: JSON
Body:
{
  "user_id": "<user_id>",
  "perspective": "<perspective>",
  "gender": "<gender>",
  "career": "<career>",
  "image_style": "<image_style>",
  "variant": "<variant>"
}
```

### Story Creation Call
```
Name: Create Story
Use as: Action
Method: POST
URL: /stories
Body type: JSON
Body:
{
  "user_id": "<user_id>",
  "character_id": <character_id>,
  "title": "<title>"
}
```

### Story Continuation Call
```
Name: Continue Story
Use as: Action
Method: POST
URL: /stories/<story_id>/continue
Body type: JSON
Body:
{
  "user_input": "<user_input>"
}
```

### Subscription Check Call
```
Name: Check Subscription
Use as: Data
Method: GET
URL: /subscription/<user_id>
```

## Step 3: Create Data Types

### Character Data Type
- id (number)
- user_id (text)
- name (text)
- perspective (text)
- gender (text)
- career (text)
- image_style (text)
- avatar_url (text)
- traits (text)
- created_at (date)

### Story Data Type
- id (number)
- user_id (text)
- character_id (number)
- title (text)
- current_segment (number)
- status (text)
- current_image_url (text)
- created_at (date)

### Story Segment Data Type
- id (number)
- story_id (number)
- segment_number (number)
- narrative_text (text)
- user_input (text)
- image_url (text)
- audio_url (text)
- created_at (date)

## Step 4: Build User Interface

### Welcome Page
1. Create a new page called "Welcome"
2. Add terms and conditions text
3. Add checkbox for agreement
4. Add "Continue" button that navigates to character creation
5. Workflow: Only enable button when checkbox is checked

### Character Creation Page
1. Create page elements:
   - Radio buttons for perspective (1st person/3rd person)
   - Radio buttons for gender (Male/Female/Alien - with Alien crossed out for free users)
   - Conditional radio buttons for variants
   - Dropdown for career
   - Radio buttons for image style (with premium styles marked)
   - Image element for avatar preview
   - "Next" button

2. Create workflows:
   - On gender selection: Show appropriate variant options
   - On any selection: Update avatar preview
   - On "Next" click: Call "Create Character" API

### Story Presentation Page
1. Create page elements:
   - Large image element for story visuals
   - Text area for narrative display
   - Input field for user responses
   - Audio element for narration
   - Control buttons (mute, sound effects, microphone, phone, end story)
   - Phone modal overlay

2. Create workflows:
   - On page load: Display initial story segment
   - On user input submit: Call "Continue Story" API
   - On API response: Update image, text, and audio
   - Audio auto-play when new segment loads

## Step 5: Implement Subscription Logic

### Free Tier Restrictions
1. Create workflows that check subscription status before:
   - Allowing alien character selection
   - Enabling premium image styles
   - Creating partner characters

2. Display upgrade prompts for restricted features:
   - Show "Premium Only" overlays
   - Add "Upgrade Now" buttons
   - Link to subscription upgrade flow

### Usage Tracking
1. Call subscription check API before story creation
2. Display usage limits to free users
3. Block actions when limits are reached
4. Show upgrade prompts when limits are approached

## Step 6: Audio Integration

### Audio Playback
1. Use HTML element with audio tag:
```html
<audio controls autoplay>
  <source src="[Story Segment's audio_url]" type="audio/mpeg">
</audio>
```

2. Create workflows:
   - Auto-play when new segment loads
   - Respect mute settings
   - Handle audio loading errors

### Voice Input (Premium Feature)
1. Add HTML element for speech recognition:
```html
<button id="voice-btn">🎤 Speak</button>
<script>
// Web Speech API implementation
</script>
```

2. Create workflows to handle voice input results

## Step 7: Phone Feature Implementation

### Phone Modal
1. Create popup element with:
   - Current date/time display
   - Contact list
   - Call interface
   - Close button

2. Style to look like phone interface
3. Create workflows for contact interactions

## Step 8: Testing and Deployment

### Testing Checklist
- [ ] Character creation works with all options
- [ ] Story initialization displays correctly
- [ ] Story continuation generates new content
- [ ] Audio playback functions properly
- [ ] Subscription restrictions work correctly
- [ ] Premium features are properly gated
- [ ] Phone interface displays and functions
- [ ] Error handling works for API failures

### Deployment
1. Test thoroughly in Bubble.io development environment
2. Deploy to Bubble.io live environment
3. Update API URLs to point to production backend
4. Test all functionality in live environment

## Troubleshooting

### Common Issues
1. **CORS Errors**: Ensure backend has CORS enabled for your Bubble.io domain
2. **API Call Failures**: Check API URLs and parameter formatting
3. **Data Type Mismatches**: Verify data types match API responses exactly
4. **Audio Not Playing**: Check audio URL accessibility and browser permissions

### Debug Steps
1. Use Bubble.io debugger to inspect API calls
2. Check browser console for JavaScript errors
3. Verify backend logs for API request issues
4. Test API calls directly using tools like Postman

## Best Practices

1. **Error Handling**: Always handle API call failures gracefully
2. **Loading States**: Show loading indicators during API calls
3. **User Feedback**: Provide clear feedback for all user actions
4. **Performance**: Cache API responses where appropriate
5. **Security**: Never expose API keys in client-side code

## Support

For additional support:
1. Check the main API documentation
2. Review backend logs for error details
3. Test API endpoints directly to isolate issues
4. Contact support with specific error messages and steps to reproduce

