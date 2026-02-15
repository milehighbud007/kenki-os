#!/usr/bin/env python3
"""
KENKI OS - Command Explanation Module
Provides detailed explanations of Linux and security commands
"""

import re
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class CommandExplainer:
    """Explains Linux and security commands using AI"""
    
    def __init__(self, claude_client=None, local_llm=None):
        self.claude_client = claude_client
        self.local_llm = local_llm
        
        # Common security tools for enhanced explanations
        self.security_tools = {
            'nmap': self._explain_nmap,
            'metasploit': self._explain_metasploit,
            'sqlmap': self._explain_sqlmap,
            'hydra': self._explain_hydra,
            'aircrack-ng': self._explain_aircrack,
            'wireshark': self._explain_wireshark,
            'tcpdump': self._explain_tcpdump,
            'netcat': self._explain_netcat,
            'john': self._explain_john,
            'hashcat': self._explain_hashcat,
            'volatility': self._explain_volatility,
            'ghidra': self._explain_ghidra,
            'radare2': self._explain_radare2,
            'beef': self._explain_beef,
            'maltego': self._explain_maltego,
            'recon-ng': self._explain_recon_ng,
            'theharvester': self._explain_theharvester,
            'amass': self._explain_amass,
            'dirb': self._explain_dirb,
            'nikto': self._explain_nikto,
            'wpscan': self._explain_wpscan,
            'joomscan': self._explain_joomscan,
            'skipfish': self._explain_skipfish,
            'w3af': self._explain_w3af,
            'zap': self._explain_zap,
            'burp': self._explain_burp,
            'nessus': self._explain_nessus,
            'openvas': self._explain_openvas
        }
    
    def explain(self, command: str) -> str:
        """Explain a command using AI"""
        if not command.strip():
            return "❌ Please provide a command to explain."
        
        # Clean the command
        command = command.strip()
        
        # Extract the main command (first word)
        main_command = command.split()[0] if command.split() else ""
        
        # Check if it's a security tool with specialized explanation
        if main_command in self.security_tools:
            return self.security_tools[main_command](command)
        
        # Use AI for general command explanation
        return self._explain_with_ai(command)
    
    def _explain_with_ai(self, command: str) -> str:
        """Use AI to explain a command"""
        prompt = f"""
        Explain this Linux/Unix command in detail for a security professional:
        
        Command: {command}
        
        Please provide:
        1. What the command does
        2. What each flag/parameter means
        3. Common use cases in security testing
        4. Potential risks or considerations
        5. Related commands or alternatives
        
        Format the response clearly with sections and examples.
        """
        
        try:
            if self.claude_client:
                response = self.claude_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1000,
                    temperature=0.7,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            elif self.local_llm:
                response = self.local_llm(
                    prompt,
                    max_tokens=1000,
                    temperature=0.7,
                    stop=["\n\n", "Human:", "Assistant:"]
                )
                return response["choices"][0]["text"]
            else:
                return self._fallback_explanation(command)
        except Exception as e:
            logger.error(f"AI explanation failed: {e}")
            return self._fallback_explanation(command)
    
    def _fallback_explanation(self, command: str) -> str:
        """Fallback explanation when AI is not available"""
        return f"""
        📋 Command: {command}
        
        🔍 Basic Explanation:
        This appears to be a Linux/Unix command. Without AI assistance, I can't provide a detailed explanation.
        
        💡 Tips:
        - Use 'man <command>' for manual pages
        - Use '--help' flag for built-in help
        - Check online documentation for detailed usage
        
        🛠️ To get AI-powered explanations, please:
        1. Set up your API keys in config.json
        2. Install required dependencies
        3. Restart the assistant
        """
    
    # Specialized explanations for security tools
    def _explain_nmap(self, command: str) -> str:
        """Explain nmap commands"""
        prompt = f"""
        Explain this nmap command in detail for network security testing:
        
        Command: {command}
        
        Include:
        1. What this specific nmap scan does
        2. Meaning of each flag and parameter
        3. What information it will reveal
        4. Legal and ethical considerations
        5. Common variations and alternatives
        6. Expected output format
        7. Security implications
        
        Focus on practical security testing scenarios.
        """
        return self._get_ai_response(prompt)
    
    def _explain_metasploit(self, command: str) -> str:
        """Explain metasploit commands"""
        prompt = f"""
        Explain this Metasploit command for penetration testing:
        
        Command: {command}
        
        Include:
        1. What this Metasploit module/command does
        2. Target system requirements
        3. Required parameters and options
        4. Expected outcomes and payloads
        5. Legal and ethical considerations
        6. Risk assessment
        7. Post-exploitation steps
        
        Emphasize responsible disclosure and authorized testing only.
        """
        return self._get_ai_response(prompt)
    
    def _explain_sqlmap(self, command: str) -> str:
        """Explain sqlmap commands"""
        prompt = f"""
        Explain this sqlmap command for SQL injection testing:
        
        Command: {command}
        
        Include:
        1. What this sqlmap scan targets
        2. Injection techniques being used
        3. Database fingerprinting process
        4. Data extraction capabilities
        5. Legal and ethical considerations
        6. Responsible disclosure practices
        7. Alternative testing methods
        
        Emphasize authorized testing and responsible disclosure.
        """
        return self._get_ai_response(prompt)
    
    def _explain_hydra(self, command: str) -> str:
        """Explain hydra commands"""
        prompt = f"""
        Explain this Hydra command for brute force testing:
        
        Command: {command}
        
        Include:
        1. What service is being tested
        2. Brute force methodology
        3. Wordlist considerations
        4. Rate limiting and timing
        5. Legal and ethical considerations
        6. Account lockout risks
        7. Alternative testing approaches
        
        Emphasize authorized testing and account protection.
        """
        return self._get_ai_response(prompt)
    
    def _explain_aircrack(self, command: str) -> str:
        """Explain aircrack-ng commands"""
        prompt = f"""
        Explain this aircrack-ng command for wireless security testing:
        
        Command: {command}
        
        Include:
        1. What wireless attack/analysis is being performed
        2. Capture file analysis process
        3. Password cracking methodology
        4. Legal and ethical considerations
        5. Wireless security implications
        6. Countermeasures and protection
        7. Responsible testing practices
        
        Emphasize authorized testing and wireless security awareness.
        """
        return self._get_ai_response(prompt)
    
    def _explain_wireshark(self, command: str) -> str:
        """Explain wireshark commands"""
        prompt = f"""
        Explain this Wireshark command for network analysis:
        
        Command: {command}
        
        Include:
        1. What network traffic is being analyzed
        2. Capture filters and display filters
        3. Protocol analysis capabilities
        4. Security implications of captured data
        5. Privacy considerations
        6. Legal compliance requirements
        7. Network troubleshooting applications
        
        Emphasize privacy protection and authorized monitoring.
        """
        return self._get_ai_response(prompt)
    
    def _explain_tcpdump(self, command: str) -> str:
        """Explain tcpdump commands"""
        prompt = f"""
        Explain this tcpdump command for packet capture:
        
        Command: {command}
        
        Include:
        1. What network traffic is being captured
        2. Filter syntax and options
        3. Output format and analysis
        4. Network troubleshooting applications
        5. Security monitoring capabilities
        6. Legal and privacy considerations
        7. Performance implications
        
        Emphasize authorized monitoring and privacy protection.
        """
        return self._get_ai_response(prompt)
    
    def _explain_netcat(self, command: str) -> str:
        """Explain netcat commands"""
        prompt = f"""
        Explain this netcat command for network connectivity testing:
        
        Command: {command}
        
        Include:
        1. What network operation is being performed
        2. Connection establishment process
        3. Data transfer capabilities
        4. Security testing applications
        5. Network troubleshooting uses
        6. Legal and ethical considerations
        7. Alternative tools and methods
        
        Emphasize authorized testing and network security.
        """
        return self._get_ai_response(prompt)
    
    def _explain_john(self, command: str) -> str:
        """Explain john commands"""
        prompt = f"""
        Explain this John the Ripper command for password cracking:
        
        Command: {command}
        
        Include:
        1. What password hash is being cracked
        2. Cracking methodology and algorithms
        3. Wordlist and rule-based attacks
        4. Performance considerations
        5. Legal and ethical considerations
        6. Password security implications
        7. Responsible testing practices
        
        Emphasize authorized testing and password security awareness.
        """
        return self._get_ai_response(prompt)
    
    def _explain_hashcat(self, command: str) -> str:
        """Explain hashcat commands"""
        prompt = f"""
        Explain this hashcat command for password recovery:
        
        Command: {command}
        
        Include:
        1. What hash type is being processed
        2. Attack modes and methodologies
        3. Hardware acceleration capabilities
        4. Performance optimization
        5. Legal and ethical considerations
        6. Password security implications
        7. Responsible testing practices
        
        Emphasize authorized testing and password security.
        """
        return self._get_ai_response(prompt)
    
    def _explain_volatility(self, command: str) -> str:
        """Explain volatility commands"""
        prompt = f"""
        Explain this Volatility command for memory forensics:
        
        Command: {command}
        
        Include:
        1. What memory analysis is being performed
        2. Memory dump analysis process
        3. Malware detection capabilities
        4. Forensic investigation applications
        5. Legal and compliance considerations
        6. Evidence handling procedures
        7. Incident response applications
        
        Emphasize forensic integrity and legal compliance.
        """
        return self._get_ai_response(prompt)
    
    def _explain_ghidra(self, command: str) -> str:
        """Explain ghidra commands"""
        prompt = f"""
        Explain this Ghidra command for reverse engineering:
        
        Command: {command}
        
        Include:
        1. What binary analysis is being performed
        2. Disassembly and decompilation process
        3. Malware analysis capabilities
        4. Vulnerability research applications
        5. Legal and ethical considerations
        6. Intellectual property concerns
        7. Responsible disclosure practices
        
        Emphasize authorized analysis and legal compliance.
        """
        return self._get_ai_response(prompt)
    
    def _explain_radare2(self, command: str) -> str:
        """Explain radare2 commands"""
        prompt = f"""
        Explain this radare2 command for binary analysis:
        
        Command: {command}
        
        Include:
        1. What binary analysis is being performed
        2. Disassembly and debugging capabilities
        3. Malware analysis applications
        4. Vulnerability research uses
        5. Legal and ethical considerations
        6. Reverse engineering techniques
        7. Responsible analysis practices
        
        Emphasize authorized analysis and legal compliance.
        """
        return self._get_ai_response(prompt)
    
    def _explain_beef(self, command: str) -> str:
        """Explain beef commands"""
        prompt = f"""
        Explain this BeEF command for browser exploitation:
        
        Command: {command}
        
        Include:
        1. What browser exploitation is being performed
        2. Client-side attack methodology
        3. JavaScript injection techniques
        4. Legal and ethical considerations
        5. Responsible testing practices
        6. Browser security implications
        7. Alternative testing approaches
        
        Emphasize authorized testing and responsible disclosure.
        """
        return self._get_ai_response(prompt)
    
    def _explain_maltego(self, command: str) -> str:
        """Explain maltego commands"""
        prompt = f"""
        Explain this Maltego command for OSINT gathering:
        
        Command: {command}
        
        Include:
        1. What OSINT investigation is being performed
        2. Data collection and correlation process
        3. Privacy and legal considerations
        4. Responsible information gathering
        5. Threat intelligence applications
        6. Data protection requirements
        7. Ethical investigation practices
        
        Emphasize privacy protection and authorized investigation.
        """
        return self._get_ai_response(prompt)
    
    def _explain_recon_ng(self, command: str) -> str:
        """Explain recon-ng commands"""
        prompt = f"""
        Explain this Recon-ng command for reconnaissance:
        
        Command: {command}
        
        Include:
        1. What reconnaissance is being performed
        2. Information gathering methodology
        3. OSINT techniques and sources
        4. Legal and ethical considerations
        5. Responsible investigation practices
        6. Threat intelligence applications
        7. Privacy protection measures
        
        Emphasize authorized investigation and privacy protection.
        """
        return self._get_ai_response(prompt)
    
    def _explain_theharvester(self, command: str) -> str:
        """Explain theharvester commands"""
        prompt = f"""
        Explain this theHarvester command for email enumeration:
        
        Command: {command}
        
        Include:
        1. What email enumeration is being performed
        2. Data source collection process
        3. Privacy and legal considerations
        4. Responsible information gathering
        5. OSINT applications
        6. Data protection requirements
        7. Ethical investigation practices
        
        Emphasize privacy protection and authorized investigation.
        """
        return self._get_ai_response(prompt)
    
    def _explain_amass(self, command: str) -> str:
        """Explain amass commands"""
        prompt = f"""
        Explain this Amass command for subdomain enumeration:
        
        Command: {command}
        
        Include:
        1. What subdomain enumeration is being performed
        2. DNS reconnaissance methodology
        3. Data source integration
        4. Legal and ethical considerations
        5. Responsible investigation practices
        6. Attack surface mapping applications
        7. Privacy protection measures
        
        Emphasize authorized investigation and responsible disclosure.
        """
        return self._get_ai_response(prompt)
    
    def _explain_dirb(self, command: str) -> str:
        """Explain dirb commands"""
        prompt = f"""
        Explain this dirb command for directory enumeration:
        
        Command: {command}
        
        Include:
        1. What directory enumeration is being performed
        2. Web crawling methodology
        3. Wordlist-based discovery
        4. Legal and ethical considerations
        5. Responsible testing practices
        6. Web application security implications
        7. Alternative testing approaches
        
        Emphasize authorized testing and responsible disclosure.
        """
        return self._get_ai_response(prompt)
    
    def _explain_nikto(self, command: str) -> str:
        """Explain nikto commands"""
        prompt = f"""
        Explain this Nikto command for web vulnerability scanning:
        
        Command: {command}
        
        Include:
        1. What web vulnerability scan is being performed
        2. Security test methodology
        3. Vulnerability detection capabilities
        4. Legal and ethical considerations
        5. Responsible testing practices
        6. Web application security implications
        7. Alternative testing approaches
        
        Emphasize authorized testing and responsible disclosure.
        """
        return self._get_ai_response(prompt)
    
    def _explain_wpscan(self, command: str) -> str:
        """Explain wpscan commands"""
        prompt = f"""
        Explain this WPScan command for WordPress security testing:
        
        Command: {command}
        
        Include:
        1. What WordPress security scan is being performed
        2. Vulnerability detection methodology
        3. Plugin and theme analysis
        4. Legal and ethical considerations
        5. Responsible testing practices
        6. WordPress security implications
        7. Alternative testing approaches
        
        Emphasize authorized testing and responsible disclosure.
        """
        return self._get_ai_response(prompt)
    
    def _explain_joomscan(self, command: str) -> str:
        """Explain joomscan commands"""
        prompt = f"""
        Explain this JoomScan command for Joomla security testing:
        
        Command: {command}
        
        Include:
        1. What Joomla security scan is being performed
        2. Vulnerability detection methodology
        3. Component and extension analysis
        4. Legal and ethical considerations
        5. Responsible testing practices
        6. Joomla security implications
        7. Alternative testing approaches
        
        Emphasize authorized testing and responsible disclosure.
        """
        return self._get_ai_response(prompt)
    
    def _explain_skipfish(self, command: str) -> str:
        """Explain skipfish commands"""
        prompt = f"""
        Explain this Skipfish command for web application security testing:
        
        Command: {command}
        
        Include:
        1. What web application security scan is being performed
        2. Crawling and testing methodology
        3. Vulnerability detection capabilities
        4. Legal and ethical considerations
        5. Responsible testing practices
        6. Web application security implications
        7. Alternative testing approaches
        
        Emphasize authorized testing and responsible disclosure.
        """
        return self._get_ai_response(prompt)
    
    def _explain_w3af(self, command: str) -> str:
        """Explain w3af commands"""
        prompt = f"""
        Explain this w3af command for web application security testing:
        
        Command: {command}
        
        Include:
        1. What web application security scan is being performed
        2. Vulnerability detection methodology
        3. Plugin-based testing approach
        4. Legal and ethical considerations
        5. Responsible testing practices
        6. Web application security implications
        7. Alternative testing approaches
        
        Emphasize authorized testing and responsible disclosure.
        """
        return self._get_ai_response(prompt)
    
    def _explain_zap(self, command: str) -> str:
        """Explain OWASP ZAP commands"""
        prompt = f"""
        Explain this OWASP ZAP command for web application security testing:
        
        Command: {command}
        
        Include:
        1. What web application security scan is being performed
        2. Vulnerability detection methodology
        3. Automated and manual testing capabilities
        4. Legal and ethical considerations
        5. Responsible testing practices
        6. Web application security implications
        7. Alternative testing approaches
        
        Emphasize authorized testing and responsible disclosure.
        """
        return self._get_ai_response(prompt)
    
    def _explain_burp(self, command: str) -> str:
        """Explain Burp Suite commands"""
        prompt = f"""
        Explain this Burp Suite command for web application security testing:
        
        Command: {command}
        
        Include:
        1. What web application security test is being performed
        2. Proxy and interception capabilities
        3. Vulnerability detection methodology
        4. Legal and ethical considerations
        5. Responsible testing practices
        6. Web application security implications
        7. Alternative testing approaches
        
        Emphasize authorized testing and responsible disclosure.
        """
        return self._get_ai_response(prompt)
    
    def _explain_nessus(self, command: str) -> str:
        """Explain Nessus commands"""
        prompt = f"""
        Explain this Nessus command for vulnerability scanning:
        
        Command: {command}
        
        Include:
        1. What vulnerability scan is being performed
        2. Network and application testing methodology
        3. Vulnerability detection capabilities
        4. Legal and ethical considerations
        5. Responsible testing practices
        6. Security assessment implications
        7. Alternative testing approaches
        
        Emphasize authorized testing and responsible disclosure.
        """
        return self._get_ai_response(prompt)
    
    def _explain_openvas(self, command: str) -> str:
        """Explain OpenVAS commands"""
        prompt = f"""
        Explain this OpenVAS command for vulnerability scanning:
        
        Command: {command}
        
        Include:
        1. What vulnerability scan is being performed
        2. Network and application testing methodology
        3. Vulnerability detection capabilities
        4. Legal and ethical considerations
        5. Responsible testing practices
        6. Security assessment implications
        7. Alternative testing approaches
        
        Emphasize authorized testing and responsible disclosure.
        """
        return self._get_ai_response(prompt)
    
    def _get_ai_response(self, prompt: str) -> str:
        """Get response from available AI models"""
        try:
            if self.claude_client:
                response = self.claude_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1000,
                    temperature=0.7,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            elif self.local_llm:
                response = self.local_llm(
                    prompt,
                    max_tokens=1000,
                    temperature=0.7,
                    stop=["\n\n", "Human:", "Assistant:"]
                )
                return response["choices"][0]["text"]
            else:
                return self._fallback_explanation("AI not available")
        except Exception as e:
            logger.error(f"AI response failed: {e}")
            return self._fallback_explanation("AI error occurred") 