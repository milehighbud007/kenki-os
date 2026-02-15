#!/usr/bin/env python3
"""
KENKI OS AI Assistant - Main CLI Interface
Integrates Claude 4 and local LLM for security tool assistance
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# AI imports
try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    print("⚠️  Claude SDK not installed. Install with: pip install anthropic")

try:
    from llama_cpp import Llama
    LLAMA_AVAILABLE = True
except ImportError:
    LLAMA_AVAILABLE = False
    print("⚠️  Llama.cpp not installed. Install with: pip install llama-cpp-python")

# Local imports
from explain import CommandExplainer
from translate import ShellTranslator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KenkiAssistant:
    """Main AI assistant for KENKI OS"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.claude_client = None
        self.local_llm = None
        self.explainer = None
        self.translator = None
        
        self._setup_ai_clients()
        self._setup_modules()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        config_file = Path(__file__).parent / config_path
        
        if not config_file.exists():
            logger.warning(f"Config file {config_path} not found. Using defaults.")
            return self._get_default_config()
        
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "anthropic_api_key": "",
            "openai_api_key": "",
            "local_llm": {
                "enabled": False,
                "model_path": "models/mistral.gguf",
                "endpoint": "http://localhost:11434"
            },
            "preferences": {
                "default_model": "claude",
                "max_tokens": 1000,
                "temperature": 0.7
            }
        }
    
    def _setup_ai_clients(self):
        """Initialize AI clients (Claude and local LLM)"""
        # Setup Claude
        if CLAUDE_AVAILABLE and self.config.get("anthropic_api_key"):
            try:
                self.claude_client = anthropic.Anthropic(
                    api_key=self.config["anthropic_api_key"]
                )
                logger.info("✅ Claude client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Claude: {e}")
        
        # Setup local LLM
        if LLAMA_AVAILABLE and self.config["local_llm"]["enabled"]:
            try:
                model_path = self.config["local_llm"]["model_path"]
                if os.path.exists(model_path):
                    self.local_llm = Llama(
                        model_path=model_path,
                        n_ctx=2048,
                        n_threads=4
                    )
                    logger.info("✅ Local LLM initialized")
                else:
                    logger.warning(f"Local model not found: {model_path}")
            except Exception as e:
                logger.error(f"Failed to initialize local LLM: {e}")
    
    def _setup_modules(self):
        """Initialize specialized modules"""
        self.explainer = CommandExplainer(self.claude_client, self.local_llm)
        self.translator = ShellTranslator(self.claude_client, self.local_llm)
    
    def explain_command(self, command: str) -> str:
        """Explain a Linux/security command"""
        if not command.strip():
            return "❌ Please provide a command to explain."
        
        try:
            explanation = self.explainer.explain(command)
            return self._format_response("Command Explanation", explanation, command)
        except Exception as e:
            logger.error(f"Error explaining command: {e}")
            return f"❌ Error explaining command: {e}"
    
    def translate_to_shell(self, natural_language: str) -> str:
        """Translate natural language to shell commands"""
        if not natural_language.strip():
            return "❌ Please provide a description of what you want to do."
        
        try:
            shell_command = self.translator.translate(natural_language)
            return self._format_response("Shell Translation", shell_command, natural_language)
        except Exception as e:
            logger.error(f"Error translating to shell: {e}")
            return f"❌ Error translating to shell: {e}"
    
    def analyze_security_tool(self, tool_name: str, context: str = "") -> str:
        """Get guidance on using security tools"""
        prompt = f"""
        Provide a comprehensive guide for using {tool_name} in ethical hacking and security testing.
        
        Include:
        1. Basic usage examples
        2. Common parameters and flags
        3. Security best practices
        4. Legal considerations
        5. Real-world use cases
        
        Context: {context}
        """
        
        try:
            response = self._get_ai_response(prompt)
            return self._format_response("Security Tool Guide", response, tool_name)
        except Exception as e:
            logger.error(f"Error analyzing security tool: {e}")
            return f"❌ Error analyzing security tool: {e}"
    
    def analyze_log_file(self, log_path: str) -> str:
        """Analyze a log file for security insights"""
        if not os.path.exists(log_path):
            return f"❌ Log file not found: {log_path}"
        
        try:
            with open(log_path, 'r') as f:
                log_content = f.read()[:5000]  # Limit content size
            
            prompt = f"""
            Analyze this log file for security insights, anomalies, and potential threats:
            
            {log_content}
            
            Provide:
            1. Summary of log contents
            2. Potential security issues
            3. Recommended actions
            4. Tools to investigate further
            """
            
            response = self._get_ai_response(prompt)
            return self._format_response("Log Analysis", response, log_path)
        except Exception as e:
            logger.error(f"Error analyzing log file: {e}")
            return f"❌ Error analyzing log file: {e}"
    
    def _get_ai_response(self, prompt: str) -> str:
        """Get response from available AI models"""
        # Try Claude first
        if self.claude_client:
            try:
                response = self.claude_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=self.config["preferences"]["max_tokens"],
                    temperature=self.config["preferences"]["temperature"],
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            except Exception as e:
                logger.warning(f"Claude failed: {e}")
        
        # Fallback to local LLM
        if self.local_llm:
            try:
                response = self.local_llm(
                    prompt,
                    max_tokens=self.config["preferences"]["max_tokens"],
                    temperature=self.config["preferences"]["temperature"],
                    stop=["\n\n", "Human:", "Assistant:"]
                )
                return response["choices"][0]["text"]
            except Exception as e:
                logger.warning(f"Local LLM failed: {e}")
        
        return "❌ No AI models available. Please check your configuration."
    
    def _format_response(self, title: str, content: str, original_input: str) -> str:
        """Format the response with KENKI branding"""
        border = "=" * 60
        return f"""
{border}
🧠 KENKI OS AI Assistant - {title}
{border}

📝 Input: {original_input}

💡 Response:
{content}

{border}
"""
    
    def interactive_mode(self):
        """Start interactive mode"""
        print("🧠 KENKI OS AI Assistant - Interactive Mode")
        print("Type 'help' for commands, 'quit' to exit")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n🔍 KENKI> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                # Auto-detect command type
                if user_input.startswith(('explain', 'what', 'how', 'why')):
                    response = self.explain_command(user_input)
                elif any(word in user_input.lower() for word in ['find', 'scan', 'check', 'analyze', 'get']):
                    response = self.translate_to_shell(user_input)
                else:
                    # Default to explanation
                    response = self.explain_command(user_input)
                
                print(response)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _show_help(self):
        """Show help information"""
        help_text = """
Available Commands:
- explain <command>     : Explain a Linux/security command
- translate <request>   : Convert natural language to shell commands
- analyze <tool>       : Get guidance on security tools
- log <file>          : Analyze a log file
- help                : Show this help
- quit                : Exit interactive mode

Examples:
- explain "nmap -sS -p 80 target.com"
- translate "find all open ports on this network"
- analyze "metasploit"
- log "/var/log/auth.log"
        """
        print(help_text)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="KENKI OS AI Assistant - Security tool guidance powered by Claude 4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "explain nmap -sS -p 80 target.com"
  %(prog)s "translate find all open ports on 192.168.1.0/24"
  %(prog)s --analyze metasploit
  %(prog)s --log /var/log/auth.log
  %(prog)s --interactive
        """
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="Natural language query or command to explain"
    )
    
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to configuration file (default: config.json)"
    )
    
    parser.add_argument(
        "--analyze",
        metavar="TOOL",
        help="Analyze a specific security tool"
    )
    
    parser.add_argument(
        "--log",
        metavar="FILE",
        help="Analyze a log file"
    )
    
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Start interactive mode"
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
    
    # Initialize assistant
    try:
        assistant = KenkiAssistant(args.config)
    except Exception as e:
        print(f"❌ Failed to initialize assistant: {e}")
        sys.exit(1)
    
    # Handle different modes
    if args.interactive:
        assistant.interactive_mode()
    elif args.analyze:
        response = assistant.analyze_security_tool(args.analyze)
        print(response)
    elif args.log:
        response = assistant.analyze_log_file(args.log)
        print(response)
    elif args.query:
        # Auto-detect query type
        query = args.query.lower()
        if query.startswith(('explain', 'what', 'how', 'why')):
            response = assistant.explain_command(args.query)
        elif any(word in query for word in ['find', 'scan', 'check', 'analyze', 'get']):
            response = assistant.translate_to_shell(args.query)
        else:
            response = assistant.explain_command(args.query)
        print(response)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 