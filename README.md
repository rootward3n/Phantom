<div align="center">

# 👻 PHANTOM

### Next-Generation Modular AI Assistant

**Fast • Intelligent • Extensible • Terminal First**

<p>
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20Ubuntu-success?style=for-the-badge">
<img src="https://img.shields.io/badge/UI-Rich-blueviolet?style=for-the-badge">
<img src="https://img.shields.io/badge/AI-Google%20Gemini-orange?style=for-the-badge">
<img src="https://img.shields.io/badge/Status-Active%20Development-green?style=for-the-badge">
<img src="https://img.shields.io/badge/License-MIT-red?style=for-the-badge">
</p>

*"Building a powerful developer AI assistant from scratch in Python."*

</div>

---

# 🚀 About

**PHANTOM** is a modern AI assistant built with Python that combines powerful language models with local tools, memory, filesystem access, and an elegant Rich terminal interface.

Unlike a normal chatbot, Phantom is designed as a **modular AI operating system** that can understand, reason, manipulate files, execute tools, and grow into a fully autonomous assistant.

---

# ✨ Features

## 🤖 AI Core

- Google Gemini Integration
- Streaming Responses
- AI Tool Calling
- Prompt Engineering
- Modular Provider Architecture

---

## 🧠 Memory

- Persistent Memory
- Conversation History
- JSON Storage
- Recall Memories
- Forget Memories

---

## 📂 Filesystem

- 📖 Read Files
- ✍ Write Files
- ➕ Append Files
- 📂 Create Directories
- 🗑 Delete Files
- 📋 Copy Files
- 🚚 Move Files
- 🌳 Directory Tree
- 📄 File Information
- 🔍 Search Files
- 📍 Current Directory
- 🏠 Workspace Navigation

---

## 🎨 Rich Terminal Interface

- 🌌 Beautiful Startup Screen
- 👻 Cyberpunk Banner
- 🎨 Rich Panels
- 📊 Rich Tables
- 📝 Markdown Rendering
- ⚡ Live Streaming
- ⏳ Thinking Spinner
- 🌈 Color Themes
- 😊 Emoji Support

---

# 📁 Project Structure

```text
Phantom
│
├── assistant.py
├── brain.py
├── commands.py
├── config.py
├── history.py
├── logger.py
├── main.py
├── memory.py
├── prompts.py
│
├── providers/
│
├── tools/
│   ├── filesystem/
│   ├── manager.py
│   └── ...
│
├── ui/
│
├── data/
│
├── logs/
│
└── requirements.txt
```

---

# ⚡ Installation

Clone repository

```bash
git clone https://github.com/USERNAME/Phantom.git
```

Enter project

```bash
cd Phantom
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create `.env`

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

Run Phantom

```bash
python3 main.py
```

Launch the Textual TUI:

```bash
python3 main.py --tui
```

---

# 💻 Commands

## System

| Command | Description |
|---------|-------------|
| `/help` | Show Help |
| `/status` | System Status |
| `/version` | Version |
| `/model` | Current Model |
| `/clear` | Clear Terminal |
| `/exit` | Exit Phantom |

---

## Memory

| Command | Description |
|---------|-------------|
| `/memory` | Show Memory |
| `/remember` | Save Memory |
| `/forget` | Delete Memory |

---

## Filesystem

| Command | Description |
|---------|-------------|
| `/read` | Read File |
| `/write` | Write File |
| `/append` | Append File |
| `/mkdir` | Create Folder |
| `/rmdir` | Remove Folder |
| `/cp` | Copy File |
| `/mv` | Move File |
| `/rm` | Delete File |
| `/pwd` | Current Directory |
| `/cd` | Change Directory |
| `/home` | Workspace Root |
| `/ls` | List Files |
| `/tree` | Directory Tree |
| `/find` | Search Files |
| `/info` | File Information |

---

# 🏗️ Architecture

```text
                 👤 User
                    │
                    ▼
              Command Handler
                    │
     ┌──────────────┴──────────────┐
     │                             │
     ▼                             ▼
