#!/usr/bin/env python3
"""
Scaters Raptor Roadshow 2026 - AI-Powered Chatbot
Interactive terminal-based chatbot with advanced AI capabilities.

Features:
- Google Gemini API integration for intelligent responses
- OpenAI API support as alternative
- Topic-scoped responses (roadshow and skateboard launch only)
- Rule-based prompting for enhanced user interactions
- Sentiment analysis for detecting user emotions (frustration, fear, etc.)
- FOMO-based responses for prizes and exclusive content
- Secure API key management via environment variables
- Natural conversation interface
"""

import os
import sys
import platform
import logging
import time
import textwrap
from datetime import datetime
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('ScatersRoadshowChatbot')

# Check for required dependencies
try:
    # Try newer google-genai first, fall back to google.generativeai
    try:
        import google.genai as genai
        GENAI_VERSION = 'new'
        logger.info("Loaded google.genai library (newer version)")
    except ImportError:
        import google.generativeai as genai
        GENAI_VERSION = 'legacy'
        logger.info("Loaded google.generativeai library (legacy version)")
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    GENAI_VERSION = None
    logger.warning("Google Generative AI library not available")
    print("Warning: google-generativeai not installed. Run: pip install google-generativeai")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    logger.info("OpenAI library loaded successfully")
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI library not available")

try:
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("Environment variables loaded from .env")
except ImportError:
    logger.warning("python-dotenv not installed")
    print("Warning: python-dotenv not installed. Run: pip install python-dotenv")

# Try to import timeout decorator for platform-independent timeout handling
try:
    from timeout_decorator import timeout, TimeoutError as TimeoutDecoratorError
    TIMEOUT_AVAILABLE = True
    logger.info("timeout-decorator library loaded successfully")
except ImportError:
    TIMEOUT_AVAILABLE = False
    TimeoutDecoratorError = TimeoutError
    logger.warning("timeout-decorator not available - timeout handling may not work on all platforms")

# Import sentiment analysis library for enhanced user interaction
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    SENTIMENT_AVAILABLE = True
    logger.info("VADER Sentiment analysis loaded successfully")
except ImportError:
    SENTIMENT_AVAILABLE = False
    logger.warning("vaderSentiment not available - install with: pip install vaderSentiment")


