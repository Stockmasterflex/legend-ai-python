# AI Conversational Trading Assistant

## Overview

Enhanced AI-powered conversational assistant with natural language understanding, smart suggestions, learning mode, and voice command support.

## Features

### 1. Natural Language Queries

The assistant can understand and process natural language queries without requiring specific API endpoints.

**Examples:**
- "Show me VCP patterns today"
- "What's AAPL doing?"
- "Find tech breakouts"
- "Compare NVDA vs AMD"
- "When should I enter TSLA?"

**How it works:**
- Automatic intent detection from user messages
- Entity extraction (symbols, patterns, sectors)
- Smart routing to appropriate analysis functions
- Natural conversation flow

### 2. Smart Suggestions

Get intelligent recommendations based on technical analysis.

#### Similar Setups
Find stocks with similar chart patterns and technical setups.

**Endpoint:** `POST /api/ai/similar-setups`

**Example:**
```python
import requests

response = requests.post(
    'http://localhost:8000/api/ai/similar-setups',
    json={
        'reference_symbol': 'AAPL',
        'top_n': 5
    }
)

print(response.json())
```

**Response:**
```json
{
  "reference_symbol": "AAPL",
  "reference_pattern": "Cup and Handle",
  "similar_stocks": [
    {
      "symbol": "MSFT",
      "pattern": "Cup and Handle",
      "confidence": 75.5,
      "similarity_score": 0.755,
      "description": "Well-formed cup with handle consolidation"
    }
  ],
  "total_found": 5
}
```

#### Entry Timing Suggestions
Get AI-powered entry point suggestions with stop loss and targets.

**Endpoint:** `POST /api/ai/entry-timing`

**Example:**
```python
response = requests.post(
    'http://localhost:8000/api/ai/entry-timing',
    json={'symbol': 'TSLA'}
)
```

**Response:**
```json
{
  "symbol": "TSLA",
  "current_price": 245.50,
  "suggestions": [
    {
      "type": "pattern_based",
      "message": "Strong Bull Flag pattern detected",
      "action": "Consider entry on confirmation",
      "entry_price": 246.00,
      "stop_loss": 238.00,
      "target": 260.00
    }
  ],
  "support_level": 238.00,
  "resistance_level": 252.00,
  "risk_reward_ratio": 1.75
}
```

### 3. Learning Mode

Interactive educational features to improve trading skills.

#### Pattern Quiz
Test your knowledge with interactive quizzes.

**Endpoint:** `POST /api/ai/quiz`

**Difficulty Levels:** easy, medium, hard

**Example:**
```python
response = requests.post(
    'http://localhost:8000/api/ai/quiz',
    json={'difficulty': 'medium'}
)
```

**Response:**
```json
{
  "quiz_type": "pattern_recognition",
  "difficulty": "medium",
  "questions": [
    {
      "question": "What is the typical success rate of a well-formed Ascending Triangle pattern?",
      "options": [
        "A) 40-50%",
        "B) 60-70%",
        "C) 75-85%",
        "D) 90-95%"
      ],
      "correct": 1,
      "explanation": "Ascending triangles have a success rate of around 60-70% when properly identified with good volume confirmation."
    }
  ],
  "total_questions": 3
}
```

#### Strategy Tutorials
Learn trading strategies with step-by-step guides.

**Endpoint:** `POST /api/ai/tutorial`

**Available Strategies:** breakout, pullback, vcp, reversal

**Example:**
```python
response = requests.post(
    'http://localhost:8000/api/ai/tutorial',
    json={'strategy': 'breakout'}
)
```

#### Entry Rules Teaching
Learn exact entry rules for specific patterns.

**Endpoint:** `POST /api/ai/entry-rules`

**Example:**
```python
response = requests.post(
    'http://localhost:8000/api/ai/entry-rules',
    json={'pattern': 'Cup and Handle'}
)
```

**Response:**
```json
{
  "pattern": "Cup and Handle",
  "entry_rules": {
    "entry_point": "Buy when price breaks above the handle's resistance on increased volume",
    "confirmation": [
      "Price closes above handle high",
      "Volume 40-50% above average",
      "Handle should be in upper half of cup",
      "Cup depth ideally 12-30%"
    ],
    "stop_loss": "Place stop just below handle low (typically 7-8% from entry)",
    "target": "Depth of cup added to breakout point",
    "example": "Cup: $40-$50-$45, Handle: $50-$48. Entry: $50.20, Stop: $46.50, Target: $60 (cup depth $10)"
  }
}
```

### 4. Voice Commands

Process transcribed voice commands for hands-free trading analysis.

**Endpoint:** `POST /api/ai/voice-command`

**How it works:**
1. Voice is transcribed to text (client-side using Web Speech API or similar)
2. Text sent to this endpoint
3. Natural language processing detects intent
4. Appropriate analysis is performed
5. Response returned (can be converted to speech client-side)

**Supported Commands:**
- "Show me AAPL analysis"
- "Find VCP patterns"
- "Compare NVDA and AMD"
- "What's TSLA doing?"
- "Explain Cup and Handle pattern"
- "Give me entry timing for MSFT"

**Example:**
```python
# After voice transcription
response = requests.post(
    'http://localhost:8000/api/ai/voice-command',
    json={'command': 'Show me AAPL analysis'}
)
```

**Response:**
```json
{
  "response": "Based on current analysis, AAPL is showing...",
  "voice_command": true,
  "execution_time_ms": 1250,
  "original_command": "Show me AAPL analysis",
  "intent": "stock_status",
  "symbol": "AAPL"
}
```

## Database Models

New tables added to support conversational features:

### ConversationHistory
Tracks all AI conversations for context and learning.

