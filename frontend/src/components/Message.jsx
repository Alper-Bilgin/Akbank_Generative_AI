export default function Message({ from, text }) {
  const isUser = from === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
      <div className={`${isUser ? "bg-sky-600 text-white" : "bg-slate-700 text-slate-100"} max-w-[80%] px-4 py-2 rounded-lg`}>
        <div className="whitespace-pre-wrap">{text}</div>
      </div>
    </div>
  );
}
