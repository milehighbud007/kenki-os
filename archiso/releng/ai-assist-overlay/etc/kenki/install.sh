#!/bin/bash
# KENKI OS Post-Installation Script
# Sets up AI assistant and security tools

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[KENKI]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    error "This script should not be run as root"
    exit 1
fi

# KENKI OS Banner
echo -e "${BLUE}"
cat << "EOF"
 ██ ▄█▀▄▄▄█████▓ ▒█████   ██ ▄█▀ ██▓ ██▓    
 ██▄█▒ ▓  ██▒ ▓▒▒██▒  ██▒ ██▄█▒ ▓██▒▓██▒    
▓███▄░ ▒ ▓██░ ▒░▒██░  ██▒▓███▄░ ▒██▒▒██░    
▓██ █▄ ░ ▓██▓ ░ ▒██   ██░▓██ █▄ ░██░▒██░    
▒██▒ █▄░ ▒██▒ ░ ░ ████▓▒░▒██▒ █▄░██░░██████▒
▒ ▒▒ ▓▒ ░ ▒ ░░   ░ ▒░▒░▒░ ▒ ▒▒ ▓▒░▓  ░ ▒░▓  ░
░ ░▒ ▒░ ░ ░      ░ ▒ ▒░ ░ ░▒ ▒░ ▒ ░░ ░ ▒  ░
░ ░░ ░  ░ ░    ░ ░ ░ ▒  ░ ░░ ░  ▒ ░  ░ ░   
░  ░                 ░ ░  ░  ░      ░  ░    
EOF
echo -e "${NC}"

log "Starting KENKI OS AI Assistant Installation..."

# Update system
log "Updating system packages..."
sudo pacman -Syu --noconfirm

# Install base development tools
log "Installing development tools..."
sudo pacman -S --noconfirm base-devel git python python-pip nodejs npm

# Install Python dependencies
log "Installing Python dependencies..."
pip install --user -r requirements.txt

# Install BlackArch tools (if not already installed)
log "Installing BlackArch security tools..."
if ! command -v nmap &> /dev/null; then
    sudo pacman -S --noconfirm blackarch
fi

# Install additional security tools
log "Installing additional security tools..."
sudo pacman -S --noconfirm \
    nmap \
    nikto \
    dirb \
    sqlmap \
    hydra \
    john \
    hashcat \
    aircrack-ng \
    wireshark-qt \
    tcpdump \
    netcat \
    volatility \
    ghidra \
    radare2 \
    maltego \
    recon-ng \
    theharvester \
    amass \
    wpscan \
    joomscan \
    skipfish \
    w3af \
    zap \
    burp \
    nessus \
    openvas

# Install terminal and shell tools
log "Installing terminal and shell tools..."
sudo pacman -S --noconfirm \
    zsh \
    alacritty \
    kitty \
    starship \
    oh-my-zsh-git \
    fzf \
    ripgrep \
    bat \
    exa \
    fd \
    htop \
    neofetch

# Install AI and ML tools
log "Installing AI and ML tools..."
sudo pacman -S --noconfirm \
    ollama \
    llama.cpp \
    python-torch \
    python-torchvision \
    python-torchaudio \
    python-transformers \
    python-diffusers

# Install GUI tools (optional)
log "Installing GUI tools..."
sudo pacman -S --noconfirm \
    firefox \
    chromium \
    gimp \
    inkscape \
    audacity \
    vlc \
    obs-studio

# Install virtualization tools
log "Installing virtualization tools..."
sudo pacman -S --noconfirm \
    qemu \
    virt-manager \
    virtualbox \
    docker \
    docker-compose

# Setup KENKI AI Assistant
log "Setting up KENKI AI Assistant..."

# Create KENKI directory
KENKI_DIR="$HOME/.kenki"
mkdir -p "$KENKI_DIR"
mkdir -p "$KENKI_DIR/ai-assist"
mkdir -p "$KENKI_DIR/local-llm/models"
mkdir -p "$KENKI_DIR/logs"

