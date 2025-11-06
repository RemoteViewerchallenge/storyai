# UI Elements and Interactions Specification

## Character Selection Interface

### Radio Button Groups
**Perspective Selection**
- **Element Type**: Radio button group
- **Options**: "1st Person", "3rd Person"
- **Default**: None selected
- **Interaction**: Single selection, updates character context
- **Visual State**: Selected option highlighted with primary color

**Gender Selection**
- **Element Type**: Radio button group with premium indicators
- **Options**: "Male", "Female", "Alien 👑"
- **Default**: None selected
- **Interaction**: Single selection, triggers sub-options for Male/Female
- **Premium Indicator**: Crown icon for Alien option
- **Visual State**: 
  - Available options: Full color, clickable
  - Premium options: Gold accent, crown icon
  - Disabled state: Grayed out with tooltip "Premium Feature"

**Character Variant Selection** (Conditional)
- **Element Type**: Radio button group (appears after gender selection)
- **Male Options**: "Male 1", "Male 2"
- **Female Options**: "Female 1", "Female 2"
- **Interaction**: Single selection, updates avatar preview
- **Visual State**: Smooth transition when appearing/disappearing

**Career Selection**
- **Element Type**: Radio button group
- **Options**: "Corporate CEO", "Hip Hop Artist", "Unemployed"
- **Default**: None selected
- **Interaction**: Single selection, influences story generation
- **Visual State**: Icons accompany each option for visual clarity

### Avatar Preview Component
**Dynamic Image Display**
- **Element Type**: Image container with loading states
- **Size**: 200x200px (desktop), 150x150px (mobile)
- **Default State**: Placeholder silhouette
- **Loading State**: Animated spinner overlay
- **Error State**: Fallback generic avatar
- **Interaction**: Updates automatically when selections change
- **Animation**: Smooth fade transition between avatar changes

### Image Generation Style Selection
**Style Radio Buttons**
- **Element Type**: Radio button group with visual previews
- **Options**: 
  - "Anime" (Free) - with small preview image
  - "Fantasy 👑" (Premium) - with preview and crown
  - "Realistic 👑" (Premium) - with preview and crown
- **Default**: "Anime" (free option)
- **Interaction**: 
  - Free users: Can select Anime only
  - Premium users: Can select any option
  - Clicking premium options shows upgrade prompt for free users
- **Visual State**: 
  - Available: Full color with preview image
  - Premium: Gold border and crown icon
  - Selected: Primary color border and checkmark

## Story Presentation Interface

### Image Canvas
**Main Display Area**
- **Element Type**: Responsive image container
- **Size**: 60% of viewport height, full width
- **Aspect Ratio**: 16:9 maintained
- **Loading State**: Skeleton placeholder with animation
- **Error State**: Fallback illustration with retry button
- **Interaction**: 
  - Click to view fullscreen (optional)
  - Pinch to zoom on mobile
- **Animation**: Smooth fade-in when new image loads

### Text Display Area
**Story Narration**
- **Element Type**: Scrollable text container
- **Typography**: 
  - Font: Inter, 16px (mobile), 18px (desktop)
  - Line height: 1.6
  - Color: #ffffff
- **Content Types**:
  - Narrative text (regular style)
  - Character dialogue (italic, different color)
  - User prompt questions (bold, highlighted)
- **Interaction**: Auto-scroll to new content
- **Animation**: Typewriter effect for new text (optional)

### User Input Field
**Text Response Area**
- **Element Type**: Expandable textarea
- **Placeholder**: "What do you do next?"
- **Size**: Auto-expanding, max 4 lines
- **Validation**: Character limit indicator
- **Interaction**:
  - Enter key submits (with Shift+Enter for new line)
  - Auto-focus after story segment completes
- **Visual State**: 
  - Default: Subtle border
  - Focus: Primary color border
  - Error: Red border with message

### Control Panel
**Audio Controls**
- **Mute Toggle**
  - Element: Toggle switch
  - States: On/Off with icon change
  - Interaction: Immediate audio mute/unmute
  
- **Sound Effects Toggle**
  - Element: Toggle switch
  - States: On/Off with icon change
  - Interaction: Enable/disable background sounds

**Voice Input Button**
- **Element Type**: Large circular button with microphone icon
- **Size**: 60px diameter
- **States**:
  - Default: Primary color background
  - Recording: Pulsing red animation
  - Processing: Loading spinner
- **Interaction**: 
  - Press and hold to record
  - Release to process
  - Voice-to-text conversion
- **Accessibility**: Voice feedback for recording state

