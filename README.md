# 🧠 KENKI OS - AI-Enhanced Security Platform

Maintained: Jackie-DeVere Allen Cole aka DevPen187
VP Architecture 
PinkHat Security Enterprise, Inc
1-719-421-6200

**KENKI OS (TrAEL AI Edition)** is a cutting-edge, AI-augmented Linux distribution built on top of BlackArch, designed for ethical hackers, cybersecurity researchers, and developers who want to supercharge their workflow with powerful AI-assisted terminal tools. It combines the firepower of 2,800+ BlackArch tools with an integrated AI assistant terminal.

![KENKI OS Banner](https://img.shields.io/badge/KENKI-OS-purple?style=for-the-badge&logo=linux)
![BlackArch Based](https://img.shields.io/badge/BlackArch-Based-red?style=for-the-badge)
![AI Enhanced](https://img.shields.io/badge/AI-Enhanced-blue?style=for-the-badge)

## 🧠 What is KENKI OS?

KENKI OS – TrAEL AI Edition is a next-gen, AI-augmented Linux OS based on BlackArch, designed for cybersecurity professionals, ethical hackers, and AI researchers. It fuses the raw power of over 2,800+ hacking tools from BlackArch with a smart, Claude 4-powered terminal assistant called `kenki-assist`.

Whether you're reverse engineering, hunting malware, scanning networks, or automating recon, KENKI gives you both intelligence and infrastructure—in one place.

## 🚀 Features

### 🤖 AI Assistant Capabilities
- **Command Explanation**: Get detailed explanations of any command or tool
- **Natural Language Translation**: Convert natural language to shell commands
- **Security Tool Guidance**: AI-powered assistance for penetration testing tools
- **Voice Interface**: Hands-free operation with voice commands
- **Local LLM Support**: Integration with llama.cpp and other local models
- **Cloud AI Integration**: Claude 4 API support for advanced reasoning

### 🛡️ Security Tools (2800+ BlackArch Tools)
- **Network Analysis**: nmap, wireshark, tcpdump, netcat
- **Web Application Testing**: sqlmap, nikto, dirb, wpscan, joomscan
- **Password Cracking**: john, hashcat, hydra
- **Wireless Security**: aircrack-ng suite
- **Forensics**: volatility, autopsy
- **Reverse Engineering**: ghidra, radare2
- **Social Engineering**: maltego, recon-ng
- **Vulnerability Assessment**: nessus, openvas, zap, burp

### 🎨 Custom User Experience
- **Custom GRUB Theme**: KENKI OS branding
- **Desktop Branding**: Custom wallpaper and desktop shortcuts
- **Interactive First-Run**: Guided setup process
- **Auto-Launch AI Assistant**: Starts automatically on boot
- **Professional UI**: Modern desktop environment with XFCE

### 🌐 Hybrid AI Support
- **🔗 Cloud**: Claude 4 via Anthropic API
- **🔒 Local**: Llama.cpp, Mistral, Phi-2, or Ollama

### 🎙️ Voice Support (Optional)
- Use Whisper for offline speech-to-text
- Speak commands and hear responses

### 🖥️ Optional Warp-style GUI
- Tauri or Electron frontend in development
- Output blocks, command history, AI sidebar

### 🧰 Offline Ready
- No cloud dependency — works 100% air-gapped

### 🛠️ Developer-First
- Includes Python, Rust, Go, Git, Docker, QEMU, and more

## 🛠️ Tech Stack

| Layer        | Tools Used                           |
|--------------|---------------------------------------|
| Base OS      | BlackArch Linux                       |
| AI Cloud     | Claude 4 (Anthropic API)              |
| AI Local     | Llama.cpp, Ollama, Mistral, Phi       |
| Shell        | Zsh + Starship                        |
| Terminal     | Alacritty / Kitty                     |
| Voice Input  | Whisper.cpp / Vosk                    |
| GUI (opt.)   | Tauri / Textual (coming soon)         |
| ISO Builder  | ArchISO                               |

## 📁 Project Structure

```
KENKI OS/
├── ai-assist/                    # AI Assistant Core
│   ├── kenki_assist.py          # Main CLI interface
│   ├── explain.py               # Command explanation module
│   ├── translate.py             # Natural language translation
│   ├── voice.py                 # Voice interface
│   ├── config.json              # Configuration file
│   └── requirements.txt         # Python dependencies
├── install/                      # Installation Scripts
│   ├── install.sh               # Main installation script
│   └── post-install.sh          # Post-installation setup
├── archiso/                      # ISO Build Configuration
│   └── releng/                  # Archiso profile
│       ├── ai-assist-overlay/   # Custom files overlay
│       ├── packages.x86_64      # Package list
│       └── profiledef.sh        # Build configuration
├── tests/                        # Test Suite
│   └── test_kenki.py           # AI assistant tests
├── demo/                         # Demo Scripts
│   └── demo.py                  # Interactive demo
├── docs/                         # Documentation
│   └── QUICK_START.md          # Quick start guide
├── build-iso.sh                 # Automated build script
└── README.md                    # This file
```

## 📦 Installation

### 🧪 Live Testing

Download the ISO (or build it yourself) and boot into KENKI via:
- 🖥️ VirtualBox / QEMU / UTM
- 🧳 USB Live boot

### 🧰 Manual Install (for CLI assistant)

```bash
git clone https://github.com/yourusername/kenki-os.git
cd kenki-os/install
bash install.sh
```

## 🛠️ Quick Start

### Prerequisites
- Arch Linux or Arch-based system (for building)
- At least 10GB free disk space
- Root access (for ISO building)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/kenki-os.git
cd kenki-os
```

### 2. Build the ISO
```bash
sudo ./build-iso.sh
```

The build process will:
- Install required dependencies (archiso)
- Set up the BlackArch-based profile
- Copy AI assistant files to the overlay
- Apply custom branding and configurations
- Build the ISO (30-60 minutes)

### 3. Test the ISO
```bash
# Test in QEMU (recommended)
qemu-system-x86_64 -enable-kvm -m 4G -smp 4 -boot d -cdrom archiso/releng/out/kenki-os-*.iso

# Or use VirtualBox/VMware
```

### 4. First Boot Setup
1. Boot the ISO
2. Run the first-run script: `/etc/kenki/first-run.sh`
3. Configure API keys: `nano /etc/kenki/ai-assist/config.json`
4. Start the AI assistant: `kenki-assist`

## 🤖 AI Assistant Usage

### Basic Commands
```bash
# Start interactive mode
kenki-assist

# Explain a command
kenki-assist explain "nmap -sS -p 80 192.168.1.1"

# Translate natural language to command
kenki-assist translate "scan for open ports on my local network"

# Voice mode
kenki-assist voice
```

### Configuration
Edit `/etc/kenki/ai-assist/config.json`:
```json
{
  "claude_api_key": "your-claude-api-key",
  "openai_api_key": "your-openai-api-key",
  "local_model_path": "/path/to/llama.cpp/model",
  "voice_enabled": true,
  "auto_explain": true
}
```

### Voice Commands
- "Scan network" → Runs network discovery
- "Check vulnerabilities" → Launches vulnerability scanner
- "Explain tool" → Gets tool explanation
- "Show help" → Displays available commands

## 💬 Example Usage

```bash
kenki-assist "Explain this command: awk '{print $2}' file.txt"
```

```bash
kenki-assist "Find all open ports in the 192.168.1.0/24 range"
```

```bash
kenki-assist "Summarize this network scan log: logs/nmap-result.txt"
```

## 🧪 Testing

### Run Test Suite
```bash
cd tests
python test_kenki.py
```

### Demo Mode
```bash
cd demo
python demo.py
```

## 🔧 Customization

### Adding Custom Tools
1. Add packages to `archiso/releng/packages.x86_64`
2. Update AI assistant knowledge in `ai-assist/kenki_assist.py`
3. Rebuild the ISO

### Modifying AI Behavior
- Edit `ai-assist/kenki_assist.py` for core logic
- Modify `ai-assist/config.json` for settings
- Update voice commands in `ai-assist/voice.py`

### Custom Branding
- Replace `archiso/releng/ai-assist-overlay/etc/kenki/kenki-wallpaper.png`
- Edit GRUB theme in `archiso/releng/ai-assist-overlay/etc/kenki/kenki-grub-theme/`
- Modify desktop shortcuts in overlay

## 👥 Who Is It For?

* Ethical hackers and red teamers
* SOC analysts and cybersecurity researchers
* AI engineers who work in security
* OS developers exploring AI + Linux integration
* Students building cybersecurity-AI prototypes

## 🧩 Roadmap

* [x] Claude 4 + Local AI Terminal CLI
* [ ] Tauri GUI Interface (Warp-style terminal)
* [ ] AI-enhanced log and PCAP stream analyzer
* [ ] GPT-4o fallback integration
* [ ] Plugin system for modular AI agents
* [ ] Voice-to-terminal auto actions

## 📚 Documentation

- [Quick Start Guide](docs/QUICK_START.md) - Getting started with KENKI OS
- [AI Assistant Guide](ai-assist/README.md) - Using the AI features
- [Build Guide](archiso/releng/README.md) - Customizing the ISO build

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r ai-assist/requirements.txt

# Run tests
python tests/test_kenki.py

# Test AI assistant locally
python ai-assist/kenki_assist.py --interactive
```

We welcome:
* New AI features or prompt chains
* Shell integrations
* Claude/GPT prompt engineering
* GUI frontend improvements (Tauri / Electron)
* Model benchmarking and optimization

## ⚠️ Legal and Ethical Notice

**IMPORTANT**: KENKI OS is designed for ethical hacking and authorized security testing only.

- ✅ **Authorized**: Use on systems you own or have explicit permission to test
- ❌ **Unauthorized**: Never use on systems without permission
- 🔒 **Compliance**: Follow all applicable laws and regulations
- 📋 **Documentation**: Keep detailed records of all testing activities

The developers are not responsible for any misuse of this software.

## 🆘 Troubleshooting

### Common Issues

**Build Fails**
```bash
# Check disk space
df -h

# Clean previous builds
sudo rm -rf archiso/releng/work archiso/releng/out

# Reinstall archiso
sudo pacman -S --noconfirm archiso
```

**AI Assistant Not Working**
```bash
# Check API keys
cat /etc/kenki/ai-assist/config.json

# Test connectivity
curl -I https://api.anthropic.com

# Check Python dependencies
pip list | grep -E "(anthropic|openai)"
```

**Voice Interface Issues**
```bash
# Install audio dependencies
sudo pacman -S pulseaudio alsa-utils

# Test microphone
arecord -d 5 test.wav && aplay test.wav
```

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/kenki-os/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/kenki-os/discussions)
- **Documentation**: [Wiki](https://github.com/your-username/kenki-os/wiki)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **BlackArch Linux** - Base security distribution
- **Arch Linux** - Base system
- **Anthropic** - Claude AI API
- **OpenAI** - GPT API
- **llama.cpp** - Local LLM support

## ✨ Credits

Created by **ROHIT(CYROS)**
Founder of the KENKI Project – where AI meets offensive security.

---

**🧠 KENKI OS - Where AI Meets Ethical Hacking**

*Built with ❤️ for the security community*