# Copy AI assistant files
cp -r ai-assist/* "$KENKI_DIR/ai-assist/"

# Make scripts executable
chmod +x "$KENKI_DIR/ai-assist/kenki_assist.py"

# Create symlinks for easy access
sudo ln -sf "$KENKI_DIR/ai-assist/kenki_assist.py" /usr/local/bin/kenki-assist
sudo ln -sf "$KENKI_DIR/ai-assist/kenki_assist.py" /usr/local/bin/kenki

# Setup shell configuration
log "Setting up shell configuration..."

# Backup existing zshrc
if [ -f "$HOME/.zshrc" ]; then
    cp "$HOME/.zshrc" "$HOME/.zshrc.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Create new zshrc with KENKI integration
cat > "$HOME/.zshrc" << 'EOF'
# KENKI OS Shell Configuration

# Path to KENKI AI Assistant
export KENKI_DIR="$HOME/.kenki"
export PATH="$KENKI_DIR/ai-assist:$PATH"

# KENKI aliases
alias kenki='python $KENKI_DIR/ai-assist/kenki_assist.py'
alias kenki-assist='python $KENKI_DIR/ai-assist/kenki_assist.py'
alias kenki-voice='python $KENKI_DIR/ai-assist/voice.py'
alias kenki-explain='python $KENKI_DIR/ai-assist/explain.py'
alias kenki-translate='python $KENKI_DIR/ai-assist/translate.py'

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

# Install Oh My Zsh if not already installed
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    log "Installing Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi

# Install Zsh plugins
log "Installing Zsh plugins..."
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# Setup Starship prompt
log "Setting up Starship prompt..."
mkdir -p "$HOME/.config"
cat > "$HOME/.config/starship.toml" << 'EOF'
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

# Setup Alacritty terminal
log "Setting up Alacritty terminal..."
mkdir -p "$HOME/.config/alacritty"
cat > "$HOME/.config/alacritty/alacritty.yml" << 'EOF'
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

# Setup Kitty terminal
log "Setting up Kitty terminal..."
mkdir -p "$HOME/.config/kitty"
cat > "$HOME/.config/kitty/kitty.conf" << 'EOF'
# KENKI OS Kitty Configuration
font_family JetBrains Mono
font_size 12
background_opacity 0.9
background_blur 1

# Colors
foreground #f8f8f2
background #1a1a1a
selection_foreground #1a1a1a
selection_background #f8f8f2

# Black
color0 #1a1a1a
color8 #575757

# Red
color1 #ff5555
color9 #ff6e67

# Green
color2 #50fa7b
color10 #5af78e

# Yellow
color3 #f1fa8c
color11 #f4f99d

# Blue
color4 #bd93f9
color12 #caa9fa

# Magenta
color5 #ff79c6
color13 #ff92d0

# Cyan
color6 #8be9fd
color14 #9aedfe

# White
color7 #bfbfbf
color15 #e6e6e6

# Key bindings
map ctrl+c copy_or_interrupt
map ctrl+v paste_from_clipboard
map ctrl+equal change_font_size all +1.0
map ctrl+minus change_font_size all -1.0
map ctrl+0 change_font_size all 0
EOF

# Setup systemd service for KENKI assistant
log "Setting up KENKI systemd service..."
sudo tee /etc/systemd/user/kenki-assistant.service > /dev/null << 'EOF'
[Unit]
Description=KENKI OS AI Assistant
After=network.target

[Service]
Type=simple
User=%i
WorkingDirectory=%h/.kenki
ExecStart=/usr/bin/python3 %h/.kenki/ai-assist/kenki_assist.py --interactive
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

# Enable the service
systemctl --user enable kenki-assistant.service

# Setup GRUB theme (optional)
log "Setting up GRUB theme..."
sudo mkdir -p /boot/grub/themes/kenki
sudo tee /boot/grub/themes/kenki/theme.txt > /dev/null << 'EOF'
# KENKI OS GRUB Theme
+ boot_menu {
    left = 10%
    width = 80%
    top = 20%
    height = 60%
}

+ label {
    text = "KENKI OS - AI-Enhanced Security Platform"
    left = 10%
    top = 10%
    width = 80%
    height = 10%
    color = "#50fa7b"
    font = "DejaVu Sans 16"
}

+ hbox {
    left = 10%
    top = 20%
    width = 80%
    height = 60%
}

+ vbox {
    width = 50%
    height = 100%
}

+ boot_menu {
    width = 100%
    height = 100%
    item_color = "#f8f8f2"
    item_font = "DejaVu Sans 12"
    selected_item_color = "#50fa7b"
    selected_item_font = "DejaVu Sans 12"
}

+ vbox {
    width = 50%
    height = 100%
}

+ label {
    text = "AI-Enhanced Security Tools"
    left = 0%
    top = 0%
    width = 100%
    height = 20%
    color = "#bd93f9"
    font = "DejaVu Sans 10"
}

+ label {
    text = "• Claude 4 Integration"
    left = 0%
    top = 20%
    width = 100%
    height = 10%
    color = "#f8f8f2"
    font = "DejaVu Sans 8"
}

+ label {
    text = "• 2800+ Security Tools"
    left = 0%
    top = 30%
    width = 100%
    height = 10%
    color = "#f8f8f2"
    font = "DejaVu Sans 8"
}

+ label {
    text = "• Natural Language Commands"
    left = 0%
    top = 40%
    width = 100%
    height = 10%
    color = "#f8f8f2"
    font = "DejaVu Sans 8"
}

+ label {
    text = "• Voice Interface"
    left = 0%
    top = 50%
    width = 100%
    height = 10%
    color = "#f8f8f2"
    font = "DejaVu Sans 8"
}

+ label {
    text = "• Ethical Hacking Focus"
    left = 0%
    top = 60%
    width = 100%
    height = 10%
    color = "#f8f8f2"
    font = "DejaVu Sans 8"
}
EOF

# Update GRUB configuration
if command -v grub-mkconfig &> /dev/null; then
    sudo sed -i 's/GRUB_THEME=.*/GRUB_THEME="\/boot\/grub\/themes\/kenki\/theme.txt"/' /etc/default/grub
    sudo grub-mkconfig -o /boot/grub/grub.cfg