**Phone Access Button**
- **Element Type**: Icon button
- **Size**: 44px minimum touch target
- **Icon**: Phone symbol
- **Interaction**: Opens phone overlay modal
- **Visual State**: Subtle hover effect

**End Story Button**
- **Element Type**: Secondary button
- **Style**: Outlined button with warning color
- **Interaction**: Confirmation dialog before ending
- **Position**: Bottom of control panel

### Phone Overlay Modal
**Modal Container**
- **Element Type**: Full-screen overlay with phone mockup
- **Background**: Dimmed story image (40% opacity)
- **Phone Mockup**: 
  - Size: 320x568px (iPhone-like proportions)
  - Background: Dark theme to match story aesthetic
  - Border: Subtle device frame

**Date/Time Display**
- **Element Type**: Static text
- **Content**: Current story date/time context
- **Style**: System font, white text

**Contact List**
- **Element Type**: Scrollable list
- **Items**: Contact name with phone icon
- **Interaction**: 
  - Tap to "call" (triggers story event)
  - Smooth list scrolling
- **Visual State**: Hover/touch feedback

**Close Button**
- **Element Type**: Icon button (X)
- **Position**: Top-right of phone mockup
- **Interaction**: Closes modal, returns to story
- **Accessibility**: ESC key also closes modal

## Premium Feature Indicators

### Crown Icon System
- **Usage**: Consistent crown icon (👑) for all premium features
- **Color**: Gold (#ffc107)
- **Size**: 16px next to feature names
- **Animation**: Subtle sparkle effect on hover

### Upgrade Prompts
**Modal Overlay**
- **Trigger**: Clicking premium features as free user
- **Content**: 
  - Feature benefits list
  - Pricing information
  - Upgrade button (primary CTA)
  - "Maybe later" option (secondary)
- **Style**: Centered modal with backdrop blur
- **Animation**: Smooth scale-in transition

### Feature Comparison
**Visual Differentiation**
- **Free Features**: Full color, fully interactive
- **Premium Features**: Gold accent, crown icon
- **Disabled Premium**: Grayed out, tooltip on hover
- **Upgrade Hints**: Subtle "Upgrade" text below premium options

## Responsive Behavior

### Mobile Adaptations
- **Touch Targets**: Minimum 44px for all interactive elements
- **Gesture Support**: Swipe navigation where appropriate
- **Keyboard Handling**: Proper focus management and virtual keyboard accommodation
- **Orientation**: Portrait-optimized with landscape support

### Tablet Adaptations
- **Layout**: Hybrid between mobile and desktop
- **Touch and Mouse**: Support for both input methods
- **Screen Real Estate**: Utilize additional space for larger previews

### Desktop Enhancements
- **Hover States**: Subtle color changes and elevation
- **Keyboard Shortcuts**: Space for voice input, Enter for text submission
- **Mouse Interactions**: Precise clicking and selection

This specification ensures consistent, accessible, and engaging user interactions throughout the application.



## Interactive Storytelling Loop

### Story Presentation Flow
The story presentation follows a continuous interactive loop:

1. **AI Content Generation**
   - Story segment generated by Mixtral 8x7B
   - Image generated by Stable Diffusion
   - Audio narration generated by ElevenLabs

2. **Content Presentation**
   - Image displays in main canvas
   - Text appears in story area
   - TTS begins narration with:
     - Narrator voice for story text
     - Individual character voices for dialogue
     - Appropriate pacing and emphasis

3. **User Input Phase**
   - After narration completes, input field becomes active
   - User can respond via:
     - Text input (typing response)
     - Voice input (microphone button)
     - Phone interaction (accessing in-story phone)
   - Input field shows prompt: "What do you do next?"

4. **Process Repetition**
   - User input sent to backend for next story segment
   - Character traits and story context maintained
   - Loop returns to step 1 with new content

### Audio Control During Loop
- **Auto-play**: Narration starts automatically when new content loads
- **User Control**: Mute/unmute affects all audio
- **Voice Switching**: Seamless transition between narrator and character voices
- **Pause/Resume**: Users can pause narration and resume later
- **Skip Option**: Advanced users can skip to input phase

### Input State Management
- **Disabled During Narration**: Input field disabled while TTS is speaking
- **Auto-focus**: Input field automatically focused after narration ends
- **Loading States**: Show processing indicator while generating next segment
- **Error Handling**: Graceful fallback if generation fails

### Visual Feedback
- **Speaking Indicator**: Visual cue showing when TTS is active
- **Character Highlighting**: Subtle highlight when character is speaking
- **Progress Indication**: Show story progression/length
- **Waiting States**: Clear indication when system is processing user input

