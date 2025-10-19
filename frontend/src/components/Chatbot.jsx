import React, { useState, useRef, useEffect } from "react";
import { FaPaperPlane, FaTrash } from "react-icons/fa";
import Message from "./Message.jsx";
import axios from "../api/axiosInstance.jsx";
import QuickQuestions from "./QuickQuestions.jsx";

export default function Chatbot() {
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem("chat_messages");
    return saved
      ? JSON.parse(saved)
      : [
          {
            id: 1,
            from: "bot",
            text: "Hoşgeldiniz! Haberlerle ilgili sorularınızı sorabilirsiniz.",
          },
        ];
  });

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const listRef = useRef(null);

  useEffect(() => {
    localStorage.setItem("chat_messages", JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    listRef.current?.scrollTo({
      top: listRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  const handleQuickQuestion = (questionText) => {
    setInput(questionText);
    sendMessage({ preventDefault: () => {} });
  };

  const sendMessage = async (e) => {
    e?.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;

    const userMsg = { id: Date.now(), from: "user", text: trimmed };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const resp = await axios.post("/chat", { question: trimmed });
      const replyText = resp?.data?.answer ?? "Sunucudan geçerli cevap alınamadı.";
      const botMsg = {
        id: Date.now() + 1,
        from: "bot",
        text: replyText,
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
      const botMsg = {
        id: Date.now() + 2,
        from: "bot",
        text: "Üzgünüz, sunucuya ulaşırken bir hata oluştu.",
      };
      setMessages((prev) => [...prev, botMsg]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    localStorage.removeItem("chat_messages");
    setMessages([
      {
        id: 1,
        from: "bot",
        text: "Sohbet sıfırlandı. Yeni bir sohbete başlayabilirsiniz.",
      },
    ]);
  };

  return (
    <div className="bg-slate-200 dark:bg-slate-800 rounded-lg shadow p-4 md:p-6 transition-colors duration-300">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">NewsBot Sohbet</h2>
        <button
          onClick={clearChat}
          className="flex items-center gap-2 text-sm px-3 py-2 rounded bg-slate-300 dark:bg-slate-700 hover:bg-slate-400 dark:hover:bg-slate-600 transition-colors"
          title="Geçmişi Temizle"
        >
          <FaTrash className="text-red-500" />
          <span className="hidden sm:inline">Sohbeti Temizle</span>
        </button>
      </div>

      {/* ✅ Mesajlar */}
      <div ref={listRef} className="h-[60vh] md:h-[65vh] overflow-auto p-3 rounded bg-slate-100 dark:bg-slate-900/40 mb-4 transition-colors">
        {messages.map((m) => (
          <Message key={m.id} from={m.from} text={m.text} />
        ))}
      </div>

      {/* ✅ Örnek sorular - input'un hemen üstünde */}
      <QuickQuestions onSelect={handleQuickQuestion} />

      {/* ✅ Mesaj gönderme alanı */}
      <form onSubmit={sendMessage} className="flex gap-3">
        <input
          className="flex-1 bg-slate-100 dark:bg-slate-700 text-slate-900 dark:text-white rounded px-4 py-3 focus:outline-none transition-colors"
          placeholder="Mesajınızı yazın..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button
          type="submit"
          className={`flex items-center gap-2 px-4 py-3 rounded transition-colors ${
            loading ? "bg-slate-400 dark:bg-slate-600 cursor-not-allowed" : "bg-sky-500 hover:bg-sky-600 dark:bg-sky-400 dark:hover:bg-sky-500"
          }`}
          disabled={loading}
        >
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