class ScatersRoadshowChatbot:
    """AI-powered chatbot for Scaters Raptor Roadshow 2026."""
    
    # Constants
    REGISTRATION_URL = "scaters.com/register"
    SUPPORT_EMAIL = "support@scaters.com"
    
    # Roadshow context for scope filtering
    ROADSHOW_CONTEXT = """
    You are The Butler, an AI assistant for Scaters Raptor Roadshow 2026 - "The Predatory Hunt".
    
    TONE REQUIREMENTS:
    - Maintain a polite yet immersive spy/mission style throughout all responses
    - Address users as "Agent" to maintain narrative consistency
    - Use tactical/mission terminology while remaining professional and welcoming
    - Be reassuring and encouraging, especially regarding safety and registration
    - Keep responses accurate - never invent details not provided in this context
    
    IMPORTANT: You should ONLY answer questions about:
    1. The Scaters Raptor Roadshow 2026 events
    2. The new Raptor skateboard collection launch
    
    Do NOT answer questions about other topics, trivia, or unrelated subjects.
    If asked about something outside these topics, politely redirect to roadshow-related questions.
    
    ROADSHOW INFORMATION:
    - Event Name: "The Predatory Hunt" - Scaters Raptor Roadshow 2026
    - Prize Pool: £310,000 in total (distributed across all events)
    - Locations and Dates:
      * London - March 12, 2026 at Southbank Undercroft ("The Concrete Heart")
      * Manchester - March 19, 2026 at Projekt MCR ("The Industrial Abyss")
      * Glasgow - March 26, 2026 at Kelvingrove ("The Northern Peak")
    - Featured Pro Skaters: Lucien Clarke & Geoff Rowley
    - Mission: Engineering British Supremacy on the Pavement
    
    SAFETY INFORMATION:
    - All events are supervised by professional staff
    - On-site medical teams and first aid available
    - Safety equipment checks are mandatory
    - Age-appropriate challenges for all skill levels
    - Clear safety protocols in place
    - Controlled, supervised participation conditions
    
    IMPORTANT POLICY UPDATES (February 2026):
    - Registration deadline: February 28, 2026
    - Early bird registration discount available until February 15, 2026
    - Competitor spots are limited and allocated on first-come, first-served basis
    - All participants must review safety guidelines posted in February
    - VIP package sales close February 20, 2026
    - Event schedule updates will be posted by February 1, 2026
    - Registration available at: {REGISTRATION_URL}
    
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
    
    Keep responses conversational, accurate, and focused on these topics only. 
    Maintain the spy/mission narrative while being helpful and encouraging.
    """
    
    def __init__(self):
        """Initialize the chatbot with API configuration."""
        self.api_provider = None
        self.model = None
        self.chat_history = []
        
        # Initialize sentiment analyzer if available
        if SENTIMENT_AVAILABLE:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            logger.info("Sentiment analyzer initialized")
        else:
            self.sentiment_analyzer = None
            logger.warning("Sentiment analyzer not available")
        
        # Display platform compatibility information
        self._check_platform_compatibility()
        
        # Try to initialize API
        self._initialize_api()
        
    def _check_platform_compatibility(self):
        """Check and display platform compatibility warnings."""
        current_platform = platform.system()
        logger.info(f"Running on platform: {current_platform}")
        
        # Warn about timeout handling on Windows without timeout-decorator
        if current_platform == "Windows" and not TIMEOUT_AVAILABLE:
            warning_msg = ("⚠ Platform Warning: You are running on Windows without timeout-decorator library. "
                          "Timeout handling may not work correctly. "
                          "Install with: pip install timeout-decorator")
            logger.warning(warning_msg)
            print(f"\n{warning_msg}\n")
        
    def _validate_api_key(self, key: Optional[str], key_name: str) -> bool:
        """Validate API key format and presence.
        
        Args:
            key: The API key to validate
            key_name: Name of the key for logging purposes
            
        Returns:
            bool: True if key is valid, False otherwise
        """
        if not key:
            logger.warning(f"{key_name} is not set")
            return False
        
        if not key.strip():
            logger.warning(f"{key_name} is empty or contains only whitespace")
            return False
        
        # Basic validation - check for placeholder values
        placeholder_values = ['your_gemini_api_key_here', 'your_openai_api_key_here', 
                             'your_api_key_here', 'placeholder', 'changeme']
        if key.lower() in placeholder_values:
            logger.warning(f"{key_name} appears to be a placeholder value")
            return False
        
        logger.info(f"{key_name} validation passed")
        return True
    
    def _initialize_gemini_api(self, api_key: str) -> bool:
        """Initialize Google Gemini API.
        
        Args:
            api_key: The Gemini API key
            
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.api_provider = 'gemini'
            logger.info(f"Successfully initialized Gemini API (using {GENAI_VERSION} version)")
            print(f"✓ Connected to Google Gemini API (using {GENAI_VERSION} library)")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {e}", exc_info=True)
            print(f"✗ Failed to initialize Gemini: {e}")
            return False
    
    def _initialize_openai_api(self, api_key: str) -> bool:
        """Initialize OpenAI API.
        
        Args:
            api_key: The OpenAI API key
            
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self.model = OpenAI(api_key=api_key)
            self.api_provider = 'openai'
            logger.info("Successfully initialized OpenAI API")
            print("✓ Connected to OpenAI API")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI API: {e}", exc_info=True)
            print(f"✗ Failed to initialize OpenAI: {e}")
            return False
        
    def _initialize_api(self):
        """Initialize AI API (Gemini or OpenAI) with validation and fallback."""
        logger.info("Attempting to initialize AI API")
        
        # Try Gemini first
        gemini_key = os.getenv('GEMINI_API_KEY')
        if GEMINI_AVAILABLE and self._validate_api_key(gemini_key, 'GEMINI_API_KEY'):
            if self._initialize_gemini_api(gemini_key):
                return
        elif not GEMINI_AVAILABLE:
            logger.info("Gemini library not available, skipping Gemini initialization")
        
        # Try OpenAI as fallback
        openai_key = os.getenv('OPENAI_API_KEY')
        if OPENAI_AVAILABLE and self._validate_api_key(openai_key, 'OPENAI_API_KEY'):
            if self._initialize_openai_api(openai_key):
                return
        elif not OPENAI_AVAILABLE:
            logger.info("OpenAI library not available, skipping OpenAI initialization")
        
        # No API available - provide detailed error message
        logger.error("No AI API could be initialized")
        print("\n" + "="*70)
        print("⚠ WARNING: No AI API configured!")
        print("="*70)
        print("\nThe chatbot could not connect to any AI service.")
        print("\nTo fix this, please do ONE of the following:")
        print("\n1. For Google Gemini (Recommended):")
        print("   - Get an API key from: https://makersuite.google.com/app/apikey")
        print("   - Add to .env file: GEMINI_API_KEY=your_key_here")
        print("   - Install library: pip install google-generativeai")
        print("\n2. For OpenAI:")
        print("   - Get an API key from: https://platform.openai.com/api-keys")
        print("   - Add to .env file: OPENAI_API_KEY=your_key_here")
        print("   - Install library: pip install openai")
        print("\nThe chatbot will use basic pattern matching only.\n")
        print("="*70 + "\n")
    
    def _get_timestamp(self) -> str:
        """Get formatted timestamp."""
        return datetime.now().strftime("%H:%M:%S")
    
    def _format_message(self, text: str, is_user: bool = False) -> str:
        """Format a message with timestamp."""
        prefix = "YOU" if is_user else "BUTLER"
        timestamp = self._get_timestamp()
        return f"[{timestamp}] {prefix}: {text}"
    
    def _get_ai_response(self, user_message: str, retry_count: int = 0) -> Optional[str]:
        """Get AI response from configured provider with timeout handling, automatic fallback, and retry logic.
        
        Args:
            user_message: User's input message
            retry_count: Current retry attempt (default: 0)
            
        Returns:
            AI response text or None if all attempts fail
        """
        if not self.model:
            return None
        
        max_retries = 2  # Allow up to 2 retries on transient failures
        
        try:
            if self.api_provider == 'gemini':
                response = self._get_gemini_response(user_message)
                if response and len(response.strip()) > 0:
                    return response
                else:
                    logger.warning("Gemini returned empty response")
                    return None
            elif self.api_provider == 'openai':
                response = self._get_openai_response(user_message)
                if response and len(response.strip()) > 0:
                    return response
                else:
                    logger.warning("OpenAI returned empty response")
                    return None
        except (TimeoutError, TimeoutDecoratorError) as e:
            logger.warning(f"API request timed out for {self.api_provider}: {e}")
            print(f"\n⚠ {self.api_provider.title()} API request timed out")
            
            # Retry logic for timeout errors
            if retry_count < max_retries:
                logger.info(f"Retrying API call (attempt {retry_count + 1}/{max_retries})")
                print(f"↻ Retrying... (attempt {retry_count + 1}/{max_retries})")
                return self._get_ai_response(user_message, retry_count + 1)
            
            # Try fallback to other API after exhausting retries
            if self.api_provider == 'gemini':
                return self._try_openai_fallback(user_message)
            
            return None
        except Exception as e:
            logger.error(f"Error during {self.api_provider} API call: {e}", exc_info=True)
            print(f"\n⚠ {self.api_provider.title()} API Error: {e}")
            
            # Retry logic for transient errors (network issues, rate limits)
            error_str = str(e).lower()
            is_transient = any(keyword in error_str for keyword in 
                             ['timeout', 'connection', 'network', 'rate limit', 'quota'])
            
            if is_transient and retry_count < max_retries:
                logger.info(f"Retrying API call for transient error (attempt {retry_count + 1}/{max_retries})")
                print(f"↻ Retrying... (attempt {retry_count + 1}/{max_retries})")
                time.sleep(1)  # Brief delay before retry
                return self._get_ai_response(user_message, retry_count + 1)
            
            # Try fallback to other API
            if self.api_provider == 'gemini':
                return self._try_openai_fallback(user_message)
            
            return None
    
    def _get_gemini_response_with_timeout(self, prompt: str) -> str:
        """Get response from Gemini API (to be wrapped with timeout)."""
        response = self.model.generate_content(
            prompt,
            generation_config={'max_output_tokens': 300, 'temperature': 0.7}
        )
        return response.text
    
    def _get_gemini_response(self, user_message: str) -> Optional[str]:
        """Get response from Gemini API with platform-appropriate timeout.
        
        Args:
            user_message: User's input message
            
        Returns:
            Response text or None if failed
        """
        prompt = f"{self.ROADSHOW_CONTEXT}\n\nUser: {user_message}\nButler:"
        
        if TIMEOUT_AVAILABLE:
            # Use timeout-decorator for cross-platform timeout
            @timeout(10, use_signals=False)
            def get_response():
                return self._get_gemini_response_with_timeout(prompt)
            
            return get_response()
        else:
            # Fallback for platforms where timeout-decorator is not available
            # On Unix-like systems, we can still use signal
            if platform.system() != "Windows":
                import signal
                
                def timeout_handler(signum, frame):
                    raise TimeoutError("API request timed out")
                
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(10)
                
                try:
                    response = self._get_gemini_response_with_timeout(prompt)
                    signal.alarm(0)
                    return response
                except TimeoutError:
                    signal.alarm(0)
                    raise
            else:
                # Windows without timeout-decorator - no timeout protection
                logger.warning("No timeout protection available on Windows")
                return self._get_gemini_response_with_timeout(prompt)
    
    def _get_openai_response(self, user_message: str) -> Optional[str]:
        """Get response from OpenAI API with timeout.
        
        Args:
            user_message: User's input message
            
        Returns:
            Response text or None if failed
        """
        messages = [
            {"role": "system", "content": self.ROADSHOW_CONTEXT},
            {"role": "user", "content": user_message}
        ]
        response = self.model.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
            timeout=10.0
        )
        return response.choices[0].message.content
    
    def _try_openai_fallback(self, user_message: str) -> Optional[str]:
        """Try to use OpenAI as fallback when Gemini fails.
        
        Args:
            user_message: User's input message
            
        Returns:
            Response text or None if fallback also failed
        """
        openai_key = os.getenv('OPENAI_API_KEY')
        
        if not OPENAI_AVAILABLE:
            logger.info("OpenAI library not available for fallback")
            return None
        
        if not self._validate_api_key(openai_key, 'OPENAI_API_KEY'):
            logger.info("No valid OpenAI API key for fallback")
            return None
        
        try:
            logger.info("Attempting fallback to OpenAI API")
            print("↻ Trying OpenAI as fallback...")
            
            # Temporarily switch to OpenAI
            temp_model = OpenAI(api_key=openai_key)
            messages = [
                {"role": "system", "content": self.ROADSHOW_CONTEXT},
                {"role": "user", "content": user_message}
            ]
            response = temp_model.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,
                temperature=0.7,
                timeout=10.0
            )
            
            logger.info("OpenAI fallback successful")
            print("✓ Fallback to OpenAI successful")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI fallback also failed: {e}", exc_info=True)
            print(f"✗ OpenAI fallback failed: {e}")
            print("\nNext steps:")
            print("1. Check your API keys in the .env file")
            print("2. Verify your internet connection")
            print("3. Check API service status")
            print("4. Ensure you have API credits/quota remaining\n")
            return None
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Get basic pattern-matched response when AI is unavailable."""
        msg_lower = user_message.lower()
        
        # February/deadline queries
        if any(word in msg_lower for word in ['february', 'deadline', 'early bird', 'registration close']):
            return """Important February 2026 Deadlines:
