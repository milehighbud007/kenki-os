#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +%H:%M:%S)]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +%H:%M:%S)]${NC} $1" >&2
    exit 1
}

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

🧠 KENKI OS - AI-Enhanced Security Platform
Building custom BlackArch-based ISO...

EOF

if [[ $EUID -ne 0 ]]; then
    error "Please run as root (use sudo)"
fi

if ! command -v mkarchiso >/dev/null 2>&1; then
    error "mkarchiso not found. Install 'archiso' package first."
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="${SCRIPT_DIR}/work"
OUT_DIR="${SCRIPT_DIR}/out"
PROFILE_DIR="${SCRIPT_DIR}/archiso/releng"

log "Checking disk space..."
avail_gb=$(df -Pk "${SCRIPT_DIR}" | awk 'NR==2 {print int($4/1024/1024)}')
if (( avail_gb < 20 )); then
    error "Not enough disk space (need at least 20GB, have ${avail_gb}GB)"
fi
log "Disk space OK: ${avail_gb}GB available"

log "Preparing ArchISO profile..."
if [[ ! -d "${PROFILE_DIR}" ]]; then
    error "Profile directory not found: ${PROFILE_DIR}"
fi

log "Cleaning previous build dirs..."
rm -rf "${WORK_DIR}" "${OUT_DIR}"
mkdir -p "${WORK_DIR}" "${OUT_DIR}"

log "Starting ISO build..."
mkarchiso -v -w "${WORK_DIR}" -o "${OUT_DIR}" "${PROFILE_DIR}"

log "✅ Build complete"
log "ISO is in: ${OUT_DIR}"
