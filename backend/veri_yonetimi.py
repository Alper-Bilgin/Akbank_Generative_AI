from pathlib import Path
import kagglehub
from langchain_core.documents import Document
import sys
from collections import Counter

def verileri_yukle_ve_hazirla(max_documents=None):
    try:
        print("Kaggle'dan veri seti indirme işlemi kontrol ediliyor...")
        veri_klasoru_yolu = kagglehub.dataset_download("oktayozturk010/42000-news-text-in-13-classes")
        print(f"Veri seti '{veri_klasoru_yolu}' konumunda hazır.")

        data_path = Path(veri_klasoru_yolu)
        documents = []

        dosyalar = list(data_path.glob("**/*.txt"))
        if max_documents:
            dosyalar = dosyalar[:max_documents]
            print(f"Test modu: İlk {max_documents} döküman yüklenecek")

        for dosya_path in dosyalar:
            try:
                kategori_adi = dosya_path.parent.name
                with open(dosya_path, 'r', encoding='utf-8') as f:
                    icerik = f.read()
                    documents.append(Document(page_content=icerik, metadata={'kategori': kategori_adi}))
            except Exception as e:
                print(f"Hata: {dosya_path} dosyası okunamadı - {e}", file=sys.stderr)

        # Kategori dağılımını göster
        kategoriler = Counter([doc.metadata['kategori'] for doc in documents])
        print(f"\nToplam {len(documents)} döküman yüklendi.")
        print("Kategori Dağılımı:")
        for kategori, sayi in kategoriler.items():
            print(f"  - {kategori}: {sayi} döküman")

        return documents

    except Exception as e:
        print(f"KRİTİK HATA: Veri seti indirilemedi - {e}", file=sys.stderr)
        return []
