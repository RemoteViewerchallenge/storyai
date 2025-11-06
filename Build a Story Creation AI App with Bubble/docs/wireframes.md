# Wireframes: AI Story Creation App

## Page 1: Welcome Page

### Layout Structure
```
+----------------------------------+
|            HEADER                |
| [Logo] "StoryForge AI"    [Login]|
+----------------------------------+
|                                  |
|         HERO SECTION             |
|    [Animated Story Illustration] |
|                                  |
|     "Create Your Own Story"      |
|    "AI-Powered Interactive       |
|     Storytelling Experience"     |
|                                  |
|    [Get Started - Free] [Sign In]|
+----------------------------------+
|                                  |
|       FEATURES PREVIEW           |
|  [Icon] Character    [Icon] AI   |
|  Creation           Generation   |
|                                  |
|  [Icon] Voice       [Icon] Image |
|  Narration         Generation    |
+----------------------------------+
|                                  |
|      TERMS AGREEMENT             |
|  □ I agree to the Terms of       |
|    Service and Privacy Policy    |
|                                  |
|    [Continue] (disabled until    |
|     terms accepted)              |
+----------------------------------+
|            FOOTER                |
|   About | Support | Privacy      |
+----------------------------------+
```

### Key Elements
- **Header**: Simple navigation with logo and login
- **Hero Section**: Engaging visual with clear value proposition
- **Features Preview**: Four key features with icons
- **Terms Agreement**: Required checkbox before proceeding
- **Call-to-Action**: Prominent "Get Started" button

## Page 2: Story Creation Page (Free Tier)

### Layout Structure
```
+----------------------------------+
|            HEADER                |
| [Back] Story Creation    [Help]  |
+----------------------------------+
|                                  |
|       PROGRESS INDICATOR         |
|    ●━━━━━━━○━━━━━━━○             |
|  Character  Partner   Story      |
|                                  |
+----------------------------------+
|                                  |
|      CHARACTER SELECTION         |
|                                  |
|  Perspective:                    |
|  ○ 1st Person  ○ 3rd Person     |
|                                  |
|  Gender:                         |
|  ○ Male  ○ Female  ○ Alien 👑    |
|                                  |
|  [If Male selected]              |
|  ○ Male 1  ○ Male 2              |
|                                  |
|  [If Female selected]            |
|  ○ Female 1  ○ Female 2          |
|                                  |
|  Career:                         |
|  ○ Corporate CEO                 |
|  ○ Hip Hop Artist                |
|  ○ Unemployed                    |
|                                  |
+----------------------------------+
|                                  |
|      AVATAR PREVIEW              |
|    [Character Avatar Image]      |
|                                  |
+----------------------------------+
|                                  |
|    IMAGE GENERATION STYLE        |
|                                  |
|  ○ Anime                         |
|  ○ Fantasy 👑                    |
|  ○ Realistic 👑                  |
|                                  |
|  👑 = Premium Only               |
+----------------------------------+
|                                  |
|      ACTION BUTTONS              |
|                                  |
|    [Back]           [Next]       |
|                                  |
+----------------------------------+
```

### Key Elements
- **Progress Indicator**: Shows current step in creation process
- **Character Selection**: Radio buttons for all character options
- **Avatar Preview**: Dynamic image that updates based on selections
- **Premium Indicators**: Crown icons for subscriber-only features
- **Navigation**: Clear back and next buttons

## Page 3: Partner Creation Page (Subscriber Preview)

