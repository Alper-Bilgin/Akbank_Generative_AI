import React from "react";

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 p-8 rounded-lg shadow-lg transition-colors duration-300">
      <h1 className="text-4xl font-extrabold mb-6">Proje Hakkında</h1>

      <p className="leading-relaxed mb-6 text-slate-700 dark:text-slate-300">
        Bu proje, haber verisi üzerinde çalışan RAG tabanlı bir chatbot arayüzünü örnekler. İki sayfadan oluşur: sohbet ekranı ve hakkında sayfası. Backend tarafında{" "}
        <code className="bg-slate-100 dark:bg-slate-700 px-1 rounded">/chat</code> endpoint'ine string tipinde bir mesaj gönderilir ve cevap kullanıcıya gösterilir.
      </p>

      <h2 className="text-2xl font-bold mb-4">Geliştirici Ekip</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
        <div className="text-center">
          <div className="font-semibold text-lg">Alper BİLĞİN</div>
          <div className="text-sm text-slate-600 dark:text-slate-400">
            Konya Teknik Üniversitesi
            <br />
            Bilgisayar Mühendisliği
          </div>
          <a href="https://www.linkedin.com/in/alper-bil%C4%9Fin-88b242162/" target="_blank" rel="noopener noreferrer" className="text-sky-500 hover:underline text-sm block mt-1">
            LinkedIn Profili
          </a>
        </div>
        <div className="text-center">
          <div className="font-semibold text-lg">Ahmet Berke ÇİFTÇİ</div>
          <div className="text-sm text-slate-600 dark:text-slate-400">
            Konya Teknik Üniversitesi
            <br />
            Bilgisayar Mühendisliği
          </div>
          <a href="https://www.linkedin.com/in/ahmet-berke-%C3%A7ift%C3%A7i-2111672b4/" target="_blank" rel="noopener noreferrer" className="text-sky-500 hover:underline text-sm block mt-1">
            LinkedIn Profili
          </a>
        </div>
      </div>

      <h2 className="text-2xl font-bold mb-4">Proje Bağlantıları</h2>
      <ul className="list-disc list-inside space-y-2 mb-8 text-slate-700 dark:text-slate-300">
        <li>
          GitHub Proje Reposu:{" "}
          <a href="https://github.com/Alper-Bilgin/Akbank_Generative_AI" target="_blank" rel="noopener noreferrer" className="text-sky-500 hover:underline">
            https://github.com/Alper-Bilgin/Akbank_Generative_AI
          </a>
        </li>
        <li>
          Kullanılan Veri Seti (Kaggle):{" "}
          <a href="https://www.kaggle.com/datasets/oktayozturk010/42000-news-text-in-13-classes" target="_blank" rel="noopener noreferrer" className="text-sky-500 hover:underline">
            42000 News Text in 13 Classes
          </a>
        </li>
      </ul>

      <h2 className="text-2xl font-bold mb-4">Veri Seti Hakkında</h2>
      <div className="text-slate-700 dark:text-slate-300 space-y-3">
        <p>
          <strong>Veri Kümesi Adı:</strong> 42 Bin Haber Veri Kümesi
        </p>
        <p>
          <strong>Son Güncelleme:</strong> 21 Nisan 2003
        </p>
        <p>
          <strong>Oluşturanlar:</strong> Oğuz Yıldırım, Fatih Atık, M. Fatih AMASYALI – Yıldız Teknik Üniversitesi, Bilgisayar Müh. Bölümü
        </p>
        <p>
          <strong>İçerik:</strong> “news” klasörü içerisinde 13 farklı kategoriye ait toplamda <strong>41.992</strong> haber metni bulunmaktadır.
        </p>

        <div className="overflow-x-auto">
          <table className="min-w-full text-sm text-left border border-slate-300 dark:border-slate-600">
            <thead className="bg-slate-200 dark:bg-slate-700">
              <tr>
                <th className="p-2 border border-slate-300 dark:border-slate-600">Sınıf İsmi</th>
                <th className="p-2 border border-slate-300 dark:border-slate-600">Örnek Sayısı</th>
              </tr>
            </thead>
            <tbody>
              {[
                ["Dünya", 3724],
                ["Ekonomi", 3265],
                ["Genel", 6673],
                ["Güncel", 5847],
                ["Kültür Sanat", 1155],
                ["Magazin", 2792],
                ["Planet", 1953],
                ["Sağlık", 1383],
                ["Siyaset", 1849],
                ["Spor", 9997],
                ["Teknoloji", 771],
                ["Türkiye", 1939],
                ["Yaşam", 644],
              ].map(([className, count]) => (
                <tr key={className}>
                  <td className="p-2 border border-slate-300 dark:border-slate-600">{className}</td>
                  <td className="p-2 border border-slate-300 dark:border-slate-600">{count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <p>
          <strong>Kullanım Alanı:</strong> Metin sınıflandırma
        </p>
        <p>
          <strong>Toplam Sınıf Sayısı:</strong> 13
        </p>
        <p>
          <strong>Toplam Örnek Sayısı:</strong> 41.992
        </p>
        <p>
          <strong>İletişim:</strong>{" "}
          <a className="text-sky-500 hover:underline" href="mailto:mfatih@ce.yildiz.edu.tr">
            mfatih@ce.yildiz.edu.tr
          </a>
        </p>
        <p>
          <strong>Referans:</strong> "Kişisel Gazete”, Oğuz Yıldırım, Fatih Atık, Yıldız Teknik Üniversitesi, Bilgisayar Mühendisliği Bölümü, Bitirme Projesi, 2013.
        </p>
      </div>
    </div>
  );
}
