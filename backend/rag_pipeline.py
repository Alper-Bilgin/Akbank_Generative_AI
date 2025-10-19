import os
import shutil
from hashlib import md5
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")


def _format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


def build_or_load_pipeline(documents, recreate_index=False, k=5):
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY .env içinde tanımlı değil.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = documents or []
    chunks = text_splitter.split_documents(docs)
    embedding_function = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    if recreate_index and os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    if not os.path.exists(CHROMA_PATH):
        print("Vektör veritabanı oluşturuluyor... (Bu işlem biraz zaman alabilir)")
        vectorstore = Chroma.from_documents(chunks, embedding_function, persist_directory=CHROMA_PATH)
        print("Veritabanı başarıyla oluşturuldu.")
    else:
        print(f"Mevcut vektör veritabanı kullanılıyor: {CHROMA_PATH}")
        vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        if chunks:
            try:
                vectorstore.add_documents(chunks)
                print("Yeni parçalar eklendi.")
            except Exception as e:
                print(f"Parça ekleme hatası: {e}")

    retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

    template = (
        "Sana verilen metin parçalarını kullanarak soruları yanıtlayan bir haber asistanısın. "
        "Sadece aşağıdaki bağlamı kullanarak cevap ver. Cevabı bilmiyorsan, 'Bu konuda bilgim yok.' de.\n"
        "Bağlam:\n{context}\n\nSoru: {question}\nCevap:"
    )
    prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {
            "context": retriever | RunnableLambda(_format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain
