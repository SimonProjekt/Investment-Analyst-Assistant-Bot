# 🧠 Investment Analyst Assistant Bot

En Telegram-bot byggd med FastAPI, LangChain, OpenAI GPT-4 och ChromaDB för att agera som en investment analyst-assistent.  
Den svarar på frågor om tre specifika bolag baserat på inlästa delårsrapporter i `.md`-format.

---

## 💼 Syfte

Projektet är skapat som ett MVP för att:
- Demonstrera ett RAG-baserat analyst-stöd till PE/investeringsorganisationer
- Testa snabb insiktsgenerering baserat på faktisk rapportdata
- Automatisera enkla analyst-frågor, SWOT-analyser, och jämförelser

---

## 🧱 Teknikstack

- **Python** (FastAPI)
- **LangChain** (Retrieval-Augmented Generation)
- **OpenAI GPT-4**
- **ChromaDB** (lokal vektor-databas)
- **Telegram Bot API**
- **Docker** (containeriserad med build.sh)
- **Render** (hosting)

---

## 🧠 Funktioner

| Kommando | Beskrivning |
|----------|-------------|
| `/start` | Introduktion och exempel på frågor |
| `/help` | Förklaring av vad boten kan hjälpa till med |
| `/summary <bolag>` | Skickar en koncis analys av bolaget |
| `/compare <bolag1> <bolag2>` | Jämför två bolag sida vid sida |
| Vanlig fråga | Fritt formulerad fråga, t.ex. "Vilka risker nämner Apotea?" |

---

## 🚀 Quick Start
Chatta med boten här: 🔗 (https://t.me/investment_analyst_assistant_bot)