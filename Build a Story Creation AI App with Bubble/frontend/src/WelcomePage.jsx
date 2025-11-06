import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Checkbox } from '@/components/ui/checkbox.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Sparkles, BookOpen, Users, Mic } from 'lucide-react'

export default function WelcomePage({ onContinue }) {
  const [termsAccepted, setTermsAccepted] = useState(false)
  const [status, setStatus] = useState(null)

  useEffect(() => {
    fetch('/api/status')
      .then(response => response.json())
      .then(data => setStatus(data.status))
      .catch(error => console.error('Error fetching status:', error));
  }, []);

  const handleContinue = () => {
    if (termsAccepted) {
      onContinue()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
      <div style={{ position: 'absolute', top: 0, left: 0, padding: '10px', backgroundColor: 'rgba(0,0,0,0.5)', color: 'white' }}>
        Backend Status: {status || 'Loading...'}
      </div>
      <div className="max-w-4xl w-full space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center space-x-2">
            <Sparkles className="h-8 w-8 text-purple-600" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Story AI
            </h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Create your own interactive AI-powered stories with dynamic characters, immersive visuals, and voice narration
          </p>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6">
          <Card className="text-center">
            <CardHeader>
              <BookOpen className="h-8 w-8 text-purple-600 mx-auto mb-2" />
              <CardTitle className="text-lg">Interactive Stories</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                Guide your story with choices and watch it unfold with AI-generated content
              </p>
            </CardContent>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <Users className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <CardTitle className="text-lg">Dynamic Characters</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                Create unique characters with distinct personalities and visual styles
              </p>
            </CardContent>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <Mic className="h-8 w-8 text-green-600 mx-auto mb-2" />
              <CardTitle className="text-lg">Voice Narration</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                Experience your stories with AI-generated voice narration and character voices
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Terms and Conditions */}
        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle>Terms and Conditions</CardTitle>
            <CardDescription>
              Please read and accept our terms to continue
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <ScrollArea className="h-40 w-full border rounded-md p-4">
              <div className="space-y-3 text-sm text-gray-700">
                <p>
                  <strong>1. Service Description:</strong> Story AI provides interactive storytelling experiences 
                  powered by artificial intelligence. Our service generates text, images, and audio content 
                  based on your inputs and preferences.
                </p>
                <p>
                  <strong>2. User Responsibilities:</strong> You agree to use our service responsibly and not 
                  to generate inappropriate, harmful, or illegal content. You are responsible for your 
                  interactions with the AI system.
                </p>
                <p>
                  <strong>3. Content Ownership:</strong> Stories and characters you create remain your 
                  intellectual property. However, you grant us the right to use AI services to generate 
                  content based on your inputs.
                </p>
                <p>
                  <strong>4. Privacy:</strong> We collect and process data necessary to provide our service. 
                  Your story data is stored securely and used only to enhance your experience.
                </p>
                <p>
                  <strong>5. Subscription Terms:</strong> Our service offers both free and premium tiers. 
                  Free users have usage limitations, while premium subscribers enjoy unlimited access 
                  to all features.
                </p>
                <p>
                  <strong>6. AI-Generated Content:</strong> Content generated by our AI systems may not 
                  always be accurate or appropriate. We strive for quality but cannot guarantee the 
                  suitability of all generated content.
                </p>
                <p>
                  <strong>7. Service Availability:</strong> We aim to provide reliable service but cannot 
                  guarantee 100% uptime. Maintenance and updates may temporarily affect availability.
                </p>
                <p>
                  <strong>8. Changes to Terms:</strong> We reserve the right to update these terms. 
                  Continued use of the service after changes constitutes acceptance of new terms.
                </p>
              </div>
            </ScrollArea>

            <div className="flex items-center space-x-2">
              <Checkbox 
                id="terms" 
                checked={termsAccepted}
                onCheckedChange={setTermsAccepted}
              />
              <label 
                htmlFor="terms" 
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                I have read and agree to the Terms and Conditions
              </label>
            </div>

            <Button 
              onClick={handleContinue}
              disabled={!termsAccepted}
              className="w-full"
              size="lg"
            >
              Continue to Story Creation
            </Button>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="text-center text-sm text-gray-500">
          <p>© 2025 Story AI. Powered by advanced AI technology.</p>
        </div>
      </div>
    </div>
  )
}

