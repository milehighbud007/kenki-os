#!/bin/bash
# KENKI OS First Run Script
# Automatically launched after boot to welcome users and guide setup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# KENKI OS Banner
echo -e "${PURPLE}"
cat << "EOF"
 ██ ▄█▀▄▄▄█████▓ ▒█████   ██ ▄█▀ ██▓ ██▓    
 ██▄█▒ ▓  ██▒ ▓▒▒██▒  ██▒ ██▄█▒ ▓██▒▓██▒    
▓███▄░ ▒ ▓██░ ▒░▒██░  ██▒▓███▄░ ▒██▒▒██░    
▓██ █▄ ░ ▓██▓ ░ ▒██   ██░▓██ █▄ ░██░▒██░    
▒██▒ █▄░ ▒██▒ ░ ░ ████▓▒░▒██▒ █▄░██░░██████▒
▒ ▒▒ ▓▒ ░ ▒ ░░   ░ ▒░▒░▒░ ▒ ▒▒ ▓▒░▓  ░ ▒░▓  ░
░ ░▒ ▒░ ░ ░      ░ ▒ ▒ ▒░ ░ ░▒ ▒░ ▒ ░░ ░ ▒  ░
░ ░░ ░  ░ ░    ░ ░ ░ ▒  ░ ░░ ░  ▒ ░  ░ ░   
░  ░                 ░ ░  ░  ░      ░  ░    
EOF
echo -e "${NC}"

echo -e "${GREEN}🧠 Welcome to KENKI OS - AI-Enhanced Security Platform${NC}"
echo -e "${CYAN}This is your first boot. Let's get you set up!${NC}"
echo ""

# Check if this is a live session or installed system
if [ -f /etc/kenki/install.sh ]; then
    echo -e "${YELLOW}📦 Live ISO detected. Running post-install setup...${NC}"
    
    # Run the post-install script
    if [ -x /etc/kenki/install.sh ]; then
        echo -e "${GREEN}🔧 Running KENKI OS installation...${NC}"
        /etc/kenki/install.sh
    else
        echo -e "${RED}❌ Install script not found or not executable${NC}"
    fi
else
    echo -e "${YELLOW}💾 Installed system detected.${NC}"
fi

# Check if AI assistant is available
if [ -f /etc/kenki/ai-assist/kenki_assist.py ]; then
    echo -e "${GREEN}✅ AI Assistant found at /etc/kenki/ai-assist/${NC}"
    
    # Test the AI assistant
    echo -e "${CYAN}🧪 Testing AI Assistant...${NC}"
    if python3 /etc/kenki/ai-assist/kenki_assist.py "test" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ AI Assistant is working!${NC}"
    else
        echo -e "${YELLOW}⚠️ AI Assistant needs configuration (API keys)${NC}"
    fi
else
    echo -e "${RED}❌ AI Assistant not found${NC}"
fi

# Show available tools
echo ""
echo -e "${BLUE}🔐 Available Security Tools:${NC}"
echo "• nmap - Network scanning"
echo "• sqlmap - SQL injection testing"
echo "• hydra - Brute force attacks"
echo "• john - Password cracking"
echo "• aircrack-ng - Wireless security"
echo "• metasploit - Exploitation framework"
echo "• And 2800+ more BlackArch tools!"

# Show AI assistant commands
echo ""
echo -e "${BLUE}🤖 AI Assistant Commands:${NC}"
echo "• kenki-assist --interactive"
echo "• kenki-assist 'explain nmap -sS'"
echo "• kenki-assist 'translate find open ports'"
echo "• kenki-voice --interactive"

# Check for configuration
echo ""
echo -e "${YELLOW}⚙️ Configuration Status:${NC}"
if [ -f /etc/kenki/ai-assist/config.json ]; then
    if grep -q "YOUR_CLAUDE_API_KEY_HERE" /etc/kenki/ai-assist/config.json; then
        echo -e "${YELLOW}⚠️ API keys not configured${NC}"
        echo "   Edit: nano /etc/kenki/ai-assist/config.json"
    else
        echo -e "${GREEN}✅ API keys configured${NC}"
    fi
else
    echo -e "${RED}❌ Configuration file not found${NC}"
fi

# Offer to start AI assistant
echo ""
echo -e "${CYAN}🚀 Quick Start Options:${NC}"
echo "1. Start AI Assistant (interactive mode)"
echo "2. Test a command explanation"
echo "3. Try voice interface"
echo "4. Set up local LLM (offline operation)"
echo "5. Open terminal"
echo "6. Skip and explore manually"

read -p "Choose an option (1-6): " choice

case $choice in
    1)
        echo -e "${GREEN}🎯 Starting AI Assistant...${NC}"
        python3 /etc/kenki/ai-assist/kenki_assist.py --interactive
        ;;
    2)
        echo -e "${GREEN}🧪 Testing command explanation...${NC}"
        python3 /etc/kenki/ai-assist/kenki_assist.py "explain nmap -sS -p 80 192.168.1.1"
        ;;
    3)
        echo -e "${GREEN}🎤 Starting voice interface...${NC}"
        python3 /etc/kenki/ai-assist/voice.py --interactive
        ;;
    4)
        echo -e "${GREEN}🧠 Setting up local LLM...${NC}"
        if [ -x /etc/kenki/setup-local-llm.sh ]; then
            sudo /etc/kenki/setup-local-llm.sh
        else
            echo -e "${RED}❌ Local LLM setup script not found${NC}"
        fi
        ;;
    5)
        echo -e "${GREEN}💻 Opening terminal...${NC}"
        # This will depend on the desktop environment
        if command -v alacritty &> /dev/null; then
            alacritty &
        elif command -v kitty &> /dev/null; then
            kitty &
        else
            xterm &
        fi
        ;;
    6)
        echo -e "${CYAN}👋 Enjoy exploring KENKI OS!${NC}"
        ;;
    *)
        echo -e "${YELLOW}Invalid choice. Opening terminal...${NC}"
        if command -v alacritty &> /dev/null; then
            alacritty &
        elif command -v kitty &> /dev/null; then
            kitty &
        else
            xterm &
        fi
        ;;
esac

echo ""
echo -e "${GREEN}🎉 KENKI OS is ready for ethical hacking!${NC}"
echo -e "${YELLOW}⚠️ Remember: Use these tools responsibly and only on authorized systems!${NC}"
echo ""
echo -e "${CYAN}📚 For help:${NC}"
echo "• kenki-assist --help"
echo "• man <tool-name>"
echo "• /etc/kenki/README.txt"
echo ""

# Create a flag to prevent running again
touch /tmp/kenki-first-run-complete

echo -e "${GREEN}✅ First run complete!${NC}" 