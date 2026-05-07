Bu proje, MDP Group'a ait web sayfalarından [Jina.ai](https://jina.ai) aracılığıyla toplanan metin verilerini kullanarak:

1. **ChromaDB** vektör veritabanında indeksler,
2. **Google Gemini** embedding ve LLM modelleri ile semantik arama yapar,
3. **LangChain** RAG zinciri üzerinden bağlama dayalı, hallüsinasyonsuz yanıtlar üretir.

Kullanıcılar, sisteme hem **Streamlit** web arayüzü hem de **FastAPI** REST API'si hem de statik **HTML** chat widget'ı üzerinden soru sorabilir.

```text
MDP_RAG_Project/
│
├── data/                       # Jina.ai ile toplanan ham metin verileri
│   ├── e_donusum_cozumleri.txt.txt
│   ├── further-sap-add-ons.txt.txt
│   ├── kurumsal.txt.txt
│   ├── mdp-blog.txt.txt
│   ├── mdp-danismanlik.txt.txt
│   ├── mdp-icerikler.txt.txt
│   ├── mdp-iletisim.txt.txt
│   ├── mdp-referanslar.txt.txt
│   ├── mdp-yapayzeka.txt.txt
│   ├── mdp_genel_bilgi.txt.txt
│   ├── non-sap-cozumler.txt.txt
│   ├── sap-fi-add-ones.txt.txt
│   ├── sap-hr-add-ons.txt.txt
│   └── sap-portal-cozumler.txt.txt
│
├── chromadb_store/              # ChromaDB kalıcı vektör veritabanı
│
├── create_db.py                # Veri yükleme ve vektör DB oluşturma scripti
├── rag_engine.py               # RAG zinciri motoru (retriever + LLM)
├── api.py                      # FastAPI REST API sunucusu
├── app.py                      # Streamlit sohbet arayüzü
├── index.html                  # Statik HTML chat widget'ı (Frontend)
├── requirements.txt            # Python bağımlılıkları
├── .env                        # API anahtarı (Git'e dahil edilmez)
└── .gitignore                  # Versiyon kontrolünden hariç tutulan dosyalar
```

## Teknoloji Yığını

