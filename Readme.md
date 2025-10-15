Projenin Amacı: Türkçe haber metinlerinden oluşan bir bilgi havuzunu kullanarak, kullanıcıların sorduğu sorulara anlamlı ve doğru cevaplar üreten RAG tabanlı bir sohbet robotu geliştirmek.


Veri Seti Hakkında Bilgi: Kaggle'dan alınan ve 13 farklı kategoride .txt dosyaları olarak organize edilmiş yaklaşık 42,000 Türkçe haber metni içeren bir veri seti kullanılmıştır.

Kullanılan Yöntemler: LangChain framework'ü ile bir RAG (Retrieval Augmented Generation) mimarisi kurulmuştur. Vektör veritabanı olarak ChromaDB, LLM ve Embedding modeli olarak ise Google Gemini API kullanılmıştır.