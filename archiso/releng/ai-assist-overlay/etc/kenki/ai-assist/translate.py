#!/usr/bin/env python3
"""
KENKI OS - Natural Language to Shell Translation Module
Converts natural language requests into executable shell commands
"""

import re
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class ShellTranslator:
    """Translates natural language to shell commands using AI"""
    
    def __init__(self, claude_client=None, local_llm=None):
        self.claude_client = claude_client
        self.local_llm = local_llm
        
        # Common security tool patterns
        self.security_patterns = {
            'network_scan': [
                'scan network', 'find open ports', 'check ports', 'network discovery',
                'port scan', 'host discovery', 'network enumeration'
            ],
            'vulnerability_scan': [
                'vulnerability scan', 'security scan', 'find vulnerabilities',
                'security assessment', 'penetration test', 'security audit'
            ],
            'web_scan': [
                'web scan', 'website scan', 'web application test', 'web security',
                'web vulnerability', 'web audit', 'web penetration test'
            ],
            'password_crack': [
                'crack password', 'break password', 'password recovery',
                'hash crack', 'password attack', 'brute force'
            ],
            'wireless_attack': [
                'wifi hack', 'wireless attack', 'wifi crack', 'wireless security',
                'wifi password', 'wireless network', 'wifi audit'
            ],
            'forensics': [
                'forensics', 'memory analysis', 'disk analysis', 'file recovery',
                'evidence analysis', 'digital forensics', 'incident response'
            ],
            'malware_analysis': [
                'malware analysis', 'virus analysis', 'reverse engineering',
                'binary analysis', 'malware reverse', 'virus reverse'
            ],
            'osint': [
                'osint', 'open source intelligence', 'information gathering',
                'reconnaissance', 'intelligence gathering', 'threat intelligence'
            ]
        }
    
    def translate(self, natural_language: str) -> str:
        """Translate natural language to shell commands"""
        if not natural_language.strip():
            return "❌ Please provide a description of what you want to do."
        
        # Clean the input
        natural_language = natural_language.strip()
        
        # Check for common patterns first
        pattern_match = self._match_security_patterns(natural_language)
        if pattern_match:
            return pattern_match
        
        # Use AI for general translation
        return self._translate_with_ai(natural_language)
    
    def _match_security_patterns(self, text: str) -> Optional[str]:
        """Match common security testing patterns"""
        text_lower = text.lower()
        
        # Network scanning patterns
        if any(pattern in text_lower for pattern in self.security_patterns['network_scan']):
            return self._generate_network_scan_command(text)
        
        # Vulnerability scanning patterns
        if any(pattern in text_lower for pattern in self.security_patterns['vulnerability_scan']):
            return self._generate_vulnerability_scan_command(text)
        
        # Web scanning patterns
        if any(pattern in text_lower for pattern in self.security_patterns['web_scan']):
            return self._generate_web_scan_command(text)
        
        # Password cracking patterns
        if any(pattern in text_lower for pattern in self.security_patterns['password_crack']):
            return self._generate_password_crack_command(text)
        
        # Wireless attack patterns
        if any(pattern in text_lower for pattern in self.security_patterns['wireless_attack']):
            return self._generate_wireless_attack_command(text)
        
        # Forensics patterns
        if any(pattern in text_lower for pattern in self.security_patterns['forensics']):
            return self._generate_forensics_command(text)
        
        # Malware analysis patterns
        if any(pattern in text_lower for pattern in self.security_patterns['malware_analysis']):
            return self._generate_malware_analysis_command(text)
        
        # OSINT patterns
        if any(pattern in text_lower for pattern in self.security_patterns['osint']):
            return self._generate_osint_command(text)
        
        return None
    
    def _generate_network_scan_command(self, text: str) -> str:
        """Generate network scanning commands"""
        # Extract target information
        target = self._extract_target(text)
        
        if 'quick' in text.lower() or 'fast' in text.lower():
            return f"nmap -sS -p 80,443,22,21,23,25,53,110,143,993,995 {target}"
        elif 'comprehensive' in text.lower() or 'full' in text.lower():
            return f"nmap -sS -sV -O -p- {target}"
        elif 'stealth' in text.lower() or 'quiet' in text.lower():
            return f"nmap -sS -T2 -p 80,443,22 {target}"
        else:
            return f"nmap -sS -p 80,443,22,21,23,25,53 {target}"
    
    def _generate_vulnerability_scan_command(self, text: str) -> str:
        """Generate vulnerability scanning commands"""
        target = self._extract_target(text)
        
        if 'web' in text.lower():
            return f"nikto -h {target}"
        elif 'network' in text.lower():
            return f"nmap -sS -sV --script vuln {target}"
        else:
            return f"nmap -sS -sV --script vuln {target}"
    
    def _generate_web_scan_command(self, text: str) -> str:
        """Generate web scanning commands"""
        target = self._extract_target(text)
        
        if 'directory' in text.lower() or 'dir' in text.lower():
            return f"dirb http://{target}"
        elif 'wordpress' in text.lower():
            return f"wpscan --url http://{target}"
        elif 'joomla' in text.lower():
            return f"joomscan --url http://{target}"
        else:
            return f"nikto -h {target}"
    
    def _generate_password_crack_command(self, text: str) -> str:
        """Generate password cracking commands"""
        if 'hash' in text.lower():
            return "john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt"
        elif 'zip' in text.lower():
            return "john --wordlist=/usr/share/wordlists/rockyou.txt archive.zip"
        else:
            return "john --wordlist=/usr/share/wordlists/rockyou.txt password.txt"
    
    def _generate_wireless_attack_command(self, text: str) -> str:
        """Generate wireless attack commands"""
        if 'capture' in text.lower() or 'handshake' in text.lower():
            return "airodump-ng -w capture wlan0"
        elif 'crack' in text.lower() or 'attack' in text.lower():
            return "aircrack-ng -w /usr/share/wordlists/rockyou.txt capture-01.cap"
        else:
            return "airodump-ng wlan0"
    
    def _generate_forensics_command(self, text: str) -> str:
        """Generate forensics commands"""
        if 'memory' in text.lower():
            return "volatility -f memory.dmp imageinfo"
        elif 'disk' in text.lower():
            return "strings disk.img | grep -i password"
        else:
            return "strings file.bin | grep -i suspicious"
    
    def _generate_malware_analysis_command(self, text: str) -> str:
        """Generate malware analysis commands"""
        if 'static' in text.lower():
            return "strings malware.exe"
        elif 'dynamic' in text.lower():
            return "strace ./malware"
        else:
            return "file malware.exe"
    
    def _generate_osint_command(self, text: str) -> str:
        """Generate OSINT commands"""
        target = self._extract_target(text)
        
        if 'email' in text.lower():
            return f"theharvester -d {target} -b google"
        elif 'domain' in text.lower():
            return f"amass enum -d {target}"
        else:
            return f"theharvester -d {target} -b all"
    
    def _extract_target(self, text: str) -> str:
        """Extract target from natural language"""
        # Look for IP addresses
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ip_match = re.search(ip_pattern, text)
        if ip_match:
            return ip_match.group()
        
        # Look for domain names
        domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
        domain_match = re.search(domain_pattern, text)
        if domain_match:
            return domain_match.group()
        
        # Look for hostnames
        hostname_pattern = r'\b(?:localhost|127\.0\.0\.1)\b'
        hostname_match = re.search(hostname_pattern, text)
        if hostname_match:
            return hostname_match.group()
        
        # Default target
        return "192.168.1.1"
    
    def _translate_with_ai(self, natural_language: str) -> str:
        """Use AI to translate natural language to shell commands"""
        prompt = f"""
        Convert this natural language request into a Linux shell command for security testing:
        
        Request: {natural_language}
        
        Requirements:
        1. Generate a single, executable shell command
        2. Focus on security and penetration testing tools
        3. Include appropriate flags and parameters
        4. Consider safety and legal implications
        5. Use common security tools like nmap, nikto, dirb, etc.
        6. Provide a command that would be useful for ethical hacking
        
        Return only the shell command, no explanations.
        """
        
        try:
            if self.claude_client:
                response = self.claude_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=200,
                    temperature=0.3,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            elif self.local_llm:
                response = self.local_llm(
                    prompt,
                    max_tokens=200,
                    temperature=0.3,
                    stop=["\n\n", "Human:", "Assistant:"]
                )
                return response["choices"][0]["text"].strip()
            else:
                return self._fallback_translation(natural_language)
        except Exception as e:
            logger.error(f"AI translation failed: {e}")
            return self._fallback_translation(natural_language)
    
    def _fallback_translation(self, natural_language: str) -> str:
        """Fallback translation when AI is not available"""
        text_lower = natural_language.lower()
        
        # Simple pattern matching fallback
        if 'port' in text_lower and 'scan' in text_lower:
            target = self._extract_target(natural_language)
            return f"nmap -sS -p 80,443,22,21,23,25,53 {target}"
        elif 'web' in text_lower and 'scan' in text_lower:
            target = self._extract_target(natural_language)
            return f"nikto -h {target}"
        elif 'directory' in text_lower or 'dir' in text_lower:
            target = self._extract_target(natural_language)
            return f"dirb http://{target}"
        elif 'password' in text_lower and 'crack' in text_lower:
            return "john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt"
        elif 'wifi' in text_lower or 'wireless' in text_lower:
            return "airodump-ng wlan0"
        else:
            return f"# No specific command found for: {natural_language}\n# Please use AI assistance for better translation"
    
    def translate_with_context(self, natural_language: str, context: Dict[str, Any]) -> str:
        """Translate with additional context"""
        # Add context to the prompt
        context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
        
        prompt = f"""
        Convert this natural language request into a Linux shell command for security testing:
        
        Request: {natural_language}
        
        Context:
        {context_str}
        
        Requirements:
        1. Generate a single, executable shell command
        2. Use the provided context to customize the command
        3. Focus on security and penetration testing tools
        4. Include appropriate flags and parameters
        5. Consider safety and legal implications
        
        Return only the shell command, no explanations.
        """
        
        try:
            if self.claude_client:
                response = self.claude_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=200,
                    temperature=0.3,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            elif self.local_llm:
                response = self.local_llm(
                    prompt,
                    max_tokens=200,
                    temperature=0.3,
                    stop=["\n\n", "Human:", "Assistant:"]
                )
                return response["choices"][0]["text"].strip()
            else:
                return self._fallback_translation(natural_language)
        except Exception as e:
            logger.error(f"AI translation with context failed: {e}")
            return self._fallback_translation(natural_language)
    
    def suggest_alternatives(self, natural_language: str) -> List[str]:
        """Suggest alternative commands for a request"""
        prompt = f"""
        For this security testing request, suggest 3 alternative Linux shell commands:
        
        Request: {natural_language}
        
        Provide 3 different approaches, each as a single shell command.
        Focus on different tools and methodologies.
        Return only the commands, one per line, no explanations.
        """
        
        try:
            if self.claude_client:
                response = self.claude_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=300,
                    temperature=0.7,
                    messages=[{"role": "user", "content": prompt}]
                )
                alternatives = response.content[0].text.strip().split('\n')
                return [alt.strip() for alt in alternatives if alt.strip()]
            elif self.local_llm:
                response = self.local_llm(
                    prompt,
                    max_tokens=300,
                    temperature=0.7,
                    stop=["\n\n", "Human:", "Assistant:"]
                )
                alternatives = response["choices"][0]["text"].strip().split('\n')
                return [alt.strip() for alt in alternatives if alt.strip()]
            else:
                return []
        except Exception as e:
            logger.error(f"AI alternatives failed: {e}")
            return []
    
    def validate_command(self, command: str) -> Dict[str, Any]:
        """Validate a shell command for safety and legality"""
        dangerous_patterns = [
            r'rm\s+-rf\s+/',
            r'dd\s+if=/dev/zero',
            r':\(\)\s*\{\s*:\|:\s*&\s*\}',
            r'chmod\s+777\s+/',
            r'chown\s+root\s+/',
            r'mkfs\s+',
            r'fdisk\s+',
            r'format\s+',
            r'wipe\s+',
            r'shred\s+'
        ]
        
        validation_result = {
            'safe': True,
            'warnings': [],
            'recommendations': []
        }
        
        # Check for dangerous patterns
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                validation_result['safe'] = False
                validation_result['warnings'].append(f"Dangerous command pattern detected: {pattern}")
        
        # Check for network scanning without target specification
        if 'nmap' in command and not re.search(r'\d+\.\d+\.\d+\.\d+', command):
            validation_result['warnings'].append("Network scan without specific target - ensure you have authorization")
        
        # Check for password attacks
        if any(tool in command.lower() for tool in ['hydra', 'john', 'hashcat']):
            validation_result['warnings'].append("Password attack tool detected - ensure you have authorization")
        
        # Check for web attacks
        if any(tool in command.lower() for tool in ['sqlmap', 'nikto', 'dirb']):
            validation_result['warnings'].append("Web security tool detected - ensure you have authorization")
        
        # Add recommendations
        if not validation_result['warnings']:
            validation_result['recommendations'].append("Command appears safe for authorized testing")
        else:
            validation_result['recommendations'].append("Review warnings before executing")
            validation_result['recommendations'].append("Ensure you have proper authorization")
            validation_result['recommendations'].append("Test in isolated environment first")
        
        return validation_result 