| Bileşen | Teknoloji | Açıklama |
| --- | --- | --- |
| **Veri Toplama** | [Jina.ai](https://jina.ai) | MDP Group web sayfalarından metin çıkarma |
| **Embedding Modeli** | `gemini-embedding-001` | Metin parçalarını vektöre dönüştürme |
| **Vektör Veritabanı** | ChromaDB | Vektörlerin kalıcı olarak saklanması ve aranması |
| **LLM** | `gemini-2.5-flash` | Bağlama dayalı doğal dilde yanıt üretimi |
| **RAG Çatısı** | LangChain | Retrieval-Augmented Generation zinciri |
| **Backend API** | FastAPI + Uvicorn | REST API uç noktası (`/ask`) |
| **Web Arayüzü** | Streamlit | İnteraktif sohbet arayüzü |
| **Chat Widget** | Vanilla HTML/CSS/JS | Harici sitelere gömülebilir chat bileşeni |
| **Ortam Yönetimi** | python-dotenv | `.env` üzerinden API anahtarı yönetimi |

---

## Kurulum ve Çalıştırma

### Depoyu Klonla

```bash
git clone [https://github.com/](https://github.com/)<KULLANICI_ADI>/MDP_RAG_Project.git
cd MDP_RAG_Project
```

### Sanal Ortam Oluştur ve Aktifleştir

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### API Anahtarını Yapılandır

Proje kök dizininde bir `.env` dosyası oluşturun:

```env
GOOGLE_API_KEY="BURAYA_KENDI_API_ANAHTARINIZI_YAZIN"
```

> Not: API anahtarınızı [Google AI Studio](https://aistudio.google.com/apikey) üzerinden alabilirsiniz.

### Vektör Veritabanını Oluştur

Bu adım, `data/` klasöründeki metin dosyalarını okuyarak ChromaDB vektör veritabanını oluşturur:

```bash
python create_db.py
```

Başarılı çıktı:

```text
1. 'data' klasöründeki metinler okunuyor...
2. Metinler parçalanıyor... (Okunan belge sayısı: 14)
3. Vektör veritabanı (Chroma) oluşturuluyor... (Toplam Parça: ...)
 Veritabanı başarıyla oluşturuldu!
```

### Uygulamayı Çalıştır

#### Seçenek A: Streamlit Arayüzü

```bash
streamlit run app.py
```

Tarayıcınızda `http://localhost:8501` adresinde açılacaktır.

#### Seçenek B: FastAPI Sunucusu

```bash
uvicorn api:app --reload
```

API `http://localhost:8000` adresinde çalışır. Swagger dokümantasyonuna `http://localhost:8000/docs` üzerinden erişebilirsiniz.

#### Seçenek C: HTML Chat Widget

`index.html` dosyasını doğrudan tarayıcıda açın. Widget, API sunucusuna (`/ask` endpoint) istek gönderir.

> **Not:** HTML widget varsayılan olarak `https://mdp-rag-project.onrender.com/ask` adresine bağlanır. Yerel kullanım için `index.html` içindeki URL'yi `http://localhost:8000/ask` olarak değiştirin.

---

## API Kullanımı

### Endpoint

```http
POST /ask
```

### İstek Gövdesi

```json
{
  "message": "MDP Group hangi alanlarda hizmet veriyor?"
}
```

### Yanıt

```json
{
  "reply": "MDP Group; SAP danışmanlığı, e-Dönüşüm çözümleri, ..."
}
```

### cURL Örneği

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"message": "MDP Group nedir?"}'
```

## Modül Açıklamaları

### `create_db.py`
- `data/` klasöründeki tüm metin dosyalarını `DirectoryLoader` ile yükler.
- `RecursiveCharacterTextSplitter` ile 1000 karakterlik parçalara böler (200 karakter örtüşme).
- `gemini-embedding-001` modeli ile her parçayı vektöre dönüştürür.
- Sonuçları `chromadb_store/` dizinine kalıcı olarak kaydeder.

### `rag_engine.py`
- `MDP_RAG_Engine` sınıfı ile tüm RAG pipeline'ını kapsüller.
- ChromaDB'den en alakalı 4 belge parçasını getirir (`k=4`).
- `gemini-2.5-flash` modelini düşük sıcaklık (`temperature=0.1`) ile kullanarak doğruluk odaklı yanıt üretir.
- Sistem prompt'u: MDP Group çalışanı gibi doğal, kendinden emin yanıtlar verir; bilgi yoksa hallüsinasyon yapmaz, `info@mdpgroup.com` adresine yönlendirir.

### `api.py`
- FastAPI uygulaması oluşturur.
- CORS middleware ile tüm origin'lere izin verir.
- `/ask` POST endpoint'i üzerinden gelen soruları `rag_engine`'e iletir.

### `app.py`
- Streamlit tabanlı interaktif sohbet arayüzü.
- Oturum bazlı mesaj geçmişi tutar.
- Markdown ve HTML formatında yanıtları görüntüler.

### `index.html`
- Bağımsız, gömülebilir chat widget'ı.
- MDP Group kurumsal temasına uygun siyah-sarı tasarım.
- Basit Markdown → HTML dönüştürücü (bold, link, satır sonu).

---

## Veri Kaynakları

Tüm veriler, MDP Group'un kurumsal web sitesinden [Jina.ai Reader](https://jina.ai) API'si kullanılarak çıkarılmış ve `data/` klasöründe `.txt` dosyaları olarak saklanmaktadır:

| Dosya | İçerik |
| --- | --- |
| `mdp_genel_bilgi.txt.txt` | Şirket hakkında genel bilgiler |
| `kurumsal.txt.txt` | Kurumsal yapı ve organizasyon |
| `mdp-danismanlik.txt.txt` | Danışmanlık hizmetleri |
| `e_donusum_cozumleri.txt.txt` | e-Dönüşüm çözümleri |
| `sap-fi-add-ones.txt.txt` | SAP FI ek çözümleri |
| `sap-hr-add-ons.txt.txt` | SAP HR ek çözümleri |
| `sap-portal-cozumler.txt.txt` | SAP Portal çözümleri |
| `further-sap-add-ons.txt.txt` | Ek SAP çözümleri |
| `non-sap-cozumler.txt.txt` | SAP dışı çözümler |
| `mdp-blog.txt.txt` | Blog içerikleri |
| `mdp-icerikler.txt.txt` | Genel içerikler |
| `mdp-iletisim.txt.txt` | İletişim bilgileri |
| `mdp-referanslar.txt.txt` | Müşteri referansları |
| `mdp-yapayzeka.txt.txt` | Yapay zeka hizmetleri |

---

## Önemli Notlar

- **API Anahtarı:** `.env` dosyasındaki `GOOGLE_API_KEY` değerini asla versiyon kontrolüne eklemeyin. `.gitignore` dosyası bunu zaten engellemektedir.
- **Embedding Tutarlılığı:** `create_db.py` ve `rag_engine.py` dosyalarında aynı embedding modeli (`gemini-embedding-001`) kullanılmalıdır. Farklı modeller hatalı arama sonuçlarına neden olur.
- **Vektör DB Yenileme:** `data/` klasörüne yeni veri eklediğinizde `create_db.py` scriptini tekrar çalıştırarak veritabanını güncellemeniz gerekir.
- **Kota ve Faturalandırma:** Google AI Studio'da ücretsiz katman kota sınırlarına dikkat edin. Yoğun kullanım için ücretli plana geçiş gerekebilir.

---

## Lisans

Bu proje deneme amaçlı geliştirilmiştir.

## İletişim

Proje hakkında sorularınız için:

- **E-posta:** oguzhankhrman@gmail.com
