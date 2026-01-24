# Scaters Raptor Roadshow 2026

> **Mission: The Predatory Hunt** - Engineering British Supremacy on the Pavement

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D14.0.0-brightgreen)](https://nodejs.org/)

## 🎯 Overview

Scaters Raptor Roadshow 2026 transforms the UK's iconic streets into tactical hunting grounds. This campaign features the ultimate UK skateboard challenge "The Predatory Hunt" hitting London, Manchester, and Glasgow with pro skaters Lucien Clarke & Geoff Rowley.

### Key Features
- 🏆 **£310,000 Bounty** - Apex rewards for champions
- 🎨 **5 Raptor Series Decks** - The ultimate weapon collection
- 🗺️ **3 UK Cities** - London, Manchester, Glasgow
- 🤖 **Interactive AI Chat** - The Butler tactical assistant
- 📱 **Responsive Design** - Mobile-first approach
- 🔗 **Google Forms Integration** - Unified registration system

## 🚀 Quick Start

### Prerequisites
- Node.js >= 14.0.0
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/scaters/scaters-raptor-roadshow-2026.git
   cd scatters-raptor-roadshow-2026
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   ```
   http://localhost:3000
   ```

### Production Deployment
```bash
npm start
```

## 📁 Project Structure

```
scaters-raptor-roadshow-2026/
├── index.html          # Main website
├── server.js           # Express server
├── package.json        # Dependencies & scripts
├── robots.txt          # SEO/Crawler instructions
└── README.md           # This file
```

## 🛠️ Technology Stack

- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Backend**: Node.js, Express.js
- **Styling**: Tailwind CSS with custom animations
- **Icons**: Font Awesome 6
- **Forms**: Google Forms integration
- **Deployment**: Static hosting ready

## 🎮 Features

### The Hunt
- **London** (Mar 12): Southbank Undercroft - "The Concrete Heart"
- **Manchester** (Mar 19): Projekt MCR - "The Industrial Abyss"
- **Glasgow** (Mar 26): Kelvingrove - "The Northern Peak"

### Raptor Collection
1. **The Eagle** - Sky Dominator (Aerial dominance)
2. **The Panther** - Shadow Hunter (Technical precision)
3. **The Bull** - Ground Breaker (Raw power)
4. **The Shark** - Flow Machine (Speed & momentum)
5. **The Snake** - Flex Assassin (Adaptive reflexes)

### Interactive Elements
- Real-time countdown to launch
- Dynamic product showcase
- AI-powered chat assistant
- Google Forms registration
- Responsive animations

## 🔧 Development

### Available Scripts

```bash
npm start      # Production server
npm run dev    # Development with auto-reload
npm run build  # Build for deployment (static site)
```

### Environment Variables

Create a `.env` file for custom configuration:

```env
PORT=3000
NODE_ENV=development
```

## 🤖 AI-Powered Python Chatbot

### Setup & Installation

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

3. **Get an API Key**
   - **Google Gemini** (Recommended): https://makersuite.google.com/app/apikey
   - **OpenAI** (Alternative): https://platform.openai.com/api-keys

4. **Run the chatbot**
   ```bash
   python chatbot.py
   ```

### Features

- 🧠 **AI-Powered Responses** - Uses Google Gemini or OpenAI for intelligent conversations
- 🎯 **Topic-Scoped** - Only answers questions about the roadshow and Raptor collection
- 🔐 **Secure API Keys** - Keys stored in .env file (never committed)
- 💬 **Interactive Console** - Terminal-based chat interface
- 🔄 **Fallback Mode** - Works with pattern matching if no API key configured
- 🎭 **Rule-Based Prompting** - Smart responses for specific query types:
  - 📍 **Location queries** → Mission Brief format
  - 🛡️ **Safety/fear concerns** → Reassurance with safety details
  - 💰 **Prize queries** → FOMO-inducing exclusive reveals
  - 🛹 **Frustration detection** → Humor and light-hearted support
- 😊 **Sentiment Analysis** - Detects user emotions using VADER sentiment analysis

### Usage

The chatbot answers questions about:
- Roadshow locations, dates, and activities
- The Raptor skateboard collection (features, models, target customers)
- Pro skaters, prizes, and event details

**Commands:**
- Type your question and press Enter
- `quit` or `exit` - End the chat
- `clear` - Clear chat history

**Example conversations:**

**Location Query (Mission Brief Format):**
```
YOU: Where is the next event?
BUTLER: 🎯 YOUR MISSION: Join us at these tactical locations where the ultimate challenge awaits!

📍 LONDON - April 04, 2026
   Mission Site: Southbank Undercroft ("The Concrete Heart")
   Your Mission: Execute precision techniques in the capital's most iconic spot
...
```

**Safety Query (Reassurance):**
```
YOU: Is it safe to participate?
BUTLER: We prioritize safety above all else. Rest assured, our events are supervised 
by professionals and follow strict safety guidelines. All venues have:
• On-site medical teams and first aid
• Safety equipment checks
...
```

**Prize Query (FOMO Response):**
```
YOU: What can I win?
BUTLER: 💰 The bounty is worth the hunt! We're talking SERIOUS rewards...
🏆 The prize pool is MASSIVE - but we're keeping some surprises under wraps!
Join us to uncover what's waiting for YOU at the apex of the hunt.
```

**Frustration Detection (Humor):**
```
YOU: This is so confusing!
BUTLER: Whoa! Let's take a kickflip back. We got this together. 🛹
What's bugging you? I'm here to help make this super simple.
```

### Testing

Run the test suite to verify chatbot functionality:
```bash
python test_chatbot.py
```

The tests verify:
- ✓ Location queries trigger Mission Brief format
- ✓ Safety/fear queries provide reassurance
- ✓ Prize queries create FOMO responses
- ✓ Frustration is detected and handled with humor
- ✓ Sentiment analysis works correctly
- ✓ Chat history is maintained

## 🌐 Web Chatbot (JavaScript)

The website includes an enhanced AI-powered chatbot with the same intelligent features:

### Features

- 🎨 **Styled Responses** - Beautiful gradient-styled responses matching Scaters branding
- 🧠 **Rule-Based Prompting** - Same smart query detection as Python chatbot:
  - 📍 Location queries → Mission Brief with blue/royal styling
  - 🛡️ Safety queries → Reassurance with gold styling  
  - 💰 Prize queries → FOMO response with purple gradient
  - 🛹 Frustration → Humor with pink/orange styling
- 😊 **Browser-Based Sentiment Analysis** - Lightweight sentiment detection in JavaScript
- 🤖 **AI Integration** - Uses Google Gemini API when available
- 🔄 **Smart Fallback** - Rule-based responses work without AI API

### Usage

1. Click the binoculars icon in the bottom-right corner
2. Type your question or use quick action buttons
3. Experience intelligent, context-aware responses

### Training the Chatbot

To extend or modify the chatbot behavior:

**Python Chatbot (`chatbot.py`):**
1. Add new keywords to the relevant lists in `_apply_rule_based_prompting()`
2. Create response templates following the existing pattern
3. Add tests in `test_chatbot.py` for new scenarios
4. Run tests to verify: `python test_chatbot.py`

**JavaScript Chatbot (`index.html`):**
1. Modify `applyRuleBasedPrompting()` function
2. Add keywords and response HTML with appropriate styling
3. Test manually in the browser
4. Use browser console to verify rule detection logs

**Response Styling Guidelines:**
- Location/Mission: Blue (#2563EB) gradient
- Safety: Gold (#D4AF37) gradient
- Prizes: Purple (#8B5CF6) gradient
- Frustration: Pink/Orange (#EC4899/#F97316) gradient
- Use emojis for visual appeal (🎯, 🛡️, 💰, 🛹)

## 📊 SEO & Performance

- **Meta Tags**: Optimized for social sharing
- **Structured Data**: JSON-LD for rich snippets
- **Performance**: Lazy-loaded images and optimized assets
- **Accessibility**: WCAG compliant design

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 About Scaters

**Scaters Worldwide** - Engineering British supremacy since 1998. From street rats to tycoons, we define excellence through physics, not flags.

### Contact
- Website: [scaters.com](https://scaters.com)
- Email: info@scaters.com
- Social: [@scaters](https://instagram.com/scaters)

---

**⚠️ WARNING**: This is a high-stakes operation. Only the strongest predators will claim the spoils of war. Join the hunt or get out of the way.

*"When you step onto a Scaters deck, you are taking command."*
