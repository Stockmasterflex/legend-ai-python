#!/bin/bash

# Test Telegram Bot Commands
# This script tests all bot commands by simulating webhook calls

BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
WEBHOOK_URL="https://legend-ai-python-production.up.railway.app/api/webhook/telegram"

# Test chat ID (replace with your actual Telegram chat ID)
CHAT_ID="123456789"

echo "🤖 Testing Legend AI Telegram Bot Commands..."
echo "================================================"
echo ""

# Test /start command
echo "1️⃣ Testing /start command..."
curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": {
      \"message_id\": 1,
      \"from\": {\"id\": $CHAT_ID, \"first_name\": \"Test\", \"username\": \"test_user\"},
      \"chat\": {\"id\": $CHAT_ID, \"type\": \"private\"},
      \"text\": \"/start\"
    }
  }" > /dev/null
echo "✅ /start command sent"
echo ""

# Test /help command
echo "2️⃣ Testing /help command..."
curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": {
      \"message_id\": 2,
      \"from\": {\"id\": $CHAT_ID, \"first_name\": \"Test\", \"username\": \"test_user\"},
      \"chat\": {\"id\": $CHAT_ID, \"type\": \"private\"},
      \"text\": \"/help\"
    }
  }" > /dev/null
echo "✅ /help command sent"
echo ""

# Test /pattern command
echo "3️⃣ Testing /pattern AAPL command..."
curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": {
      \"message_id\": 3,
      \"from\": {\"id\": $CHAT_ID, \"first_name\": \"Test\", \"username\": \"test_user\"},
      \"chat\": {\"id\": $CHAT_ID, \"type\": \"private\"},
      \"text\": \"/pattern AAPL\"
    }
  }" > /dev/null
echo "✅ /pattern AAPL command sent"
echo ""

# Test /chart command
echo "4️⃣ Testing /chart NVDA command..."
curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": {
      \"message_id\": 4,
      \"from\": {\"id\": $CHAT_ID, \"first_name\": \"Test\", \"username\": \"test_user\"},
      \"chat\": {\"id\": $CHAT_ID, \"type\": \"private\"},
      \"text\": \"/chart NVDA\"
    }
  }" > /dev/null
echo "✅ /chart NVDA command sent"
echo ""

# Test /scan command
echo "5️⃣ Testing /scan command..."
curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": {
      \"message_id\": 5,
      \"from\": {\"id\": $CHAT_ID, \"first_name\": \"Test\", \"username\": \"test_user\"},
      \"chat\": {\"id\": $CHAT_ID, \"type\": \"private\"},
      \"text\": \"/scan\"
    }
  }" > /dev/null
echo "✅ /scan command sent"
echo ""

# Test natural language query
echo "6️⃣ Testing AI natural language: 'analyze TSLA'..."
curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": {
      \"message_id\": 6,
      \"from\": {\"id\": $CHAT_ID, \"first_name\": \"Test\", \"username\": \"test_user\"},
      \"chat\": {\"id\": $CHAT_ID, \"type\": \"private\"},
      \"text\": \"analyze TSLA\"
    }
  }" > /dev/null
echo "✅ Natural language query sent"
echo ""

echo "================================================"
echo "✅ All test commands sent successfully!"
echo ""
echo "📱 Check your Telegram bot to see the responses"
echo "   Bot: @YourBotName"
echo ""
echo "📊 Check logs for any errors:"
echo "   railway logs"

