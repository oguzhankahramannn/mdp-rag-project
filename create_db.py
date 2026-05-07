import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# .env dosyasındaki API anahtarını yükle
load_dotenv()

DATA_PATH = "data"
CHROMA_PATH = "chromadb_store"

def generate_data_store():
    print("1. 'data' klasöründeki metinler okunuyor...")
    # Dosya adındaki .txt.txt uzantısını dert etmemek için genel bir arama yapıyoruz
    loader = DirectoryLoader(DATA_PATH, glob="*.*", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    documents = loader.load()

    print(f"2. Metinler parçalanıyor... (Okunan belge sayısı: {len(documents)})")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    print(f"3. Vektör veritabanı (Chroma) oluşturuluyor... (Toplam Parça: {len(chunks)})")
    # Gemini'nin yerleştirme (embedding) modelini kullanıyoruz
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    
    # Verileri ChromaDB'ye yaz ve klasöre kaydet
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=CHROMA_PATH
    )
    print(" Veritabanı başarıyla oluşturuldu! (Sol tarafta 'chromadb_store' klasörünü görebilirsin)")

if __name__ == "__main__":
    generate_data_store()