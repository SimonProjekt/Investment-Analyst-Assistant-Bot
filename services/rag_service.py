from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate

class ChromaCompatibleEmbeddings:
    def __init__(self, embeddings_model):
        self.embeddings_model = embeddings_model

    def __call__(self, input):
        return self.embeddings_model.embed_documents(input)

    def embed_documents(self, texts):
        return self.embeddings_model.embed_documents(texts)

    def embed_query(self, text):
        return self.embeddings_model.embed_query(text)

def get_qa_chain():
    original_embeddings = OpenAIEmbeddings()
    compatible_embeddings = ChromaCompatibleEmbeddings(original_embeddings)

    db = Chroma(
        persist_directory="db",
        embedding_function=compatible_embeddings
    )

    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 10})
    llm = ChatOpenAI(model="gpt-4")

    # ✅ FIXAD PROMPT
    template = """
    Du är en mycket skicklig och pålitlig investment analyst assistant. 
    Din uppgift är att hjälpa användaren att förstå företagens affärsmodell, finansiella utveckling och strategiska läge utifrån innehållet i de tillgängliga rapporterna.

    Använd följande kontext för att svara:
    {context}

    Svara:
    - med konkreta observationer från rapportmaterialet
    - i ett professionellt och koncist språk
    - utan att spekulera utanför det som faktiskt nämns i rapporterna

    Om något inte framgår i materialet, säg det tydligt.

    Fråga: {question}
    """

    prompt = PromptTemplate.from_template(template)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain
