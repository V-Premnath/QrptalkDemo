# Qryptalk - Post-Quantum Secure Messaging Application

## Overview
Qryptalk is a desktop messaging application designed with post-quantum cryptography to ensure secure communication resistant to quantum computer attacks. It uses CRYSTALS-Kyber for key encapsulation, HKDF for key derivation, and AES-GCM for message encryption.

## Features
- Post-quantum secure key exchange and messaging
- Session management with key rotation
- Encrypted message storage
- User-friendly chat interface
- Secure network communication

## Technology Stack
- Python 3.9+
- PyQt6 for GUI
- pqcrypto for post-quantum cryptography
- cryptography for symmetric encryption
- SQLite (with SQLCipher) for encrypted storage
- asyncio and websockets for networking

## Installation
```bash
pip install -r requirements.txt
```

## Running the Application
```bash
python -m Qryptalk.main
```

## Project Structure
- `Qryptalk/claude/`: Cryptographic foundation (Kyber KEM, key derivation, message crypto)
- `Qryptalk/session/`: Conversation and session management
- `Qryptalk/network/`: Network protocol and client
- `Qryptalk/storage/`: Database, key store, and repository
- `Qryptalk/ui/`: User interface components
- `Qryptalk/main.py`: Application entry point

## Testing
Run tests with:
```bash
pytest
```

## Next Steps
- Implement session management and network protocol
- Develop UI components with PyQt6
- Add comprehensive unit and integration tests
- Perform security and performance testing

## License
MIT License

## Contact
QrypTalk Development Team
