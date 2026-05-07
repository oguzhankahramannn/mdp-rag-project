import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


CHROMA_PATH = "chromadb_store"

class MDP_RAG_Engine:
    def __init__(self):
        # DİKKAT: create_db.py'de hangi embedding modelini kullandıysan buraya da aynısını yazmalısın.
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

        
        # Oluşturduğumuz kalıcı veritabanına bağlan
        self.db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embeddings)
        self.retriever = self.db.as_retriever(search_kwargs={"k": 4})
        
        # Gemini 2.0 Flash'ı devreye sokuyoruz (temperature=0.1 ile uydurmayı minimuma indiriyoruz)
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
        #self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.1)
        
        # Asistanın Karakteri ve Kuralları
        self.prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "Sen MDP Group için çalışan profesyonel, yardımsever ve bilgi küpü bir kurumsal yapay zeka asistanısın. "
         "Kullanıcılara sanki yıllardır bu şirkette çalışıyormuşsun gibi doğal, akıcı ve kendinden emin bir dille cevap ver.\n\n"
         "Sana sağlanan arka plan bilgilerini ({context}) kullanarak yanıt üret ancak ASLA 'bana verilen bağlama göre', 'metinde belirtildiği üzere', 'bağlamda geçmiyor' veya 'sağlanan bilgiye göre' gibi ifadeler kullanma. "
         "Bilgiyi doğrudan, kendi doğal bilginmiş gibi sun.\n\n"
         "Eğer sorunun cevabı elindeki bilgilerde kesinlikle yoksa, asla uydurma (halüsinasyon) yapma. Konuyu kibarca toparla ve sadece şu cümleyi kur: "
         "'Bu konuda detaylı bilgi almak için info@mdpgroup.com adresine yazabilirsiniz.'\n\n"
         "İletişim, telefon veya iletişim numarası sorulursa MUTLAKA tıklanabilir olarak şu numaraları ver:\n"
         "Türkiye: <a href='tel:+902161234567'>+90 216 123 45 67</a>\n"
         "İsviçre: <a href='tel:+41441234567'>+41 44 123 45 67</a>\n\n"
         "Arka Plan Bilgisi:\n{context}"),
         ("human", "{input}")
])
        
        self.qa_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, self.qa_chain)

    def ask_to_bot(self, user_query: str):
        response = self.rag_chain.invoke({"input": user_query})
        return response["answer"]

# Diğer dosyalar bu motoru kullanabilsin diye dışarı aktarıyoruz
engine = MDP_RAG_Engine()