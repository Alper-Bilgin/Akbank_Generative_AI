import React from "react";

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto bg-slate-800 p-8 rounded-lg shadow-lg">
      <h1 className="text-4xl font-extrabold mb-4">Proje Hakkında</h1>
      <p className="text-slate-300 leading-relaxed mb-6">
        Bu proje, haber verisi üzerinde çalışan RAG tabanlı bir chatbot arayüzünü örnekler. İki sayfadan oluşur: sohbet ekranı ve hakkında sayfası. Backend tarafında /chat endpoint'ine string tipinde
        bir mesaj gönderilir ve cevap gösterilir.
      </p>
      <h2 className="text-2xl font-bold mb-2">Geliştirici Ekip</h2>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="text-center">
          <div className="w-28 h-28 rounded-full bg-slate-700 mx-auto mb-3"></div>
          <div className="font-semibold">Geliştirici 1</div>
          <a className="text-sm text-sky-400" href="#">
            LinkedIn
          </a>
        </div>
        <div className="text-center">
          <div className="w-28 h-28 rounded-full bg-slate-700 mx-auto mb-3"></div>
          <div className="font-semibold">Geliştirici 2</div>
          <a className="text-sm text-sky-400" href="#">
            LinkedIn
          </a>
        </div>
        <div className="text-center">
          <div className="w-28 h-28 rounded-full bg-slate-700 mx-auto mb-3"></div>
          <div className="font-semibold">Geliştirici 3</div>
          <a className="text-sm text-sky-400" href="#">
            LinkedIn
          </a>
        </div>
      </div>
    </div>
  );
}
