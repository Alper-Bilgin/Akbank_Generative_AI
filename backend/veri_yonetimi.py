from pathlib import Path
import kagglehub
from langchain_core.documents import Document
import sys
from collections import Counter


def verileri_yukle_ve_hazirla(max_documents=None):
    """
    Kaggle'dan Türkçe haber veri setini indirir, dosyaları okur ve LangChain Document'lerine dönüştürür

    Args:
        max_documents (int, optional): Test amaçlı ilk N dökümanı yükle. None ise tümünü yükler.

    Returns:
        list[Document]: LangChain Document objelerinin listesi. Her dökümanın:
            - page_content: Haberin tam metni
            - metadata: {'kategori': 'spor'} gibi ek bilgiler

    Veri Seti Yapısı:
        42000-news-text-in-13-classes/
        ├── ekonomi/
        │   ├── haber1.txt
        │   └── haber2.txt
        ├── spor/
        │   ├── haber1.txt
        │   └── haber2.txt
        └── ... (13 kategori)
    """
    try:
        print("Kaggle'dan veri seti indirme işlemi kontrol ediliyor...")

        # KaggleHub ile veri setini indir
        # Eğer daha önce indirilmişse cache'den yükler (tekrar indirmez)
        # Veri seti ~/.cache/kagglehub/ klasörüne indirilir
        veri_klasoru_yolu = kagglehub.dataset_download("oktayozturk010/42000-news-text-in-13-classes")
        print(f"Veri seti '{veri_klasoru_yolu}' konumunda hazır.")

        # Path objesi oluştur (modern dosya işlemleri için)
        data_path = Path(veri_klasoru_yolu)

        # Tüm dökümanları tutacak liste
        documents = []

        # Tüm .txt dosyalarını recursive olarak bul
        # **/*.txt: Tüm alt klasörlerdeki .txt dosyaları
        # glob() bir generator döndürür, list() ile listeye çevir
        dosyalar = list(data_path.glob("**/*.txt"))

        # Test modu: Sadece ilk N dökümanı yükle (hız için)
        if max_documents:
            dosyalar = dosyalar[:max_documents]
            print(f"Test modu: İlk {max_documents} döküman yüklenecek")

        # Her txt dosyasını oku ve LangChain Document'e dönüştür
        for dosya_path in dosyalar:
            try:
                # Dosya yolu: .../ekonomi/haber1.txt
                # parent.name ile klasör adını (kategoriyi) al: "ekonomi"
                kategori_adi = dosya_path.parent.name

                # Dosyayı UTF-8 encoding ile oku (Türkçe karakterler için önemli)
                with open(dosya_path, 'r', encoding='utf-8') as f:
                    icerik = f.read()

                    # LangChain Document objesi oluştur
                    # page_content: Vektörleştirilecek ana metin
                    # metadata: Filtreleme ve raporlama için ek bilgiler
                    documents.append(Document(
                        page_content=icerik,
                        metadata={'kategori': kategori_adi}
                    ))
            except Exception as e:
                # Tek bir dosya hatası tüm işlemi durdurmasın
                # stderr'e yaz ki loglarda görünsün
                print(f"Hata: {dosya_path} dosyası okunamadı - {e}", file=sys.stderr)

        # İstatistik: Her kategoriden kaç döküman yüklendi?
        # Counter: {'spor': 3200, 'ekonomi': 2800, ...}
        kategoriler = Counter([doc.metadata['kategori'] for doc in documents])

        # Yükleme özetini yazdır
        print(f"\nToplam {len(documents)} döküman yüklendi.")
        print("Kategori Dağılımı:")
        for kategori, sayi in kategoriler.items():
            print(f"  - {kategori}: {sayi} döküman")

        return documents

    except Exception as e:
        # Kaggle bağlantı hatası, API anahtarı eksik, vb.
        # Kritik hata: Uygulama çalışamaz
        print(f"KRİTİK HATA: Veri seti indirilemedi - {e}", file=sys.stderr)
        return []  # Boş liste döndür ki uygulama crash etmesin
