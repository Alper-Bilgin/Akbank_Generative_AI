import React, { useState, useRef, useEffect } from "react";
import { FaPaperPlane } from "react-icons/fa";
import Message from "./Message.jsx";
export default function Chatbot() {
  const [messages, setMessages] = useState([{ id: 1, from: "bot", text: "Hoşgeldiniz! Haberlerle ilgili sorularınızı sorabilirsiniz." }]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const listRef = useRef(null);

  useEffect(() => {
    // en son mesaja kaydır
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (e) => {
    e?.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;

    const userMsg = { id: Date.now(), from: "user", text: trimmed };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      // /chat endpoint'ine sadece string içeren bir payload gönderiyoruz
      const resp = await axios.post("/chat", { message: trimmed });
      // Beklenen: { reply: string } veya direkt string
      const replyText = resp?.data?.reply ?? resp?.data ?? "Sunucudan geçerli cevap alınamadı.";
      const botMsg = { id: Date.now() + 1, from: "bot", text: replyText };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
      const botMsg = { id: Date.now() + 2, from: "bot", text: "Üzgünüz, sunucuya ulaşırken bir hata oluştu." };
      setMessages((prev) => [...prev, botMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-800 rounded-lg shadow p-4 md:p-6">
      <h2 className="text-2xl font-bold mb-4">NewsBot Sohbet</h2>

      <div ref={listRef} className="h-[60vh] md:h-[65vh] overflow-auto p-3 rounded bg-slate-900/40 mb-4">
        {messages.map((m) => (
          <Message key={m.id} from={m.from} text={m.text} />
        ))}
      </div>

      <form onSubmit={sendMessage} className="flex gap-3">
        <input className="flex-1 bg-slate-700 rounded px-4 py-3 focus:outline-none" placeholder="Mesajınızı yazın..." value={input} onChange={(e) => setInput(e.target.value)} disabled={loading} />
        <button type="submit" className={`flex items-center gap-2 px-4 py-3 rounded ${loading ? "bg-slate-600 cursor-not-allowed" : "bg-sky-500 hover:bg-sky-600"}`} disabled={loading}>
          {loading ? (
            "Gönderiliyor..."
          ) : (
            <>
              <FaPaperPlane /> Gönder
            </>
          )}
        </button>
      </form>
    </div>
  );
}
