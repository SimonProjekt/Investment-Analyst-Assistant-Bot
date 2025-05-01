from fastapi import FastAPI, Request
from models.query_request import QueryRequest
from services.telegram_service import send_telegram_message, send_typing_action
from services.rag_service import get_qa_chain
from utils.load_env import load_environment_variables
from services.database_service import create_database
import uvicorn
import os

# Starta om Chroma om db/ saknas
if not os.path.exists("db") or not os.listdir("db"):
    print("🛠️ Ingen db hittades, bygger om...")
    create_database()
else:
    print("✅ db/ hittades, fortsätter...")

# Ladda miljövariabler
load_environment_variables()

# Initiera FastAPI och QA-chain
app = FastAPI()
qa_chain = get_qa_chain()

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    try:
        print(f"🔎 Fråga mottagen: {request.query}")
        result = qa_chain({"query": request.query})
        print(f"✅ Svar genererat.")
        return {
            "answer": result["result"],
            "sources": [doc.page_content for doc in result["source_documents"]]
        }
    except Exception as e:
        print(f"❌ Fel i /query-endpointen: {e}")
        return {"error": str(e)}


@app.post("/webhook")
async def telegram_webhook(request: Request):
    body = await request.json()
    print("Telegram-meddelande mottaget:", body)

    try:
        chat_id = body["message"]["chat"]["id"]
        message_text = body["message"]["text"].strip().lower()

        print(f"Användaren skrev: {message_text}")

        send_typing_action(chat_id)

        if message_text == "/start":
            welcome_message = (
                "Hej! 👋 Jag är din Investment Analyst Assistant.\n\n"
        "Just nu har jag tillgång till tre rapporter:\n"
        "📄 Yubico\n📄 Apotea\n📄 Asmode\n\n"
        "Jag svarar endast baserat på innehållet i dessa rapporter – inget annat. "
        "Använd mig för att snabbt få ut insikter ur materialet.\n\n"
        "Du kan t.ex. skriva frågor som:\n"
        "- Gör en SWOT-analys på Yubico\n"
        "- Vad är tillväxtstrategin för Apotea?\n"
        "- Är Asmode en attraktiv investering?\n\n"
        "Skriv /help om du vill veta vad jag mer kan hjälpa dig med."
            )
            send_telegram_message(chat_id, welcome_message)

        elif message_text == "/help":
            help_message = (
                 "📊 Jag hjälper dig analysera företagsrapporter baserat på följande tre bolag:\n"
        "- Yubico\n- Apotea\n- Asmode\n\n"
        "🔎 Jag är optimerad för att besvara:\n"
        "- SWOT-analyser\n"
        "- Tillväxtstrategier\n"
        "- Marknadsposition och affärsmodell\n"
        "- Risker, möjligheter och investeringsattraktivitet\n\n"
        "- Skriv /summary <bolag> för en investeringssammanfattning\n"
        "  t.ex. /summary yubico\n"
        "- /compare <bolag1> <bolag2>: jämför två bolag\n"
        "  t.ex. /compare apotea yubico\n"

        "📌 Exempelfrågor:\n"
        "- Gör en SWOT-analys på Yubico\n"
        "- Vad är Apoteas strategi för fortsatt tillväxt?\n"
        "- Vilka risker lyfter Asmode fram?\n\n"
        "Ställ din fråga direkt, så hjälper jag dig så gott jag kan!"
            )
            send_telegram_message(chat_id, help_message)
        
        elif message_text.startswith("/summary"):
            # Extrahera bolagsnamn
            parts = message_text.split()
            if len(parts) < 2:
                send_telegram_message(chat_id, "Ange ett bolagsnamn, t.ex. /summary apotea")
            else:
                company = parts[1].capitalize()

                prompt = (
                    f"Gör en sammanfattning av bolaget {company} baserat på rapporten.\n"
                    f"Beskriv:\n"
                    f"- Affärsmodell\n"
                    f"- Marknadsposition\n"
                    f"- Tillväxtstrategi\n"
                    f"- Risker\n"
                    f"- Möjligheter\n"
                    f"Svara koncist och investeringsorienterat."
                )

                response = qa_chain.invoke({"query": prompt})
                answer = response["result"]

                send_telegram_message(chat_id, f"📊 Sammanfattning av {company}:\n\n{answer}")
        
        
        elif message_text.startswith("/compare"):
            parts = message_text.split()
            if len(parts) < 3:
                send_telegram_message(chat_id, "Använd: /compare <bolag1> <bolag2>\nExempel: /compare apotea yubico")
            else:
                company1 = parts[1].capitalize()
                company2 = parts[2].capitalize()

                prompt = (
                    f"Jämför bolagen {company1} och {company2} baserat på tillgängliga rapporter.\n"
                    f"Beskriv skillnader och likheter inom:\n"
                    f"- Affärsmodell\n"
                    f"- Tillväxtstrategi\n"
                    f"- Risker och möjligheter\n"
                    f"- Investeringsattraktivitet\n"
                    f"Svara strukturerat och koncist."
                )

                response = qa_chain.invoke({"query": prompt})
                answer = response["result"]

                send_telegram_message(chat_id, f"📊 Jämförelse mellan {company1} och {company2}:\n\n{answer}")



        

        else:
            # Vanlig fråga till RAG
            response = qa_chain.invoke({"query": message_text})
            answer = response["result"]

            print(f"Svar från RAG: {answer}")

            send_telegram_message(chat_id, answer)

        return {"status": "Message processed"}

    except Exception as e:
        print("Fel vid hantering av Telegram-meddelande:", str(e))
        return {"status": "error", "message": str(e)}

# Kör lokalt
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
