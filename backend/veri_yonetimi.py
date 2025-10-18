# backend/veri_yonetimi.py

from pathlib import Path
import kagglehub
from langchain_core.documents import Document
import sys

def verileri_yukle_ve_hazirla():
    """
    Kaggle'dan veri setini indirir ve klasör yapısı ne olursa olsun içindeki
    tüm .txt dosyalarını okuyarak LangChain Document listesi döndürür.
    """
    try:
        print("Kaggle'dan veri seti indirme işlemi kontrol ediliyor...")
        veri_klasoru_yolu = kagglehub.dataset_download("oktayozturk010/42000-news-text-in-13-classes")
        print(f"Veri seti '{veri_klasoru_yolu}' konumunda hazır.")

        data_path = Path(veri_klasoru_yolu)
        documents = []

        # --- GÜNCELLENEN KISIM: Tüm alt klasörleri gez ---
        # Klasör yapısı ne olursa olsun, tüm .txt dosyalarını bul (recursive arama)
        for dosya_path in data_path.glob("**/*.txt"):
            try:
                # Dosyanın bulunduğu klasörün adını kategori olarak al
                kategori_adi = dosya_path.parent.name

                with open(dosya_path, 'r', encoding='utf-8') as f:
                    icerik = f.read()
                    documents.append(Document(page_content=icerik, metadata={'kategori': kategori_adi}))
            except Exception as e:
                print(f"Hata: {dosya_path} dosyası okunamadı - {e}", file=sys.stderr)
        # --- GÜNCELLENEN KISIM SONU ---

        if not documents:
            print("Uyarı: İndirilen veri seti içinde hiç .txt dosyası bulunamadı.", file=sys.stderr)

        return documents

    except Exception as e:
        print(
            f"KRİTİK HATA: Veri seti indirilemedi. Kaggle API kimlik doğrulamanızı (kaggle.json) kontrol edin !! - {e}",
            file=sys.stderr)
        return []