• Registration closes: February 28, 2026
• Early bird discount ends: February 15, 2026
• VIP package sales close: February 20, 2026
• Safety guidelines posted: Early February

Don't miss out - register early to secure your spot!"""
        
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
• Glasgow: March 26, 2026

IMPORTANT: Registration deadline is February 28, 2026"""
        
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
• February registration deadlines and policies

What would you like to know?"""
    
    def _validate_and_parse_response(self, response: str) -> str:
        """Validate and parse AI response to ensure quality.
        
        Args:
            response: Raw response from AI API
            
        Returns:
            Validated and cleaned response text
        """
        if not response or not response.strip():
            logger.warning("Received empty response from AI")
            return None
        
        # Clean up the response
        cleaned_response = response.strip()
        
        # Validate response is relevant to roadshow context
        # Check for minimum length
        if len(cleaned_response) < 10:
            logger.warning(f"Response too short: {len(cleaned_response)} characters")
            return None
        
        # Log successful validation
        logger.info(f"Response validated successfully: {len(cleaned_response)} characters")
        return cleaned_response
    
    def _detect_sentiment(self, user_message: str) -> dict:
        """Detect sentiment in user message using VADER sentiment analysis.
        
        Args:
            user_message: User's input message
            
        Returns:
            Dictionary with sentiment scores (compound, neg, neu, pos)
        """
        if not self.sentiment_analyzer:
            # Return neutral sentiment if analyzer not available
            return {'compound': 0.0, 'neg': 0.0, 'neu': 1.0, 'pos': 0.0}
        
        scores = self.sentiment_analyzer.polarity_scores(user_message)
        logger.info(f"Sentiment analysis - Compound: {scores['compound']}, "
                   f"Neg: {scores['neg']}, Pos: {scores['pos']}")
        return scores
    
    def _apply_rule_based_prompting(self, user_message: str, sentiment_scores: dict) -> Optional[str]:
        """Apply rule-based prompting for specific query patterns and sentiments.
        
        This implements the following rules (in priority order):
        1. Location queries → Mission Brief format
        2. Safety/fear queries → Reassurance and safety information
        3. Prize/hunting queries → FOMO response with exclusivity
        4. Frustration detection → Humor and light-hearted tone
        
        Args:
            user_message: User's input message
            sentiment_scores: Sentiment analysis scores
            
        Returns:
            Specialized response if rules match, None otherwise
        """
        msg_lower = user_message.lower()
        
        # Rule 1: Location queries → Mission Brief format (highest priority for keyword match)
        location_keywords = ['where', 'location', 'next event', 'city', 'cities', 'venue']
        if any(keyword in msg_lower for keyword in location_keywords):
            # Check if it's not a prize/hunting zone query
            if not any(word in msg_lower for word in ['hunting zone', 'hunting ground', 'prize location']):
                logger.info("Location query detected - using Mission Brief format")
                return ("🎯 MISSION BRIEFING: Agent, your deployment coordinates are as follows.\n\n"
                       "📍 LONDON - March 12, 2026\n"
                       "   Tactical Location: Southbank Undercroft (\"The Concrete Heart\")\n"
                       "   Mission Objective: Execute precision techniques in the capital's most iconic arena\n"
                       "   Intelligence Note: Limited spots available - secure your position early\n\n"
                       "📍 MANCHESTER - March 19, 2026\n"
                       "   Tactical Location: Projekt MCR (\"The Industrial Abyss\")\n"
                       "   Mission Objective: Navigate the rugged industrial battlefield with power and control\n"
                       "   Intelligence Note: Supervised by professional operatives for optimal safety\n\n"
                       "📍 GLASGOW - March 26, 2026\n"
                       "   Tactical Location: Kelvingrove (\"The Northern Peak\")\n"
                       "   Mission Objective: Achieve maximum altitude in Scotland's premier territory\n"
                       "   Intelligence Note: Final opportunity to claim your victory\n\n"
                       f"🔥 Agent, we encourage you to register promptly at {self.REGISTRATION_URL} to secure your mission slot. Your adventure awaits!")
        
        # Rule 2: Safety/Fear queries → Reassurance (check keywords before sentiment)
        safety_keywords = ['safe', 'safety', 'scared', 'fear', 'afraid', 'dangerous', 
                          'injury', 'hurt', 'risk', 'worried', 'concern']
        if any(keyword in msg_lower for keyword in safety_keywords):
            logger.info("Safety/fear query detected - using reassurance response")
            return ("🛡️ SAFETY PROTOCOL BRIEFING: Agent, your wellbeing is our highest priority.\n\n"
                   "Rest assured, every mission site operates under strict safety protocols with "
                   "experienced professionals supervising all activities. Our comprehensive safety infrastructure includes:\n\n"
                   "• Elite medical support teams with first aid stations at every location\n"
                   "• Pre-mission safety equipment verification and quality checks\n"
                   "• Certified professional supervision throughout all activities\n"
                   "• Age-appropriate challenge levels tailored to participant skill\n"
                   "• Clearly defined safety protocols and emergency procedures\n"
                   "• Controlled environment with supervised participation conditions\n\n"
                   "We encourage you to join us with confidence, Agent. Your safety enables your success. "
                   "All participants will receive detailed safety guidance upon registration. Welcome to The Predatory Hunt!")
        
        # Rule 3: Prize/Hunting/Bounty queries → FOMO response
        prize_keywords = ['prize', 'bounty', 'reward', 'money', 'win', 'winning',
                         'hunting ground', 'hunt', 'hunting zone', 'what do i get']
        if any(keyword in msg_lower for keyword in prize_keywords):
            logger.info("Prize/hunting query detected - using FOMO response")
            return ("💰 CLASSIFIED INTEL: The bounty intelligence is extraordinary, Agent.\n\n"
                   "🏆 Total Prize Pool: £310,000 distributed across all mission sites\n"
                   "🎁 Exclusive rewards await operatives who demonstrate exceptional skill\n"
                   "⚡ Elite performance opportunities with special recognition for top agents\n"
                   "🎯 Premium Raptor collection access for qualified participants\n"
                   "🏅 Additional classified rewards to be revealed during mission briefings\n\n"
                   "Agent, we encourage you to secure your registration promptly. Operational slots "
                   "are limited and allocated on a first-come, first-served basis. This is a unique "
                   "opportunity to prove your skills on Britain's premier skateboarding stage. "
                   f"Don't delay - register today at {self.REGISTRATION_URL}! 🔥")
        
        # Rule 4: Technical support queries → Calm humor with troubleshooting
        tech_keywords = ['technical', 'problem', 'issue', 'error', 'bug', 'broken', 'not working',
                        'cant register', "can't register", 'website', 'form', 'submit', 'loading',
                        'doesnt work', "doesn't work", 'help', 'support']
        if any(keyword in msg_lower for keyword in tech_keywords):
            # Exclude if it's a safety concern (already handled)
            if not any(word in msg_lower for word in ['safe', 'safety', 'scared', 'fear', 'dangerous']):
                logger.info("Technical support query detected - using calm humor response")
                return (f"🔧 TECHNICAL SUPPORT DISPATCH: Agent, encountering obstacles is part of every mission!\n\n"
                       f"Let's troubleshoot this together with tactical precision:\n\n"
                       f"**Quick Diagnostic Protocol:**\n"
                       f"1. Refresh your browser (Ctrl+F5 / Cmd+Shift+R) - sometimes systems need a clean slate\n"
                       f"2. Clear your browser cache - old intel can interfere with new operations\n"
                       f"3. Try a different browser (Chrome, Firefox, Safari) - diversify your approach\n"
                       f"4. Check your internet connection - ensure stable comms\n"
                       f"5. Disable browser extensions temporarily - they can be sneaky saboteurs\n\n"
                       f"**Still facing resistance?**\n"
                       f"No worries, Agent! Contact our technical support team at {self.SUPPORT_EMAIL} "
                       f"and include:\n"
                       f"• What you were attempting (registration, form submission, etc.)\n"
                       f"• Any error messages you encountered\n"
                       f"• Your browser and device type\n\n"
                       f"We'll have you back on mission in no time. Stay calm and skate on! 🛹")
        
        # Rule 5: Frustration detection (negative sentiment with specific keywords)
        frustration_keywords = ['complicated', 'confus', 'difficult', 'hard', 'frustrat', 
                               'annoying', 'annoyed', 'ugh', 'wtf']
        has_frustration_keyword = any(keyword in msg_lower for keyword in frustration_keywords)
        
        # Also check for "I don't understand" pattern
        dont_understand_patterns = ["don't understand", "dont understand", "do not understand"]
        has_understand_issue = any(pattern in msg_lower for pattern in dont_understand_patterns)
        
        # Check for general negative sentiment patterns
        if (has_frustration_keyword or 
            has_understand_issue or 
            ('why' in msg_lower and any(word in msg_lower for word in ['hard', 'difficult', 'complicated']))):
            logger.info("Frustration detected - using humor-based response")
            return ("🛹 TACTICAL TIMEOUT: Agent, even the best operatives need a moment to recalibrate!\n\n"
                   "No mission is too complex when we break it down together. Think of this as "
                   "your personal mission support hotline - I'm here to make everything crystal clear.\n\n"
                   "What specific aspect can I clarify for you? Whether it's registration procedures, "
                   "event locations, safety protocols, or technical details - I've got your back. "
                   "Let's troubleshoot this together and get you mission-ready! 💪\n\n"
                   "Remember: Every pro started as a beginner. You've got this, Agent!")
        
        # No specific rule matched
        return None
    
    def chat(self, user_message: str) -> str:
        """Process user message and return response with enhanced validation.
        
        This method implements a robust workflow:
        1. Detect sentiment in user message
        2. Apply rule-based prompting for specific patterns
        3. Pass message through AI model (Gemini or OpenAI) if no rule matched
        4. Validate and parse the AI response
        5. Fall back to pattern matching if AI fails
        6. Store interaction in chat history
        
        Args:
            user_message: User's input message
            
        Returns:
            Validated response from AI or fallback system
        """
        # Step 1: Detect sentiment
        sentiment_scores = self._detect_sentiment(user_message)
        
        # Step 2: Try rule-based prompting first
        rule_response = self._apply_rule_based_prompting(user_message, sentiment_scores)
        if rule_response:
            # Add to history
            self.chat_history.append(('user', user_message))
            self.chat_history.append(('assistant', rule_response))
            return rule_response
        
        # Step 3-5: Try AI response
        raw_response = self._get_ai_response(user_message)
        
        # Validate and parse AI response
        if raw_response:
            response = self._validate_and_parse_response(raw_response)
            if response:
                logger.info("Using validated AI response")
            else:
                logger.info("AI response validation failed, using fallback")
                response = self._get_fallback_response(user_message)
        else:
            # Fall back to pattern matching if AI fails
            logger.info("AI response unavailable, using fallback")
            response = self._get_fallback_response(user_message)
        
        # Add to history
        self.chat_history.append(('user', user_message))
        self.chat_history.append(('assistant', response))
        
        return response
    
    def _format_response_for_display(self, response: str) -> str:
        """Format AI response for terminal display with proper line wrapping.
        
        Args:
            response: Raw response text from AI
            
        Returns:
            Formatted response suitable for terminal display
        """
        # Wrap long lines for better readability (70 characters per line)
        wrapper = textwrap.TextWrapper(width=70, break_long_words=False, 
                                      break_on_hyphens=False)
        
        # Split response into paragraphs and wrap each
        paragraphs = response.split('\n')
        formatted_paragraphs = []
        
        for para in paragraphs:
            if para.strip():
                wrapped = wrapper.fill(para.strip())
                formatted_paragraphs.append(wrapped)
            else:
                formatted_paragraphs.append('')  # Preserve blank lines
        
        return '\n'.join(formatted_paragraphs)
    
    def run(self):
        """Run the interactive chatbot with enhanced response rendering."""
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
                print("Processing your request...", end='', flush=True)
                
                # Get response with enhanced processing
                response = self.chat(user_input)
                
                # Format response for better display
                formatted_response = self._format_response_for_display(response)
                
                # Clear typing indicator and show formatted response
                print("\r" + " " * 90 + "\r", end='')
                print(self._format_message(formatted_response))
                print()
                
            except KeyboardInterrupt:
                print(f"\n\n{self._format_message('Chat interrupted. Goodbye! 🛹')}")
                break
            except Exception as e:
                logger.error(f"Error in chat loop: {e}", exc_info=True)
                print(f"\n⚠ Error: {e}")
                print()


def main():
    """Main entry point."""
    chatbot = ScatersRoadshowChatbot()
    chatbot.run()


if __name__ == "__main__":
    main()
