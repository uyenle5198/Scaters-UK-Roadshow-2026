#!/usr/bin/env python3
"""
Scaters Raptor Roadshow 2026 - AI-Powered Chatbot
Interactive terminal-based chatbot with advanced AI capabilities.

Features:
- Google Gemini API integration for intelligent responses
- OpenAI API support as alternative
- Topic-scoped responses (roadshow and skateboard launch only)
- Secure API key management via environment variables
- Natural conversation interface
"""

import os
import sys
from datetime import datetime
from typing import Optional

# Check for required dependencies
try:
    # Try newer google-genai first, fall back to google.generativeai
    try:
        import google.genai as genai
        GENAI_VERSION = 'new'
    except ImportError:
        import google.generativeai as genai
        GENAI_VERSION = 'legacy'
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    GENAI_VERSION = None
    print("Warning: google-generativeai not installed. Run: pip install google-generativeai")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Run: pip install python-dotenv")


class ScatersRoadshowChatbot:
    """AI-powered chatbot for Scaters Raptor Roadshow 2026."""
    
    # Roadshow context for scope filtering
    ROADSHOW_CONTEXT = """
    You are The Butler, an AI assistant for Scaters Raptor Roadshow 2026 - "The Predatory Hunt".
    
    IMPORTANT: You should ONLY answer questions about:
    1. The Scaters Raptor Roadshow 2026 events
    2. The new Raptor skateboard collection launch
    
    Do NOT answer questions about other topics, trivia, or unrelated subjects.
    If asked about something outside these topics, politely redirect to roadshow-related questions.
    
    ROADSHOW INFORMATION:
    - Event Name: "The Predatory Hunt" - Scaters Raptor Roadshow 2026
    - Prize Pool: £310,000 in total
    - Locations and Dates:
      * London - March 12, 2026 at Southbank Undercroft ("The Concrete Heart")
      * Manchester - March 19, 2026 at Projekt MCR ("The Industrial Abyss")
      * Glasgow - March 26, 2026 at Kelvingrove ("The Northern Peak")
    - Featured Pro Skaters: Lucien Clarke & Geoff Rowley
    - Mission: Engineering British Supremacy on the Pavement
    
    RAPTOR SKATEBOARD COLLECTION (5 Decks):
    1. The Eagle - Sky Dominator (Aerial dominance, for vert and air tricks)
    2. The Panther - Shadow Hunter (Technical precision, for street and technical skating)
    3. The Bull - Ground Breaker (Raw power, for aggressive skating and transitions)
    4. The Shark - Flow Machine (Speed & momentum, for bowls and carving)
    5. The Snake - Flex Assassin (Adaptive reflexes, for flexible riding styles)
    
    TARGET CUSTOMERS:
    - Professional skateboarders seeking high-performance equipment
    - Street skating enthusiasts
    - UK skateboarding community
    - Competitors in "The Predatory Hunt" challenge
    - Collectors of premium skateboard decks
    
    PURPOSE OF ROADSHOW:
    - Launch the new Raptor skateboard collection
    - Showcase British skateboarding talent
    - Create competitive skateboarding events across UK cities
    - Build community and excitement around Scaters brand
    - Crown champions and award significant prizes
    
    ACTIVITIES AT EVENTS:
    - Live skateboarding competitions
    - Pro skater demonstrations by Lucien Clarke & Geoff Rowley
    - Product testing and demos of Raptor collection
    - Meet & greet with pro skaters
    - Prize competitions
    - Registration for "The Predatory Hunt" challenge
    
    Keep responses conversational, simple, and focused on these topics only.
    """
    
    def __init__(self):
        """Initialize the chatbot with API configuration."""
        self.api_provider = None
        self.model = None
        self.chat_history = []
        
        # Try to initialize API
        self._initialize_api()
        
    def _initialize_api(self):
        """Initialize AI API (Gemini or OpenAI)."""
        # Try Gemini first
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=gemini_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.api_provider = 'gemini'
                print("✓ Connected to Google Gemini API")
                return
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}")
        
        # Try OpenAI as fallback
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key and OPENAI_AVAILABLE:
            try:
                self.model = OpenAI(api_key=openai_key)
                self.api_provider = 'openai'
                print("✓ Connected to OpenAI API")
                return
            except Exception as e:
                print(f"Failed to initialize OpenAI: {e}")
        
        # No API available
        print("\n⚠ WARNING: No AI API configured!")
        print("Please set GEMINI_API_KEY or OPENAI_API_KEY in .env file")
        print("The chatbot will use basic pattern matching only.\n")
    
    def _get_timestamp(self) -> str:
        """Get formatted timestamp."""
        return datetime.now().strftime("%H:%M:%S")
    
    def _format_message(self, text: str, is_user: bool = False) -> str:
        """Format a message with timestamp."""
        prefix = "YOU" if is_user else "BUTLER"
        timestamp = self._get_timestamp()
        return f"[{timestamp}] {prefix}: {text}"
    
    def _get_ai_response(self, user_message: str) -> Optional[str]:
        """Get AI response from configured provider with timeout handling."""
        if not self.model:
            return None
        
        try:
            if self.api_provider == 'gemini':
                # Use Gemini API with timeout protection
                import signal
                
                def timeout_handler(signum, frame):
                    raise TimeoutError("API request timed out")
                
                # Set 10 second timeout for API call
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(10)
                
                try:
                    prompt = f"{self.ROADSHOW_CONTEXT}\n\nUser: {user_message}\nButler:"
                    response = self.model.generate_content(
                        prompt,
                        generation_config={'max_output_tokens': 300, 'temperature': 0.7}
                    )
                    signal.alarm(0)  # Cancel alarm
                    return response.text
                except TimeoutError:
                    signal.alarm(0)
                    print("\n⚠ API request timed out")
                    return None
            
            elif self.api_provider == 'openai':
                # Use OpenAI API with timeout
                messages = [
                    {"role": "system", "content": self.ROADSHOW_CONTEXT},
                    {"role": "user", "content": user_message}
                ]
                response = self.model.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=300,
                    temperature=0.7,
                    timeout=10.0  # 10 second timeout
                )
                return response.choices[0].message.content
        
        except TimeoutError:
            print("\n⚠ API request timed out")
            return None
        except Exception as e:
            print(f"\n⚠ AI API Error: {e}")
            return None
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Get basic pattern-matched response when AI is unavailable."""
        msg_lower = user_message.lower()
        
        # Location queries
        if any(word in msg_lower for word in ['location', 'where', 'city', 'cities']):
            return """The Raptor Roadshow visits 3 UK cities:
