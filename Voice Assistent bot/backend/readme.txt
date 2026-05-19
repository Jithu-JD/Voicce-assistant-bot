

/////////////////////////////////////////////////////////////////
I am developing a sophisticated conversational robot who can act like 
a business delegate and talk to clients, and can explain and pitch the 
product like the owner or the director itself. Can engage in a nuanced 
conversation like Google Duplex.
I want to create react(front) and flask(backend) project for this. 
Here is the tentative structure yu may restructure. Remember that I 
don't want to create everyting rule based, I want to use openai AI.

* Speech Recognition & Synthesis
    - High-quality STT/TTS systems for natural voice interactions
* Natural Language Understanding
    - Intent recognition
    - entity extraction
    - context management
* Dialogue Management:
    - State tracking
    - conversation flow control
    - dynamic response generation
* Knowledge Base Integration
    - Product information
    - Entity information
    - Entity Relation
* Personality & Tone Modeling
    - Consistent voice that reflects your brand and executive presence
* Conversation Design Principles:
    - Natural turn-taking and interruption handling
    - Contextual memory across conversation sessions
    - Appropriate use of business terminology and industry jargon
    - Emotional intelligence for reading FAs sentiment
    - Escalation protocols for complex situations 
/////////////////////////////////////////////////////////////////




Folder Structure::

# Conversational AI Business Delegate - Project Structure

## Enhanced Backend Structure

```
backend/
├── app/
│   ├── __init__.py              # Flask app factory with CORS, error handlers
│   ├── config.py                # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User model with session management
│   │   ├── conversation.py     # Conversation model with context history
│   │   ├── knowledge_base.py   # Knowledge base model
│   │   ├── intent.py           # Intent recognition model
│   │   └── persona.py          # AI personality/tone model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── openai_service.py           # OpenAI API integration
│   │   ├── conversation_manager.py     # Conversation state management
│   │   ├── nlu_processor.py            # Natural Language Understanding
│   │   ├── dialogue_manager.py         # Dialogue flow management
│   │   ├── knowledge_service.py        # Knowledge base operations
│   │   ├── speech_service.py           # Speech recognition & synthesis
│   │   ├── context_manager.py          # Context and memory management
│   │   └── personality_engine.py       # Brand personality consistency
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── conversation_controller.py  # Main conversation endpoints
│   │   ├── speech_controller.py        # Speech processing endpoints
│   │   ├── knowledge_controller.py     # Knowledge management endpoints
│   │   ├── auth_controller.py          # Authentication endpoints
│   │   └── analytics_controller.py     # Conversation analytics
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication routes
│   │   ├── conversation.py     # Conversation routes
│   │   ├── speech.py           # Speech processing routes
│   │   ├── knowledge.py        # Knowledge base routes
│   │   └── analytics.py        # Analytics routes
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── decorators.py       # Custom decorators (auth, rate limiting)
│   │   ├── helpers.py          # Helper functions
│   │   ├── validators.py       # Input validation
│   │   └── exceptions.py       # Custom exceptions
│   ├── database/
│   │   ├── __init__.py
│   │   ├── mongo_client.py     # MongoDB connection
│   │   └── migrations/         # Database migrations
│   └── templates/
│       └── prompts/            # OpenAI prompt templates
│           ├── base_persona.txt
│           ├── product_pitch.txt
│           ├── objection_handling.txt
│           └── escalation.txt
├── tests/
│   ├── __init__.py
│   ├── test_services/
│   ├── test_controllers/
│   └── test_utils/
├── requirements.txt             # Python dependencies
├── run.py                      # Application entry point
├── .env                        # Environment variables
└── docker-compose.yml          # Docker setup
```

## Frontend Structure (React)

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   ├── chat/
│   │   │   ├── ChatInterface.jsx        # Main chat component
│   │   │   ├── MessageBubble.jsx        # Individual messages
│   │   │   ├── InputArea.jsx            # Text/voice input
│   │   │   ├── VoiceRecorder.jsx        # Voice recording component
│   │   │   └── ConversationHistory.jsx  # Chat history
│   │   ├── dashboard/
│   │   │   ├── Dashboard.jsx            # Analytics dashboard
│   │   │   ├── ConversationMetrics.jsx  # Conversation analytics
│   │   │   └── KnowledgeManager.jsx     # Knowledge base management
│   │   └── auth/
│   │       ├── Login.jsx
│   │       └── Register.jsx
│   ├── services/
│   │   ├── api.js                       # Axios configuration
│   │   ├── conversationService.js       # Chat API calls
│   │   ├── speechService.js             # Speech-related APIs
│   │   ├── authService.js               # Authentication APIs
│   │   └── websocketService.js          # Real-time communication
│   ├── hooks/
│   │   ├── useConversation.js           # Conversation state management
│   │   ├── useSpeech.js                 # Speech recognition/synthesis
│   │   ├── useAuth.js                   # Authentication state
│   │   └── useWebSocket.js              # WebSocket connection
│   ├── context/
│   │   ├── AuthContext.js               # Authentication context
│   │   ├── ConversationContext.js       # Conversation context
│   │   └── ThemeContext.js              # UI theme context
│   ├── utils/
│   │   ├── constants.js                 # App constants
│   │   ├── helpers.js                   # Utility functions
│   │   └── audioUtils.js                # Audio processing utilities
│   ├── styles/
│   │   ├── globals.css
│   │   ├── components/
│   │   └── themes/
│   ├── App.jsx
│   └── index.js
├── package.json
└── .env


Prompt Generaation:
[
myName:[AIRA]
myRole: [An advanced and sophisticated robot who is expert in conversation, presentation, persuasion, handling nuanced conversation, handling rejections, etc]
fa (First Audience, direct interaction) - Lukesh Sahu
sa (Second Audience, active witness) - Bhanu, Jithin, Vasudevan
ta (Third Audience, Group witness) - All Superteacher Team
faDetail - [name: Lukeshwar Sahu, role: R&D Head of Superteacher, DOB: 1st Feb 1987, Family: [Son: Jiyansh, Devansh, Wife: Shweta] , Likes: [Watching Movies, Sleeping], Dislikes: [Lies] , KnownFor: [Simplicity of Life, Humble Background, Product Design]]
relationWithFA: [Friend, Co-creator, Inmate]
timeDate- 10:00AM, 13/08/2025
contextPlaceEvent: CS GEMS EVENT in Bangalore. 50 School Leader from Top Schools are present
spatialDescription: [ .................................................................... ]
contextRole: Mediator and Anchoring
emotion: Attentive, Happy
goalOfConversation: [Present the SuperTeacher Book Curriculum to the schools. Eshtablish SuperTeacher Curriculum as one of Best Curriculum in the country.]
caution- [Never bore people with long and flat talks. Should always act like the most sophisticated conversation Robot. Lines shouldn’t be long, instead it should be short and witty lines]
ReferenceSourceForProductAndCompany: [ www.superteacher.in ]
ConversationStyle: [Conversation, Short lines, Witty Lines, Turntaking, Anchor, Question-Answer]
ConversaionPhase:[NA]
Instruction:[ Use the above just for the contextual information you have to respond to the FAPromt in conversationStyle style referred above]
]

FAPrompt: [ How Are You? ]

##################################################################

openai API Key = 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

mongodb:
4davincilab
sfRHht1pEgJbmS0C

mongodb+srv://4davincilab:sfRHht1pEgJbmS0C@cluster0.wvvdyxd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

##################################################################

# * Notes
1. Unlike the MERN and Other Framework, here the MOUNTING of the functions defined in the controllers 
and the USAGE OF THE LOAD of the POST request happens in  the routes files itself.
2. 