Slash Commands                AI Assistant
     │                             │
     ▼                             ▼
 Tool Manager                Google Gemini
     │                             │
     └──────────────┬──────────────┘
                    ▼
            Filesystem & Memory
```

---

# 📊 Development Progress

## ✅ Milestone 1 — Project Setup

████████████████████ 100%

## ✅ Milestone 2 — Gemini Integration

████████████████████ 100%

## ✅ Milestone 3 — Streaming Responses

████████████████████ 100%

## ✅ Milestone 4 — Memory System

████████████████████ 100%

## ✅ Milestone 5 — Conversation History

████████████████████ 100%

## ✅ Milestone 6 — Logging

████████████████████ 100%

## ✅ Milestone 7 — Command Framework

████████████████████ 100%

## ✅ Milestone 8 — File Toolkit

████████████████████ 100%

## ✅ Milestone 9 — Filesystem Navigation

████████████████████ 100%

## ✅ Milestone 10 — Workspace Management

████████████████████ 100%

## ✅ Milestone 11 — Tool Manager

████████████████████ 100%

## ✅ Milestone 12 — AI Tool Calling

████████████████████ 100%

## 🚧 Milestone 13 — Rich Terminal UI

██████████████████░░ 90%

### Completed

- ✅ Rich Console
- ✅ Cyberpunk Banner
- ✅ Startup Dashboard
- ✅ Rich Prompt
- ✅ Rich Panels
- ✅ Rich Tables
- ✅ Emoji Support
- ✅ Spinner
- ✅ Streaming Output
- ✅ Markdown Rendering

### Remaining

- 🔄 Theme Switching
- 🔄 Live Dashboard
- 🔄 Command Auto-completion

---

# 🗺️ Roadmap

| Milestone | Status |
|------------|--------|
| 1️⃣ Core Setup | ✅ |
| 2️⃣ Gemini Integration | ✅ |
| 3️⃣ Streaming | ✅ |
| 4️⃣ Memory | ✅ |
| 5️⃣ History | ✅ |
| 6️⃣ Logging | ✅ |
| 7️⃣ Commands | ✅ |
| 8️⃣ Filesystem | ✅ |
| 9️⃣ Navigation | ✅ |
| 🔟 Workspace | ✅ |
| 1️⃣1️⃣ Tool Manager | ✅ |
| 1️⃣2️⃣ AI Tool Calling | ✅ |
| 1️⃣3️⃣ Rich CLI | 🚧 |
| 1️⃣4️⃣ Multi Provider AI | 📅 |
| 1️⃣5️⃣ Knowledge Base (RAG) | 📅 |
| 1️⃣6️⃣ Plugin System | 📅 |
| 1️⃣7️⃣ FastAPI Backend | 📅 |
| 1️⃣8️⃣ Web Dashboard | 📅 |
| 1️⃣9️⃣ Voice Assistant | 📅 |
| 2️⃣0️⃣ Phantom v1.0 | 🎯 |

---

# 🛠️ Tech Stack

### Language

- 🐍 Python

### AI

- 🤖 Google Gemini

### Terminal

- 🎨 Rich

### Storage

- 💾 JSON

### Networking

- 🌐 Requests

### Configuration

- ⚙ python-dotenv

---

# 🎯 Vision

Phantom aims to become a complete AI operating environment capable of:

- 🤖 AI Reasoning
- 🧠 Long-Term Memory
- 📚 Knowledge Base (RAG)
- 🔌 Plugin System
- 🌐 Web Dashboard
- 🎤 Voice Interaction
- 📱 Android Support
- ⚡ Autonomous Task Execution

---

# 🤝 Contributing

Contributions, ideas, feature requests, and bug reports are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

# 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

## 👻 PHANTOM

### *"Code. Learn. Evolve."*

⭐ If you like Phantom, consider starring the repository!

Made with ❤️ and Python.

</div>