fi

# Create desktop entry
log "Creating desktop entry..."
mkdir -p "$HOME/.local/share/applications"
cat > "$HOME/.local/share/applications/kenki-assistant.desktop" << 'EOF'
[Desktop Entry]
Name=KENKI AI Assistant
Comment=AI-Enhanced Security Assistant
Exec=alacritty -e kenki-assist --interactive
Icon=terminal
Terminal=false
Type=Application
Categories=System;Security;Development;
Keywords=security;ai;hacking;penetration;testing;
EOF

# Create desktop entry for terminal
cat > "$HOME/.local/share/applications/kenki-terminal.desktop" << 'EOF'
[Desktop Entry]
Name=KENKI Terminal
Comment=AI-Enhanced Terminal
Exec=alacritty
Icon=terminal
Terminal=false
Type=Application
Categories=System;TerminalEmulator;
Keywords=terminal;console;command;
EOF

# Setup Python virtual environment
log "Setting up Python virtual environment..."
python -m venv "$KENKI_DIR/venv"
source "$KENKI_DIR/venv/bin/activate"
pip install -r requirements.txt

# Create activation script
cat > "$KENKI_DIR/activate.sh" << 'EOF'
#!/bin/bash
source "$HOME/.kenki/venv/bin/activate"
export PYTHONPATH="$HOME/.kenki:$PYTHONPATH"
EOF

chmod +x "$KENKI_DIR/activate.sh"

# Setup logging
log "Setting up logging..."
mkdir -p "$KENKI_DIR/logs"
touch "$KENKI_DIR/logs/kenki_assistant.log"

# Create configuration template
log "Creating configuration template..."
if [ ! -f "$KENKI_DIR/ai-assist/config.json" ]; then
    cp "$KENKI_DIR/ai-assist/config.json" "$KENKI_DIR/ai-assist/config.json.backup"
    cat > "$KENKI_DIR/ai-assist/config.json" << 'EOF'
{
  "anthropic_api_key": "YOUR_CLAUDE_API_KEY_HERE",
  "openai_api_key": "YOUR_OPENAI_API_KEY_HERE",
  "local_llm": {
    "enabled": false,
    "model_path": "models/mistral.gguf",
    "endpoint": "http://localhost:11434"
  },
  "preferences": {
    "default_model": "claude",
    "max_tokens": 1000,
    "temperature": 0.7
  }
}
EOF
fi

# Final setup
log "Finalizing setup..."

# Set default shell to zsh
if command -v chsh &> /dev/null; then
    log "Setting default shell to zsh..."
    chsh -s $(which zsh)
fi

# Create welcome script
cat > "$KENKI_DIR/welcome.sh" << 'EOF'
#!/bin/bash
echo "🧠 Welcome to KENKI OS!"
echo "💡 Available commands:"
echo "   kenki-assist          - AI assistant"
echo "   kenki-assist -i       - Interactive mode"
echo "   kenki-voice           - Voice interface"
echo ""
echo "🔧 Setup your API keys:"
echo "   nano ~/.kenki/ai-assist/config.json"
echo ""
echo "📚 Documentation:"
echo "   kenki-assist --help"
echo ""
echo "🚀 Ready for ethical hacking!"
EOF

chmod +x "$KENKI_DIR/welcome.sh"

# Display completion message
echo ""
echo -e "${GREEN}🎉 KENKI OS Installation Complete!${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "1. Configure your API keys:"
echo "   nano ~/.kenki/ai-assist/config.json"
echo ""
echo "2. Start the AI assistant:"
echo "   kenki-assist --interactive"
echo ""
echo "3. Test the voice interface:"
echo "   kenki-voice"
echo ""
echo "4. Explore security tools:"
echo "   nmap --help"
echo "   nikto --help"
echo ""
echo -e "${YELLOW}⚠️  Remember: Use these tools responsibly and only on authorized systems!${NC}"
echo ""
echo -e "${GREEN}🧠 KENKI OS - AI-Enhanced Security Platform${NC}"
echo ""

# Run welcome script
"$KENKI_DIR/welcome.sh"

log "Installation completed successfully!"
log "Please restart your terminal or run: source ~/.zshrc"