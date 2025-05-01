import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from services.rag_service import ChromaCompatibleEmbeddings

def create_database():
    file_paths = [
        os.path.join("data", "apotea.md"),
        os.path.join("data", "asmode.md"),
        os.path.join("data", "yubico.md")
    ]

    documents = []
    for path in file_paths:
        if os.path.exists(path):
            print(f"🔄 Läser in: {path}")
            loader = TextLoader(path)
            docs = loader.load()
            documents.extend(docs)
        else:
            print(f"⚠️ Fil saknas: {path}")

    if not documents:
        raise RuntimeError("❌ Inga dokument laddades in. Kontrollera att markdown-filerna finns i data/")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(documents)
    print(f"🧩 Antal chunkade dokument: {len(documents)}")

    original_embeddings = OpenAIEmbeddings()
    embeddings = ChromaCompatibleEmbeddings(original_embeddings)

    db = Chroma.from_documents(
        documents,
        embedding=embeddings,
        persist_directory="db"
    )
    db.persist()
    print("✅ Databas skapad och sparad i ./db")

if __name__ == "__main__":
    load_dotenv()
    if not os.path.exists("db") or not os.listdir("db"):
        print("🛠️ Ingen db hittades, bygger om...")
        create_database()
    else:
        print("✅ db/ redan finns, använder den.")
