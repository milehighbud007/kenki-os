#!/bin/bash
# KENKI OS Advanced Setup Script
# Configures desktop environment, wallpaper, and system preferences

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}🔧 Configuring KENKI OS desktop environment...${NC}"

# Create user directories if they don't exist
mkdir -p ~/.config
mkdir -p ~/.local/share/applications
mkdir -p ~/Pictures/Wallpapers

# Copy KENKI wallpaper if available
if [ -f /etc/kenki/kenki-wallpaper.png ]; then
    echo -e "${BLUE}🎨 Setting up KENKI wallpaper...${NC}"
    cp /etc/kenki/kenki-wallpaper.png ~/Pictures/Wallpapers/
    
    # Set wallpaper for different desktop environments
    if command -v xfconf-query &> /dev/null; then
        # XFCE
        xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s ~/Pictures/Wallpapers/kenki-wallpaper.png
    elif command -v gsettings &> /dev/null; then
        # GNOME
        gsettings set org.gnome.desktop.background picture-uri "file://$HOME/Pictures/Wallpapers/kenki-wallpaper.png"
    fi
fi

# Copy desktop entries
echo -e "${BLUE}📱 Setting up desktop shortcuts...${NC}"
if [ -f /etc/kenki/kenki-branding.desktop ]; then
    cp /etc/kenki/kenki-branding.desktop ~/.local/share/applications/
    update-desktop-database ~/.local/share/applications
fi

# Configure terminal preferences
echo -e "${BLUE}💻 Configuring terminal...${NC}"
mkdir -p ~/.config/alacritty
cat > ~/.config/alacritty/alacritty.yml << 'EOF'
# KENKI OS Alacritty Configuration
window:
  opacity: 0.9
  decorations: buttonless
  padding:
    x: 10
    y: 10

font:
  normal:
    family: "JetBrains Mono"
    style: Regular
  bold:
    family: "JetBrains Mono"
    style: Bold
  italic:
    family: "JetBrains Mono"
    style: Italic
  size: 12

colors:
  primary:
    background: '#1a1a1a'
    foreground: '#f8f8f2'
  cursor:
    text: '#1a1a1a'
    cursor: '#f8f8f2'
  normal:
    black: '#1a1a1a'
    red: '#ff5555'
    green: '#50fa7b'
    yellow: '#f1fa8c'
    blue: '#bd93f9'
    magenta: '#ff79c6'
    cyan: '#8be9fd'
    white: '#bfbfbf'
  bright:
    black: '#575757'
    red: '#ff6e67'
    green: '#5af78e'
    yellow: '#f4f99d'
    blue: '#caa9fa'
    magenta: '#ff92d0'
    cyan: '#9aedfe'
    white: '#e6e6e6'

selection:
  save_to_clipboard: true

cursor:
  style: Block
  blink_interval: 0
  blink_timeout: 5

mouse:
  hide_when_typing: false

key_bindings:
  - { key: V, mods: Control, action: Paste }
  - { key: C, mods: Control, action: Copy }
  - { key: Key0, mods: Control, action: ResetFontSize }
  - { key: Equals, mods: Control, action: IncreaseFontSize }
  - { key: Minus, mods: Control, action: DecreaseFontSize }
EOF

# Configure Starship prompt
echo -e "${BLUE}⭐ Configuring Starship prompt...${NC}"
mkdir -p ~/.config
cat > ~/.config/starship.toml << 'EOF'
# KENKI OS Starship Configuration
format = """
$username\
$hostname\
$directory\
$git_branch\
$git_state\
$git_status\
$cmd_duration\
$line_break\
$python\
$character"""

[character]
success_symbol = "[🧠](green)"
error_symbol = "[❌](red)"
use_symbol_for_status = true

[directory]
style = "blue bold"
truncation_length = 3
truncation_symbol = "…/"

[git_branch]
symbol = "🌿 "
truncation_length = 4
truncation_symbol = ""

[cmd_duration]
min_time = 2000
format = "took [$duration](yellow) "

[python]
symbol = "🐍 "
EOF

# Configure Zsh
echo -e "${BLUE}🐚 Configuring Zsh...${NC}"
if [ ! -f ~/.zshrc ]; then
    cat > ~/.zshrc << 'EOF'
# KENKI OS Shell Configuration

# Path to KENKI AI Assistant
export KENKI_DIR="/etc/kenki"
export PATH="$KENKI_DIR/ai-assist:$PATH"

# KENKI aliases
alias kenki='python3 $KENKI_DIR/ai-assist/kenki_assist.py'
alias kenki-assist='python3 $KENKI_DIR/ai-assist/kenki_assist.py'
alias kenki-voice='python3 $KENKI_DIR/ai-assist/voice.py'
alias kenki-explain='python3 $KENKI_DIR/ai-assist/explain.py'
alias kenki-translate='python3 $KENKI_DIR/ai-assist/translate.py'

# KENKI prompt integration
kenki_prompt() {
    if [ $? -eq 0 ]; then
        echo "🧠 KENKI ready"
    else
        echo "❌ KENKI error"
    fi
}

# Add to PROMPT
PROMPT='%F{blue}%n@%m%f %F{green}%~%f %F{yellow}$(kenki_prompt)%f %# '

# Oh My Zsh configuration
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="agnoster"
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
source $ZSH/oh-my-zsh.sh

# Starship prompt
eval "$(starship init zsh)"

# KENKI welcome message
echo "🧠 Welcome to KENKI OS - AI-Enhanced Security Platform"
echo "💡 Type 'kenki --help' for AI assistant commands"
echo "🔧 Type 'kenki --interactive' for interactive mode"
EOF
fi

# Set up autostart for first run
echo -e "${BLUE}🚀 Setting up autostart...${NC}"
mkdir -p ~/.config/autostart
if [ -f /etc/kenki/kenki-autostart.desktop ]; then
    cp /etc/kenki/kenki-autostart.desktop ~/.config/autostart/
fi

# Create symlinks for easy access
echo -e "${BLUE}🔗 Creating symlinks...${NC}"
sudo ln -sf /etc/kenki/ai-assist/kenki_assist.py /usr/local/bin/kenki-assist
sudo ln -sf /etc/kenki/ai-assist/kenki_assist.py /usr/local/bin/kenki
sudo ln -sf /etc/kenki/ai-assist/voice.py /usr/local/bin/kenki-voice

# Set default shell to zsh if available
if command -v chsh &> /dev/null && [ "$SHELL" != "/bin/zsh" ]; then
    echo -e "${YELLOW}🐚 Setting default shell to zsh...${NC}"
    chsh -s $(which zsh)
fi

echo -e "${GREEN}✅ KENKI OS desktop configuration complete!${NC}"
echo -e "${BLUE}🎨 Desktop environment configured with KENKI branding${NC}"
echo -e "${BLUE}💻 Terminal configured with KENKI theme${NC}"
echo -e "${BLUE}⭐ Starship prompt configured${NC}"
echo -e "${BLUE}🐚 Zsh configured with KENKI aliases${NC}"
echo -e "${BLUE}🚀 Autostart configured${NC}" 