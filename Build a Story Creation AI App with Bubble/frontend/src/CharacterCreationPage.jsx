import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { ArrowLeft, Crown, User, Briefcase, Palette, Sparkles } from 'lucide-react'

export default function CharacterCreationPage({ onBack, onCharacterCreated, subscription = { tier: 'free', can_use_premium_features: false } }) {
  const [character, setCharacter] = useState({
    perspective: '',
    gender: '',
    variant: '',
    career: '',
    imageStyle: ''
  })

  const [avatarUrl, setAvatarUrl] = useState('/api/placeholder/200/200')

  const isPremium = subscription.can_use_premium_features

  const perspectives = [
    { value: '1st_person', label: '1st Person', description: 'Experience the story through your character\'s eyes' },
    { value: '3rd_person', label: '3rd Person', description: 'Watch your character\'s story unfold from outside' }
  ]

  const genders = [
    { value: 'male', label: 'Male', available: true },
    { value: 'female', label: 'Female', available: true },
    { value: 'alien', label: 'Alien', available: isPremium, premium: true }
  ]

  const maleVariants = [
    { value: 'male_1', label: 'Male 1', description: 'Classic masculine appearance' },
    { value: 'male_2', label: 'Male 2', description: 'Modern masculine appearance' }
  ]

  const femaleVariants = [
    { value: 'female_1', label: 'Female 1', description: 'Classic feminine appearance' },
    { value: 'female_2', label: 'Female 2', description: 'Modern feminine appearance' }
  ]

  const careers = [
    { value: 'ceo', label: 'Corporate CEO', description: 'Lead a major corporation' },
    { value: 'hip_hop_artist', label: 'Hip Hop Artist', description: 'Create music and perform' },
    { value: 'unemployed', label: 'Unemployed', description: 'Seeking new opportunities' }
  ]

  const imageStyles = [
    { value: 'anime', label: 'Anime', available: true, description: 'Japanese animation style' },
    { value: 'fantasy', label: 'Fantasy', available: isPremium, premium: true, description: 'Magical and mystical style' },
    { value: 'realistic', label: 'Realistic', available: isPremium, premium: true, description: 'Photorealistic style' }
  ]

  const getVariants = () => {
    if (character.gender === 'male') return maleVariants
    if (character.gender === 'female') return femaleVariants
    return []
  }

  const updateCharacter = (field, value) => {
    setCharacter(prev => {
      const updated = { ...prev, [field]: value }
      
      // Reset variant when gender changes
      if (field === 'gender') {
        updated.variant = ''
      }
      
      return updated
    })
  }

  // Simulate avatar update when character changes
  useEffect(() => {
    if (character.gender && character.imageStyle) {
      // In a real app, this would call the backend API to generate an avatar
      const avatarParams = new URLSearchParams({
        gender: character.gender,
        style: character.imageStyle,
        variant: character.variant || 'default'
      })
      setAvatarUrl(`/api/placeholder/200/200?${avatarParams.toString()}`)
    }
  }, [character.gender, character.imageStyle, character.variant])

  const isFormValid = () => {
    return character.perspective && 
           character.gender && 
           character.career && 
           character.imageStyle &&
           (character.gender === 'alien' || character.variant)
  }

  const handleNext = () => {
    if (isFormValid()) {
      onCharacterCreated(character)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Button variant="ghost" onClick={onBack} className="flex items-center space-x-2">
            <ArrowLeft className="h-4 w-4" />
            <span>Back</span>
          </Button>
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900">Create Your Character</h1>
            <p className="text-gray-600 mt-2">Design your story's protagonist</p>
          </div>
          <div className="w-20"></div> {/* Spacer for centering */}
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Character Options */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Perspective Selection */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <User className="h-5 w-5" />
                  <span>Story Perspective</span>
                </CardTitle>
                <CardDescription>Choose how you want to experience the story</CardDescription>
              </CardHeader>
              <CardContent>
                <RadioGroup value={character.perspective} onValueChange={(value) => updateCharacter('perspective', value)}>
                  <div className="grid md:grid-cols-2 gap-4">
                    {perspectives.map((perspective) => (
                      <div key={perspective.value} className="flex items-center space-x-2 p-4 border rounded-lg hover:bg-gray-50">
                        <RadioGroupItem value={perspective.value} id={perspective.value} />
                        <div className="flex-1">
                          <Label htmlFor={perspective.value} className="font-medium cursor-pointer">
                            {perspective.label}
                          </Label>
                          <p className="text-sm text-gray-600 mt-1">{perspective.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </RadioGroup>
              </CardContent>
            </Card>

            {/* Gender Selection */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <User className="h-5 w-5" />
                  <span>Character Type</span>
                </CardTitle>
                <CardDescription>Select your character's type</CardDescription>
              </CardHeader>
              <CardContent>
                <RadioGroup value={character.gender} onValueChange={(value) => updateCharacter('gender', value)}>
                  <div className="grid md:grid-cols-3 gap-4">
                    {genders.map((gender) => (
                      <div key={gender.value} className={`relative flex items-center space-x-2 p-4 border rounded-lg ${
                        gender.available ? 'hover:bg-gray-50' : 'opacity-50 cursor-not-allowed bg-gray-50'
                      }`}>
                        <RadioGroupItem 
                          value={gender.value} 
                          id={gender.value} 
                          disabled={!gender.available}
                        />
                        <div className="flex-1">
                          <Label 
                            htmlFor={gender.value} 
                            className={`font-medium flex items-center space-x-2 ${
                              gender.available ? 'cursor-pointer' : 'cursor-not-allowed'
                            }`}
                          >
                            <span className={gender.premium && !gender.available ? 'line-through' : ''}>
                              {gender.label}
                            </span>
                            {gender.premium && (
                              <Badge variant="secondary" className="text-xs">
                                <Crown className="h-3 w-3 mr-1" />
                                Premium
                              </Badge>
                            )}
                          </Label>
                        </div>
                      </div>
                    ))}
                  </div>
                </RadioGroup>
              </CardContent>
            </Card>

            {/* Variant Selection */}
            {character.gender && character.gender !== 'alien' && (
              <Card>
                <CardHeader>
                  <CardTitle>Character Variant</CardTitle>
                  <CardDescription>Choose your character's appearance style</CardDescription>
                </CardHeader>
                <CardContent>
                  <RadioGroup value={character.variant} onValueChange={(value) => updateCharacter('variant', value)}>
                    <div className="grid md:grid-cols-2 gap-4">
                      {getVariants().map((variant) => (
                        <div key={variant.value} className="flex items-center space-x-2 p-4 border rounded-lg hover:bg-gray-50">
                          <RadioGroupItem value={variant.value} id={variant.value} />
                          <div className="flex-1">
                            <Label htmlFor={variant.value} className="font-medium cursor-pointer">
                              {variant.label}
                            </Label>
                            <p className="text-sm text-gray-600 mt-1">{variant.description}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </RadioGroup>
                </CardContent>
              </Card>
            )}

            {/* Career Selection */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Briefcase className="h-5 w-5" />
                  <span>Career</span>
                </CardTitle>
                <CardDescription>What does your character do for a living?</CardDescription>
              </CardHeader>
              <CardContent>
                <Select value={character.career} onValueChange={(value) => updateCharacter('career', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a career" />
                  </SelectTrigger>
                  <SelectContent>
                    {careers.map((career) => (
                      <SelectItem key={career.value} value={career.value}>
                        <div>
                          <div className="font-medium">{career.label}</div>
                          <div className="text-sm text-gray-600">{career.description}</div>
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </CardContent>
            </Card>

            {/* Image Style Selection */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Palette className="h-5 w-5" />
                  <span>Image Style</span>
                </CardTitle>
                <CardDescription>Choose the visual style for your story</CardDescription>
              </CardHeader>
              <CardContent>
                <RadioGroup value={character.imageStyle} onValueChange={(value) => updateCharacter('imageStyle', value)}>
                  <div className="grid md:grid-cols-3 gap-4">
                    {imageStyles.map((style) => (
                      <div key={style.value} className={`relative flex items-center space-x-2 p-4 border rounded-lg ${
                        style.available ? 'hover:bg-gray-50' : 'opacity-50 cursor-not-allowed bg-gray-50'
                      }`}>
                        <RadioGroupItem 
                          value={style.value} 
                          id={style.value} 
                          disabled={!style.available}
                        />
                        <div className="flex-1">
                          <Label 
                            htmlFor={style.value} 
                            className={`font-medium flex items-center space-x-2 ${
                              style.available ? 'cursor-pointer' : 'cursor-not-allowed'
                            }`}
                          >
                            <span>{style.label}</span>
                            {style.premium && (
                              <Badge variant="secondary" className="text-xs">
                                <Crown className="h-3 w-3 mr-1" />
                                Premium
                              </Badge>
                            )}
                          </Label>
                          <p className="text-sm text-gray-600 mt-1">{style.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </RadioGroup>
              </CardContent>
            </Card>
          </div>

          {/* Avatar Preview */}
          <div className="lg:col-span-1">
            <Card className="sticky top-4">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Sparkles className="h-5 w-5" />
                  <span>Character Preview</span>
                </CardTitle>
                <CardDescription>Your character will look like this</CardDescription>
              </CardHeader>
              <CardContent className="text-center space-y-4">
                <div className="w-48 h-48 mx-auto bg-gray-200 rounded-lg flex items-center justify-center overflow-hidden">
                  <img 
                    src={avatarUrl} 
                    alt="Character Avatar" 
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjRjNGNEY2Ii8+CjxjaXJjbGUgY3g9IjEwMCIgY3k9IjgwIiByPSIzMCIgZmlsbD0iIzlDQTNBRiIvPgo8cGF0aCBkPSJNNTAgMTUwQzUwIDEyNS4xNDcgNzEuNzY1IDEwNSAxMDAgMTA1UzE1MCAxMjUuMTQ3IDE1MCAxNTBWMjAwSDUwVjE1MFoiIGZpbGw9IiM5Q0EzQUYiLz4KPC9zdmc+'
                    }}
                  />
                </div>
                
                {character.gender && character.career && character.imageStyle && (
                  <div className="space-y-2 text-sm">
                    <div className="p-3 bg-blue-50 rounded-lg">
                      <p className="font-medium text-blue-900">Character Summary</p>
                      <p className="text-blue-700 mt-1">
                        {character.perspective === '1st_person' ? 'First-person' : 'Third-person'} {character.gender} {careers.find(c => c.value === character.career)?.label.toLowerCase()} in {character.imageStyle} style
                      </p>
                    </div>
                  </div>
                )}

                <Button 
                  onClick={handleNext}
                  disabled={!isFormValid()}
                  className="w-full"
                  size="lg"
                >
                  Create Character & Start Story
                </Button>

                {!isPremium && (
                  <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                    <p className="text-sm text-yellow-800">
                      <Crown className="h-4 w-4 inline mr-1" />
                      Upgrade to Premium for alien characters and advanced image styles
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

