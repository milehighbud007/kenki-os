#!/usr/bin/env python3
"""
KENKI OS - Voice Interface Module
Provides voice input/output for the AI assistant
"""

import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
import logging
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

# Import KENKI modules
from kenki_assist import KenkiAssistant

logger = logging.getLogger(__name__)

class KenkiVoiceInterface:
    """Voice interface for KENKI OS AI Assistant"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.assistant = KenkiAssistant(config_path)
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.is_speaking = False
        
        self._setup_voice_engine()
        self._setup_voice_commands()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load voice configuration"""
        config_file = Path(__file__).parent / config_path
        
        if not config_file.exists():
            return self._get_default_voice_config()
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('voice', self._get_default_voice_config())
        except json.JSONDecodeError:
            return self._get_default_voice_config()
    
    def _get_default_voice_config(self) -> Dict[str, Any]:
        """Return default voice configuration"""
        return {
            "enabled": True,
            "voice_id": None,
            "rate": 150,
            "volume": 0.8,
            "language": "en-US",
            "wake_word": "kenki",
            "timeout": 5,
            "energy_threshold": 4000,
            "pause_threshold": 0.8,
            "phrase_threshold": 0.3,
            "non_speaking_duration": 0.5
        }
    
    def _setup_voice_engine(self):
        """Setup text-to-speech engine"""
        try:
            # Configure voice engine
            self.engine.setProperty('rate', self.config.get('rate', 150))
            self.engine.setProperty('volume', self.config.get('volume', 0.8))
            
            # Set voice
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to find a good voice
                for voice in voices:
                    if 'en' in voice.id.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                else:
                    # Use first available voice
                    self.engine.setProperty('voice', voices[0].id)
            
            logger.info("✅ Voice engine initialized")
        except Exception as e:
            logger.error(f"Failed to initialize voice engine: {e}")
    
    def _setup_voice_commands(self):
        """Setup voice command patterns"""
        self.voice_commands = {
            'explain': ['explain', 'what is', 'how does', 'tell me about'],
            'translate': ['translate', 'convert', 'find command', 'get command'],
            'analyze': ['analyze', 'scan', 'check', 'test'],
            'help': ['help', 'what can you do', 'commands', 'options'],
            'stop': ['stop', 'quit', 'exit', 'goodbye', 'bye'],
            'clear': ['clear', 'reset', 'start over'],
            'repeat': ['repeat', 'say again', 'what did you say']
        }
    
    def speak(self, text: str, interrupt: bool = True):
        """Speak text using TTS"""
        if self.is_speaking and interrupt:
            self.engine.stop()
        
        try:
            self.is_speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS error: {e}")
        finally:
            self.is_speaking = False
    
    def speak_async(self, text: str):
        """Speak text asynchronously"""
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.daemon = True
        thread.start()
    
    def listen(self, timeout: Optional[int] = None) -> Optional[str]:
        """Listen for voice input"""
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Set recognition parameters
                self.recognizer.energy_threshold = self.config.get('energy_threshold', 4000)
                self.recognizer.pause_threshold = self.config.get('pause_threshold', 0.8)
                self.recognizer.phrase_threshold = self.config.get('phrase_threshold', 0.3)
                self.recognizer.non_speaking_duration = self.config.get('non_speaking_duration', 0.5)
                
                logger.info("🎤 Listening...")
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout or self.config.get('timeout', 5),
                    phrase_time_limit=10
                )
                
                # Recognize speech
                text = self.recognizer.recognize_google(
                    audio,
                    language=self.config.get('language', 'en-US')
                )
                
                logger.info(f"🎤 Heard: {text}")
                return text.lower()
                
        except sr.WaitTimeoutError:
            logger.info("⏰ Listening timeout")
            return None
        except sr.UnknownValueError:
            logger.info("❓ Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"🔌 Speech recognition error: {e}")
            return None
        except Exception as e:
            logger.error(f"🎤 Listening error: {e}")
            return None
    
    def process_voice_command(self, text: str) -> str:
        """Process voice command and return response"""
        if not text:
            return "I didn't hear anything. Please try again."
        
        # Check for wake word
        wake_word = self.config.get('wake_word', 'kenki').lower()
        if wake_word in text:
            # Remove wake word from command
            text = text.replace(wake_word, '').strip()
        
        # Determine command type
        command_type = self._classify_command(text)
        
        try:
            if command_type == 'explain':
                # Extract the command to explain
                command = self._extract_command(text)
                if command:
                    response = self.assistant.explain_command(command)
                else:
                    response = "Please specify what command you'd like me to explain."
            
            elif command_type == 'translate':
                # Extract the natural language request
                request = self._extract_request(text)
                if request:
                    response = self.assistant.translate_to_shell(request)
                else:
                    response = "Please tell me what you'd like me to do."
            
            elif command_type == 'analyze':
                # Extract target for analysis
                target = self._extract_target(text)
                if target:
                    response = self.assistant.analyze_security_tool(target)
                else:
                    response = "Please specify what you'd like me to analyze."
            
            elif command_type == 'help':
                response = self._get_help_text()
            
            elif command_type == 'stop':
                response = "Goodbye! Have a great day."
                self.is_listening = False
            
            elif command_type == 'clear':
                response = "Starting fresh. How can I help you?"
            
            elif command_type == 'repeat':
                response = "I'll repeat my last response."
                # This would need to store the last response
                response = "I don't have a previous response to repeat."
            
            else:
                # Default to explanation
                response = self.assistant.explain_command(text)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing voice command: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _classify_command(self, text: str) -> str:
        """Classify the type of voice command"""
        text_lower = text.lower()
        
        for command_type, keywords in self.voice_commands.items():
            if any(keyword in text_lower for keyword in keywords):
                return command_type
        
        return 'general'
    
    def _extract_command(self, text: str) -> Optional[str]:
        """Extract command from voice input"""
        # Look for quoted text or specific command patterns
        import re
        
        # Look for quoted text
        quoted = re.findall(r'"([^"]*)"', text)
        if quoted:
            return quoted[0]
        
        # Look for "command" or "tool" keywords
        command_patterns = [
            r'command\s+([a-zA-Z0-9\s\-\.\/]+)',
            r'tool\s+([a-zA-Z0-9\s\-\.\/]+)',
            r'explain\s+([a-zA-Z0-9\s\-\.\/]+)',
            r'what\s+is\s+([a-zA-Z0-9\s\-\.\/]+)',
            r'how\s+does\s+([a-zA-Z0-9\s\-\.\/]+)'
        ]
        
        for pattern in command_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_request(self, text: str) -> Optional[str]:
        """Extract natural language request from voice input"""
        # Remove common prefixes
        prefixes = ['translate', 'convert', 'find command', 'get command', 'make command']
        for prefix in prefixes:
            if text.lower().startswith(prefix):
                text = text[len(prefix):].strip()
                break
        
        return text if text else None
    
    def _extract_target(self, text: str) -> Optional[str]:
        """Extract target for analysis from voice input"""
        # Look for tool names or targets
        import re
        
        # Common security tools
        tools = [
            'nmap', 'metasploit', 'sqlmap', 'hydra', 'john', 'hashcat',
            'aircrack', 'wireshark', 'volatility', 'ghidra', 'radare2',
            'nikto', 'dirb', 'wpscan', 'joomscan', 'maltego', 'recon-ng'
        ]
        
        for tool in tools:
            if tool in text.lower():
                return tool
        
        # Look for quoted text
        quoted = re.findall(r'"([^"]*)"', text)
        if quoted:
            return quoted[0]
        
        return None
    
    def _get_help_text(self) -> str:
        """Get help text for voice commands"""
        return """
        I can help you with security testing tasks. Here are some voice commands:
        
        • "Explain nmap" - Get detailed explanation of a command
        • "Translate find open ports" - Convert to shell command
        • "Analyze metasploit" - Get tool guidance
        • "Help" - Show this help
        • "Stop" - Exit voice mode
        
        You can also ask me general questions about security tools and commands.
        """
    
    def start_voice_mode(self):
        """Start interactive voice mode"""
        self.speak("Welcome to KENKI OS voice interface. How can I help you?")
        
        self.is_listening = True
        while self.is_listening:
            try:
                # Listen for voice input
                text = self.listen()
                
                if text:
                    # Process the command
                    response = self.process_voice_command(text)
                    
                    # Speak the response
                    self.speak(response)
                    
                    # Check if we should stop
                    if 'goodbye' in response.lower() or 'stop' in response.lower():
                        break
                
                time.sleep(0.1)  # Small delay to prevent CPU overuse
                
            except KeyboardInterrupt:
                self.speak("Voice mode stopped by user.")
                break
            except Exception as e:
                logger.error(f"Voice mode error: {e}")
                self.speak("Sorry, I encountered an error. Please try again.")
    
    def voice_command(self, command: str) -> str:
        """Process a single voice command"""
        response = self.process_voice_command(command)
        return response

def main():
    """Main entry point for voice interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="KENKI OS Voice Interface - AI-powered voice commands for security testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --interactive          # Start voice mode
  %(prog)s "explain nmap"         # Process single command
  %(prog)s --test                 # Test voice recognition
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        help="Voice command to process"
    )
    
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Start interactive voice mode"
    )
    
    parser.add_argument(
        "--test",
        "-t",
        action="store_true",
        help="Test voice recognition"
    )
    
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize voice interface
    try:
        voice_interface = KenkiVoiceInterface(args.config)
    except Exception as e:
        print(f"❌ Failed to initialize voice interface: {e}")
        return 1
    
    # Handle different modes
    if args.interactive:
        voice_interface.start_voice_mode()
    elif args.test:
        print("🎤 Testing voice recognition...")
        print("Please speak something...")
        text = voice_interface.listen()
        if text:
            print(f"✅ Heard: {text}")
        else:
            print("❌ No speech detected")
    elif args.command:
        response = voice_interface.voice_command(args.command)
        print(response)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 