**Fields:**
- conversation_id
- user_id
- role (user/assistant/system)
- content
- intent_type
- entities (JSON)
- timestamp

### LearningProgress
Tracks user's learning progress through quizzes and tutorials.

**Fields:**
- user_id
- quiz_type
- difficulty
- questions_answered
- correct_answers
- accuracy
- patterns_learned (JSON)
- strategies_learned (JSON)
- last_quiz_at

### VoiceCommand
Tracks voice command usage for analytics.

**Fields:**
- user_id
- command_text
- intent_detected
- entities (JSON)
- response
- success
- execution_time_ms

### SmartSuggestion
Tracks smart suggestions provided to users.

**Fields:**
- user_id
- suggestion_type
- reference_symbol
- suggested_symbols (JSON)
- suggestion_data (JSON)
- user_action

## API Endpoints Summary

### Existing Endpoints
- `POST /api/ai/chat` - Conversational chat (now with NL understanding)
- `POST /api/ai/analyze` - Stock analysis
- `POST /api/ai/compare` - Compare stocks
- `POST /api/ai/explain-pattern` - Pattern explanation
- `POST /api/ai/clear-history` - Clear conversation
- `GET /api/ai/status` - Check AI status

### New Endpoints
- `POST /api/ai/similar-setups` - Find similar stock setups
- `POST /api/ai/entry-timing` - Get entry timing suggestions
- `POST /api/ai/quiz` - Generate pattern quiz
- `POST /api/ai/tutorial` - Get strategy tutorial
- `POST /api/ai/entry-rules` - Learn pattern entry rules
- `POST /api/ai/voice-command` - Process voice commands

## Integration Examples

### Frontend Integration (React/Vue/Angular)

```javascript
// Voice command integration
const handleVoiceCommand = async () => {
  // 1. Start voice recognition
  const recognition = new webkitSpeechRecognition();
  recognition.lang = 'en-US';

  recognition.onresult = async (event) => {
    const command = event.results[0][0].transcript;

    // 2. Send to API
    const response = await fetch('/api/ai/voice-command', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ command })
    });

    const result = await response.json();

    // 3. Display or speak response
    console.log(result.response);
    // Optionally convert to speech
    const utterance = new SpeechSynthesisUtterance(result.response);
    speechSynthesis.speak(utterance);
  };

  recognition.start();
};

// Natural language query
const handleNaturalQuery = async (query) => {
  const response = await fetch('/api/ai/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      message: query,
      include_market_data: true
    })
  });

  const result = await response.json();
  // Response automatically includes intent and relevant data
  console.log(result);
};

// Learning mode - quiz
const startQuiz = async (difficulty = 'medium') => {
  const response = await fetch('/api/ai/quiz', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ difficulty })
  });

  const quiz = await response.json();
  // Display questions and handle answers
  quiz.questions.forEach((q, i) => {
    console.log(`Q${i+1}: ${q.question}`);
    q.options.forEach(opt => console.log(opt));
  });
};
```

### Mobile App Integration (React Native)

```javascript
import Voice from '@react-native-voice/voice';

const TradingAssistant = () => {
  const [listening, setListening] = useState(false);

  const startVoiceCommand = async () => {
    try {
      await Voice.start('en-US');
      setListening(true);
    } catch (e) {
      console.error(e);
    }
  };

  Voice.onSpeechResults = async (e) => {
    const command = e.value[0];

    const response = await fetch('https://your-api.com/api/ai/voice-command', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ command })
    });

    const result = await response.json();
    // Handle result
  };

  return (
    <TouchableOpacity onPress={startVoiceCommand}>
      <Text>🎤 {listening ? 'Listening...' : 'Tap to speak'}</Text>
    </TouchableOpacity>
  );
};
```

## Natural Language Patterns

The assistant recognizes these patterns:

| Pattern | Example | Intent |
|---------|---------|--------|
| show_patterns | "Show me VCP patterns today" | List patterns of type |
| stock_status | "What's AAPL doing?" | Analyze stock |
| find_breakouts | "Find tech breakouts" | Scan for breakouts |
| compare | "Compare NVDA vs AMD" | Compare stocks |
| entry_timing | "When should I enter TSLA" | Entry suggestions |
| pattern_explanation | "Explain Cup and Handle pattern" | Pattern education |
| best_stocks | "Best tech stocks" | Top picks |

## Configuration

No additional configuration required! The conversational features work with your existing API keys:

- `OPENROUTER_API_KEY` or `OPENAI_API_KEY` - For AI responses
- `TWELVEDATA_API_KEY` - For market data

## Performance

- Natural language parsing: ~5-10ms
- Voice command processing: ~1-2 seconds (including analysis)
- Similar setups search: ~3-5 seconds (15 stocks)
- Quiz generation: <100ms (pre-built questions)
- Tutorial retrieval: <100ms (pre-built) or ~1-2s (AI-generated)

## Best Practices

1. **Voice Commands**
   - Use clear, concise commands
   - Speak ticker symbols clearly
   - Include action words (show, find, compare)

2. **Natural Language Queries**
   - Be specific with ticker symbols
   - Use common trading terminology
   - Ask one question at a time

3. **Learning Mode**
   - Start with easy difficulty
   - Complete tutorials before quizzes
   - Review explanations for wrong answers

4. **Smart Suggestions**
   - Review multiple suggestions
   - Check confidence scores
   - Verify with your own analysis

## Future Enhancements

Planned features:
- Multi-language support
- Custom pattern training
- Portfolio-specific suggestions
- Real-time voice alerts
- Personalized learning paths
- Advanced quiz analytics

## Support

For issues or questions:
- Check API status: `GET /api/ai/status`
- Review logs for errors
- Test with simple queries first
- Verify API keys are configured

## License

Part of Legend AI Trading Platform