• London - March 12, 2026 at Southbank Undercroft
• Manchester - March 19, 2026 at Projekt MCR  
• Glasgow - March 26, 2026 at Kelvingrove"""
        
        # Skateboard queries
        if any(word in msg_lower for word in ['skateboard', 'deck', 'raptor', 'collection']):
            return """The Raptor Collection features 5 premium decks:
• The Eagle - Sky Dominator (aerial dominance)
• The Panther - Shadow Hunter (technical precision)
• The Bull - Ground Breaker (raw power)
• The Shark - Flow Machine (speed & momentum)
• The Snake - Flex Assassin (adaptive reflexes)"""
        
        # Prize queries
        if any(word in msg_lower for word in ['prize', 'money', 'bounty', 'reward']):
            return "The Predatory Hunt features a £310,000 total prize pool across all events!"
        
        # Date queries
        if any(word in msg_lower for word in ['when', 'date', 'time']):
            return """Event dates:
• London: March 12, 2026
• Manchester: March 19, 2026
• Glasgow: March 26, 2026"""
        
        # Activities queries
        if any(word in msg_lower for word in ['activity', 'activities', 'what', 'do']):
            return """Roadshow activities include:
• Live skateboarding competitions
• Pro demonstrations by Lucien Clarke & Geoff Rowley
• Raptor collection product testing
• Meet & greet with pro skaters
• Prize competitions"""
        
        # Pro skaters
        if any(word in msg_lower for word in ['skater', 'pro', 'lucien', 'geoff', 'rowley', 'clarke']):
            return "Featured pro skaters: Lucien Clarke & Geoff Rowley will be demonstrating at all events!"
        
        # Default response
        return """I'm The Butler, here to help with information about:
• The Raptor Roadshow 2026 (locations, dates, activities)
• The Raptor skateboard collection (features, models)

What would you like to know?"""
    
    def chat(self, user_message: str) -> str:
        """Process user message and return response."""
        # Try AI response first
        response = self._get_ai_response(user_message)
        
        # Fall back to pattern matching if AI fails
        if response is None:
            response = self._get_fallback_response(user_message)
        
        # Add to history
        self.chat_history.append(('user', user_message))
        self.chat_history.append(('assistant', response))
        
        return response
    
    def run(self):
        """Run the interactive chatbot."""
        print("=" * 70)
        print("  SCATERS RAPTOR ROADSHOW 2026 - THE PREDATORY HUNT")
        print("  AI-Powered Chatbot: The Butler")
        print("=" * 70)
        print()
        print("Welcome! I'm The Butler, your AI assistant for the Raptor Roadshow.")
        print("Ask me about roadshow locations, dates, activities, or the Raptor")
        print("skateboard collection.")
        print()
        print("Commands: 'quit' or 'exit' to end chat, 'clear' to clear history")
        print("-" * 70)
        print()
        
        while True:
            try:
                # Get user input
                user_input = input(f"{self._format_message('', is_user=True).split(':')[0]}: ").strip()
                
                # Handle empty input
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print(f"\n{self._format_message('Thank you for chatting! See you at the roadshow! 🛹')}")
                    break
                
                if user_input.lower() == 'clear':
                    self.chat_history = []
                    print("\n[Chat history cleared]\n")
                    continue
                
                # Show typing indicator
                print(f"{self._format_message('', is_user=False).split(':')[0]}: ", end='', flush=True)
                print("Thinking...", end='', flush=True)
                
                # Get response
                response = self.chat(user_input)
                
                # Clear typing indicator and show response
                print("\r" + " " * 80 + "\r", end='')
                print(self._format_message(response))
                print()
                
            except KeyboardInterrupt:
                print(f"\n\n{self._format_message('Chat interrupted. Goodbye! 🛹')}")
                break
            except Exception as e:
                print(f"\n⚠ Error: {e}")
                print()


def main():
    """Main entry point."""
    chatbot = ScatersRoadshowChatbot()
    chatbot.run()


if __name__ == "__main__":
    main()
