import { useState } from 'react'
import WelcomePage from './components/WelcomePage.jsx'
import CharacterCreationPage from './components/CharacterCreationPage.jsx'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('welcome')
  const [userData, setUserData] = useState({
    character: null,
    story: null,
    subscription: { tier: 'free', can_use_premium_features: false }
  })

  const handleWelcomeContinue = () => {
    setCurrentPage('character-creation')
  }

  const handleCharacterCreated = (character) => {
    setUserData(prev => ({ ...prev, character }))
    setCurrentPage('story-presentation')
  }

  const handleBackToWelcome = () => {
    setCurrentPage('welcome')
  }

  const handleBackToCharacterCreation = () => {
    setCurrentPage('character-creation')
  }

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'welcome':
        return <WelcomePage onContinue={handleWelcomeContinue} />
      case 'character-creation':
        return (
          <CharacterCreationPage 
            onBack={handleBackToWelcome}
            onCharacterCreated={handleCharacterCreated}
            subscription={userData.subscription}
          />
        )
      case 'story-presentation':
        return (
          <div className="min-h-screen bg-gray-900 text-white p-8">
            <div className="max-w-4xl mx-auto">
              <div className="flex items-center justify-between mb-6">
                <button 
                  onClick={handleBackToCharacterCreation}
                  className="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600 flex items-center gap-2"
                >
                  ← Back to Character Creation
                </button>
                <h1 className="text-2xl font-bold">Your Story</h1>
                <button className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
                  End Story
                </button>
              </div>

              {/* Story Image Canvas */}
              <div className="bg-black h-96 flex items-center justify-center mb-6 rounded-lg">
                <div className="text-center text-gray-400">
                  <div className="w-16 h-16 bg-gray-600 rounded-full mx-auto mb-4"></div>
                  <p>Story Scene</p>
                  <p className="text-sm">AI-generated image will appear here</p>
                </div>
              </div>

              {/* Story Text */}
              <div className="bg-gray-800 p-6 rounded-lg mb-6">
                <div className="h-32 overflow-y-auto text-gray-100">
                  <p>
                    You stand at the entrance of the gleaming corporate tower, your reflection caught in the polished glass doors. 
                    As the newly appointed CEO of TechNova Industries, today marks the beginning of your journey to transform this company. 
                    The morning sun casts long shadows across the marble lobby as employees begin to arrive for another day of work.
                  </p>
                  <p className="mt-4">
                    What would you like to do next?
                  </p>
                </div>
              </div>

              {/* User Input and Controls */}
              <div className="flex gap-4 items-end">
                <div className="flex-1">
                  <input
                    type="text"
                    placeholder="What do you want to do next? Describe your action..."
                    className="w-full p-3 bg-gray-800 border border-gray-600 text-white rounded-lg"
                  />
                </div>
                
                <div className="flex gap-2">
                  <button className="p-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600" title="Voice Input">
                    🎤
                  </button>
                  <button className="p-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600" title="Phone">
                    📞
                  </button>
                  <button className="px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Continue Story
                  </button>
                </div>
              </div>

              {/* Story Progress */}
              <div className="mt-4 flex items-center justify-between text-sm text-gray-400">
                <div>Story Segments: 1</div>
                <div className="flex items-center gap-4">
                  <span className="px-2 py-1 bg-gray-700 rounded text-xs">Free Tier</span>
                  <span className="text-xs">4 stories remaining this month</span>
                </div>
              </div>
            </div>
          </div>
        )
      default:
        return <WelcomePage onContinue={handleWelcomeContinue} />
    }
  }

  return (
    <div className="App">
      {renderCurrentPage()}
    </div>
  )
}

export default App