### Layout Structure
```
+----------------------------------+
|            HEADER                |
| [Back] Partner Creation   [Help] |
+----------------------------------+
|                                  |
|       PROGRESS INDICATOR         |
|    ●━━━━━━━●━━━━━━━○             |
|  Character  Partner   Story      |
|                                  |
+----------------------------------+
|                                  |
|      PREMIUM OVERLAY             |
|                                  |
|    🔒 PREMIUM FEATURE            |
|                                  |
|   "Create a story partner to     |
|    enhance your narrative        |
|    experience"                   |
|                                  |
|   ✓ Multiple characters          |
|   ✓ Character relationships      |
|   ✓ Advanced storylines          |
|                                  |
|    [Upgrade to Premium]          |
|    [Continue with Free Version]  |
|                                  |
+----------------------------------+
|                                  |
|    GRAYED OUT PARTNER OPTIONS    |
|  (Same as character selection    |
|   but visually disabled)         |
|                                  |
|  Perspective: ○ 1st ○ 3rd        |
|  Gender: ○ Male ○ Female ○ Alien |
|  Career: ○ CEO ○ Artist ○ Other  |
|                                  |
+----------------------------------+
|                                  |
|      ACTION BUTTONS              |
|                                  |
|    [Back]           [Next]       |
|                                  |
+----------------------------------+
```

### Key Elements
- **Premium Overlay**: Clear indication this is a paid feature
- **Feature Benefits**: List of what premium unlocks
- **Upgrade CTA**: Prominent upgrade button
- **Fallback Option**: Continue with free version
- **Disabled Preview**: Shows what's available but grayed out

## Page 4: Story Presentation Page

### Layout Structure
```
+----------------------------------+
|            HEADER                |
| [Menu] Story View        [⚙️]    |
+----------------------------------+
|                                  |
|                                  |
|        IMAGE CANVAS              |
|     [AI Generated Image]         |
|        (Large Display)           |
|                                  |
|                                  |
+----------------------------------+
|                                  |
|       STORY TEXT AREA            |
|                                  |
|  "Once upon a time, in a land    |
|   far away, your character       |
|   began an incredible journey... |
|                                  |
|   What do you do next?"          |
|                                  |
|  [Text Input Field]              |
|  "Type your response..."         |
|                                  |
+----------------------------------+
|                                  |
|       CONTROL PANEL              |
|                                  |
| [🔇] Mute  [🎵] Sound Effects    |
|                                  |
|        [🎤]           [📱]       |
|     Voice Input      Phone       |
|                                  |
|           [End Story]            |
|                                  |
+----------------------------------+
```

### Key Elements
- **Image Canvas**: Large area for AI-generated visuals (60% of viewport)
- **Story Text**: Narrative text with clear typography
- **Input Field**: Text area for user responses
- **Control Panel**: Audio controls, voice input, phone access
- **Action Buttons**: Large, accessible touch targets

## Phone Overlay (When Phone Icon Clicked)

### Layout Structure
```
+----------------------------------+
|         PHONE OVERLAY            |
|  +----------------------------+  |
|  |        📱 Phone            |  |
|  |                            |  |
|  |  📅 June 27, 2025          |  |
|  |  🕐 10:43 AM               |  |
|  |                            |  |
|  |      CONTACTS              |  |
|  |                            |  |
|  |  📞 Mom                    |  |
|  |  📞 Best Friend            |  |
|  |  📞 Work                   |  |
|  |  📞 Emergency Services     |  |
|  |                            |  |
|  |        [Close]             |  |
|  +----------------------------+  |
|                                  |
|     [Background Story Image]     |
|        (Dimmed/Blurred)          |
+----------------------------------+
```

### Key Elements
- **Modal Overlay**: Phone interface over story background
- **Date/Time**: Current story context
- **Contact List**: Predefined contacts for story interaction
- **Close Button**: Return to main story view
- **Background**: Dimmed story image maintains context

## Responsive Design Considerations

### Mobile Layout Adjustments
- **Stacked Elements**: Single column layout on mobile
- **Larger Touch Targets**: Minimum 44px for all interactive elements
- **Simplified Navigation**: Hamburger menu for secondary options
- **Optimized Text Size**: Readable without zooming
- **Thumb-Friendly Controls**: Bottom placement for primary actions

### Tablet Layout
- **Hybrid Approach**: Combines mobile and desktop elements
- **Side-by-Side**: Character selection and avatar preview
- **Larger Canvas**: More space for story presentation
- **Enhanced Controls**: Additional space for control panel

This wireframe structure provides a clear foundation for the development phase, ensuring all required features are accounted for and properly organized.

