#!/bin/bash
# KENKI OS - Local LLM Setup Script
# Downloads and configures local LLM models for offline AI operation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +%H:%M:%S)]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date +%H:%M:%S)]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +%H:%M:%S)]${NC} $1"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}❌ This script must be run as root (use sudo)${NC}"
    exit 1
fi

log "🧠 Setting up Local LLM for KENKI OS..."

# Create models directory
MODELS_DIR="/etc/kenki/ai-assist/models"
mkdir -p "$MODELS_DIR"
cd "$MODELS_DIR"

# Install llama.cpp dependencies
log "Installing llama.cpp dependencies..."
pacman -S --noconfirm cmake ninja python-pip

# Install llama-cpp-python
log "Installing llama-cpp-python..."
pip install llama-cpp-python

# Download models (choose one based on available space)
log "Available models to download:"
echo "1. Mistral 7B (4GB) - Fast, good quality"
echo "2. Llama2 7B (4GB) - Balanced performance"
echo "3. CodeLlama 7B (4GB) - Good for code/security"
echo "4. Phi-2 (1.5GB) - Small, fast"
echo "5. Skip download (manual setup later)"

read -p "Choose model (1-5): " model_choice

case $model_choice in
    1)
        MODEL_URL="https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
        MODEL_NAME="mistral-7b-instruct-v0.2.Q4_K_M.gguf"
        ;;
    2)
        MODEL_URL="https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
        MODEL_NAME="llama-2-7b-chat.Q4_K_M.gguf"
        ;;
    3)
        MODEL_URL="https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF/resolve/main/codellama-7b-instruct.Q4_K_M.gguf"
        MODEL_NAME="codellama-7b-instruct.Q4_K_M.gguf"
        ;;
    4)
        MODEL_URL="https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf"
        MODEL_NAME="phi-2.Q4_K_M.gguf"
        ;;
    5)
        log "Skipping model download. You can download manually later."
        log "Models directory: $MODELS_DIR"
        exit 0
        ;;
    *)
        error "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Check available disk space
AVAILABLE_SPACE=$(df . | awk 'NR==2 {print $4}')
REQUIRED_SPACE=5000000  # 5GB in KB

if [ "$AVAILABLE_SPACE" -lt "$REQUIRED_SPACE" ]; then
    error "Insufficient disk space. Need at least 5GB free."
    echo "Available: $(($AVAILABLE_SPACE / 1024 / 1024))GB"
    exit 1
fi

log "Downloading model: $MODEL_NAME"
log "This may take 10-30 minutes depending on your internet connection..."

# Download with progress
wget --progress=bar:force:noscroll "$MODEL_URL" -O "$MODEL_NAME"

if [ $? -eq 0 ]; then
    log "✅ Model downloaded successfully!"
    log "Model size: $(du -h "$MODEL_NAME" | cut -f1)"
else
    error "❌ Model download failed!"
    exit 1
fi

# Update config.json with local model path
CONFIG_FILE="/etc/kenki/ai-assist/config.json"
if [ -f "$CONFIG_FILE" ]; then
    log "Updating config.json with local model path..."
    
    # Create backup
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
    
    # Update the local_llm section
    python3 -c "
import json
import os

config_file = '$CONFIG_FILE'
model_path = '$MODELS_DIR/$MODEL_NAME'

if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    if 'local_llm' not in config:
        config['local_llm'] = {}
    
    config['local_llm']['enabled'] = True
    config['local_llm']['model_path'] = model_path
    config['local_llm']['endpoint'] = 'http://localhost:11434'
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print('Config updated successfully!')
else:
    print('Config file not found, creating new one...')
    config = {
        'anthropic_api_key': '',
        'openai_api_key': '',
        'local_llm': {
            'enabled': True,
            'model_path': model_path,
            'endpoint': 'http://localhost:11434'
        },
        'preferences': {
            'default_model': 'local',
            'max_tokens': 1000,
            'temperature': 0.7
        }
    }
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print('New config file created!')
"
    
    log "✅ Configuration updated!"
else
    warn "Config file not found. You'll need to configure manually."
fi

# Test the local LLM
log "Testing local LLM..."
python3 -c "
from llama_cpp import Llama
import os

model_path = '$MODELS_DIR/$MODEL_NAME'
if os.path.exists(model_path):
    try:
        llm = Llama(model_path=model_path, n_ctx=2048, n_threads=4)
        response = llm('Hello, I am KENKI OS AI assistant. Test message.', max_tokens=50)
        print('✅ Local LLM test successful!')
        print(f'Response: {response[\"choices\"][0][\"text\"]}')
    except Exception as e:
        print(f'❌ Local LLM test failed: {e}')
else:
    print(f'❌ Model file not found: {model_path}')
"

# Create systemd service for auto-start
log "Creating systemd service for local LLM..."
cat > /etc/systemd/system/kenki-local-llm.service << EOF
[Unit]
Description=KENKI OS Local LLM Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$MODELS_DIR
ExecStart=/usr/bin/python3 -c "from llama_cpp import Llama; Llama(model_path='$MODELS_DIR/$MODEL_NAME', n_ctx=2048, n_threads=4)"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
systemctl daemon-reload
systemctl enable kenki-local-llm.service

log "✅ Local LLM setup complete!"
echo ""
echo -e "${GREEN}🎉 Local LLM Setup Summary:${NC}"
echo "• Model: $MODEL_NAME"
echo "• Location: $MODELS_DIR"
echo "• Size: $(du -h "$MODEL_NAME" | cut -f1)"
echo "• Service: kenki-local-llm.service (enabled)"
echo ""
echo -e "${YELLOW}💡 Usage:${NC}"
echo "• Start AI assistant: kenki-assist"
echo "• Test local model: python3 -c \"from llama_cpp import Llama; llm = Llama('$MODELS_DIR/$MODEL_NAME')\""
echo "• Check service: systemctl status kenki-local-llm.service"
echo ""
echo -e "${BLUE}🔧 Configuration:${NC}"
echo "• Config file: $CONFIG_FILE"
echo "• Default model: local (offline operation)"
echo "• Fallback: Claude (when online)" 