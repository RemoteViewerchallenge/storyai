import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { 
  ArrowLeft, 
  Mic, 
  Phone, 
  Volume2, 
  VolumeX, 
  Music, 
  MusicOff, 
  Send,
  X,
  Clock,
  User
} from 'lucide-react'

export default function StoryPresentationPage({ 
  onBack, 
  character, 
  subscription = { tier: 'free', can_use_premium_features: false } 
}) {
  const [storyState, setStoryState] = useState({
    currentImage: '/api/placeholder/800/600',
    narrativeText: 'Your story begins here...',
    userInput: '',
    isAudioPlaying: false,
    isMuted: false,
    soundEffectsEnabled: true,
    showPhone: false
  })

  const [isLoading, setIsLoading] = useState(false)

  const handleUserSubmit = () => {
    if (!storyState.userInput.trim()) return
    
    setIsLoading(true)
    setTimeout(() => {
      setStoryState(prev => ({
        ...prev,
        narrativeText: `You decided to: "${prev.userInput}". The story continues...`,
        userInput: ''
      }))
      setIsLoading(false)
    }, 1000)
  }

  const togglePhone = () => {
    setStoryState(prev => ({
      ...prev,
      showPhone: !prev.showPhone
    }))
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <div className="bg-gray-800 p-4 flex items-center justify-between border-b border-gray-700">
        <Button variant="ghost" onClick={onBack} className="text-white hover:bg-gray-700">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back
        </Button>
        <h1 className="text-xl font-bold">Your Story</h1>
        <Button variant="destructive" size="sm">
          End Story
        </Button>
      </div>

      <div className="p-4">
        {/* Image Canvas */}
        <div className="bg-black h-96 flex items-center justify-center mb-4 rounded-lg">
          <img 
            src={storyState.currentImage} 
            alt="Story Scene" 
            className="max-w-full max-h-full object-contain rounded"
            onError={(e) => {
              e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAwIiBoZWlnaHQ9IjYwMCIgdmlld0JveD0iMCAwIDgwMCA2MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI4MDAiIGhlaWdodD0iNjAwIiBmaWxsPSIjMUYyOTM3Ii8+CjxjaXJjbGUgY3g9IjQwMCIgY3k9IjMwMCIgcj0iNTAiIGZpbGw9IiM0Qjc2ODgiLz4KPHRleHQgeD0iNDAwIiB5PSIzNzAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiM5Q0EzQUYiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIyNCI+U3RvcnkgU2NlbmU8L3RleHQ+Cjwvc3ZnPg=='
            }}
          />
        </div>

        {/* Story Text */}
        <div className="bg-gray-800 p-4 rounded-lg mb-4">
          <div className="h-32 overflow-y-auto text-gray-100">
            {storyState.narrativeText}
          </div>
        </div>

        {/* User Input and Controls */}
        <div className="flex gap-2">
          <Input
            value={storyState.userInput}
            onChange={(e) => setStoryState(prev => ({ ...prev, userInput: e.target.value }))}
            placeholder="What do you want to do next?"
            className="flex-1 bg-gray-800 border-gray-600 text-white"
            disabled={isLoading}
          />
          
          <Button
            variant="outline"
            size="sm"
            onClick={togglePhone}
            className="border-gray-600 text-white hover:bg-gray-700"
          >
            <Phone className="h-4 w-4" />
          </Button>

          <Button
            onClick={handleUserSubmit}
            disabled={!storyState.userInput.trim() || isLoading}
            size="sm"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>

        {/* Phone Modal */}
        {storyState.showPhone && (
          <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
            <Card className="w-80 bg-gray-800 border-gray-600">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-white">Phone</h3>
                  <Button variant="ghost" size="sm" onClick={togglePhone} className="text-white">
                    <X className="h-4 w-4" />
                  </Button>
                </div>
                
                <div className="text-center text-white">
                  <div className="text-2xl font-bold">12:34</div>
                  <div className="text-sm text-gray-400">Today</div>
                </div>

                <div className="mt-4 space-y-2">
                  <h4 className="font-medium text-white">Contacts</h4>
                  <Button
                    variant="ghost"
                    className="w-full justify-start text-white hover:bg-gray-700"
                    onClick={() => {
                      alert('Calling Assistant...')
                      togglePhone()
                    }}
                  >
                    <User className="h-4 w-4 mr-3" />
                    Assistant
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {isLoading && (
          <div className="text-center mt-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto"></div>
            <p className="mt-2">Generating story...</p>
          </div>
        )}
      </div>
    </div>
  )
}

