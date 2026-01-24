#!/usr/bin/env python3
"""
Tests for Scaters Raptor Roadshow 2026 Chatbot
Tests rule-based prompting and sentiment awareness features.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Import the chatbot module
from chatbot import ScatersRoadshowChatbot


class TestChatbotRuleBasedPrompting(unittest.TestCase):
    """Test cases for rule-based prompting functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock the API initialization to avoid requiring API keys
        with patch.object(ScatersRoadshowChatbot, '_initialize_api'):
            self.chatbot = ScatersRoadshowChatbot()
            # Ensure sentiment analyzer is available for tests
            if not self.chatbot.sentiment_analyzer:
                from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
                self.chatbot.sentiment_analyzer = SentimentIntensityAnalyzer()
    
    def test_location_query_mission_brief_format(self):
        """Test that location queries return Mission Brief format response."""
        test_queries = [
            "Where is the next event?",
            "What locations are you visiting?",
            "Where will the roadshow be?",
            "What cities are hosting events?"
        ]
        
        for query in test_queries:
            with self.subTest(query=query):
                response = self.chatbot.chat(query)
                # Check for Mission Brief indicators (case-insensitive)
                self.assertIn("MISSION", response.upper())
                # Check for cities (case-insensitive)
                response_upper = response.upper()
                self.assertIn("LONDON", response_upper)
                self.assertIn("MANCHESTER", response_upper)
                self.assertIn("GLASGOW", response_upper)
                # Check for mission-style language
                self.assertTrue(
                    any(word in response.lower() for word in ['mission', 'tactical', 'battlefield']),
                    f"Response should contain mission-style language: {response}"
                )
    
    def test_safety_fear_queries_reassurance(self):
        """Test that safety/fear queries return reassurance responses."""
        test_queries = [
            "Is it safe to participate?",
            "I'm scared to try this",
            "What if I get hurt?",
            "Is this dangerous?",
            "Are there safety measures?"
        ]
        
        for query in test_queries:
            with self.subTest(query=query):
                response = self.chatbot.chat(query)
                # Check for safety reassurance
                self.assertTrue(
                    any(word in response.lower() for word in ['safe', 'safety', 'professional', 'supervised']),
                    f"Response should contain safety reassurance: {response}"
                )
                # Should mention specific safety measures
                self.assertTrue(
                    any(phrase in response.lower() for phrase in ['first aid', 'medical', 'safety equipment', 'safety protocol']),
                    f"Response should mention specific safety measures: {response}"
                )
    
    def test_prize_queries_fomo_response(self):
        """Test that prize queries create FOMO without disclosing all details."""
        test_queries = [
            "What's the prize amount?",
            "What can I win?",
            "Where is the hunting zone?",
            "What prizes are there?",
            "Tell me about the bounty"
        ]
        
        for query in test_queries:
            with self.subTest(query=query):
                response = self.chatbot.chat(query)
                # Check for FOMO language
                self.assertTrue(
                    any(word in response.lower() for word in ['exclusive', 'amazing', 'once-in-a-lifetime', 'don\'t miss']),
                    f"Response should create FOMO: {response}"
                )
                # Should mention prizes but keep some mystery
                self.assertTrue(
                    any(word in response.lower() for word in ['prize', 'reward', 'bounty', 'opportunity']),
                    f"Response should mention prizes: {response}"
                )
                # Should encourage action
                self.assertTrue(
                    any(phrase in response.lower() for phrase in ['join', 'register', 'don\'t miss out']),
                    f"Response should encourage action: {response}"
                )
    
    def test_frustration_detection_humor_response(self):
        """Test that frustration is detected and responded with humor."""
        test_queries = [
            "Why is this so complicated?",
            "This is confusing!",
            "I don't understand anything",
            "This is so frustrating",
            "Why is it so hard?"
        ]
        
        for query in test_queries:
            with self.subTest(query=query):
                response = self.chatbot.chat(query)
                # Check for humor/light-hearted tone
                self.assertTrue(
                    any(word in response.lower() for word in ['kickflip', 'whoa', 'together', 'got this']),
                    f"Response should have humor/light-hearted tone: {response}"
                )
                # Should offer help
                self.assertTrue(
                    any(word in response.lower() for word in ['help', 'clarify', 'simple', 'bugging']),
                    f"Response should offer help: {response}"
                )
    
    def test_sentiment_detection(self):
        """Test sentiment detection functionality."""
        # Positive sentiment
        positive_scores = self.chatbot._detect_sentiment("This is amazing! I love it!")
        self.assertGreater(positive_scores['compound'], 0.3, "Should detect positive sentiment")
        
        # Negative sentiment
        negative_scores = self.chatbot._detect_sentiment("This is terrible and confusing!")
        self.assertLess(negative_scores['compound'], -0.3, "Should detect negative sentiment")
        
        # Neutral sentiment
        neutral_scores = self.chatbot._detect_sentiment("What time does it start?")
        self.assertGreaterEqual(neutral_scores['compound'], -0.3)
        self.assertLessEqual(neutral_scores['compound'], 0.3)
    
    def test_rule_based_prompting_priority(self):
        """Test that rule-based prompting takes priority over AI/fallback."""
        # Location query should trigger rule-based response
        response = self.chatbot.chat("Where is the event?")
        self.assertIn("MISSION", response.upper())
        
        # Safety query should trigger rule-based response
        response = self.chatbot.chat("Is it safe?")
        self.assertTrue(any(word in response.lower() for word in ['safe', 'safety', 'professional']))
        
        # Prize query should trigger rule-based response
        response = self.chatbot.chat("What can I win?")
        self.assertTrue(any(word in response.lower() for word in ['prize', 'bounty', 'reward']))
    
    def test_multiple_keywords_in_query(self):
        """Test queries with multiple keywords still trigger correct rule."""
        # Location + safety
        response = self.chatbot.chat("Where is the event and is it safe?")
        # Should prioritize the first matching rule (location in this case)
        self.assertTrue(
            "MISSION" in response.upper() or 
            any(word in response.lower() for word in ['safe', 'safety']),
            "Should trigger one of the rules"
        )


class TestChatbotIntegration(unittest.TestCase):
    """Integration tests for the chatbot."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch.object(ScatersRoadshowChatbot, '_initialize_api'):
            self.chatbot = ScatersRoadshowChatbot()
            if not self.chatbot.sentiment_analyzer:
                from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
                self.chatbot.sentiment_analyzer = SentimentIntensityAnalyzer()
    
    def test_chat_history_stored(self):
        """Test that chat history is properly stored."""
        self.chatbot.chat("Where is the event?")
        self.assertEqual(len(self.chatbot.chat_history), 2)  # user + assistant
        self.assertEqual(self.chatbot.chat_history[0][0], 'user')
        self.assertEqual(self.chatbot.chat_history[1][0], 'assistant')
    
    def test_different_query_types(self):
        """Test different types of queries work correctly."""
        queries = [
            "Where is the roadshow?",
            "Is it safe?",
            "What prizes can I win?",
            "This is so confusing!"
        ]
        
        for query in queries:
            response = self.chatbot.chat(query)
            self.assertIsNotNone(response)
            self.assertGreater(len(response), 0)
            self.assertIsInstance(response, str)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestChatbotRuleBasedPrompting))
    suite.addTests(loader.loadTestsFromTestCase(TestChatbotIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
