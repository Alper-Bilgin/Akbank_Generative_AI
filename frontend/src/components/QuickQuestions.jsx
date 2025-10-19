import React from "react";
import { FaQuestionCircle } from "react-icons/fa";

const questions = ["Türkiye Siyaseti hakkında bana bilgi verir misin?", "2000 yılına ait spor haberlerini sırasıyla ver?", "Recep Tayyip Erdoğan kimdir?"];

export default function QuickQuestions({ onSelect }) {
  return (
    <div className="mb-4">
      <h3 className="text-lg font-semibold mb-2 flex items-center gap-2">
        <FaQuestionCircle className="text-sky-600 dark:text-sky-400" />
        Örnek Sorular:
      </h3>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {questions.map((q, i) => (
          <button
            key={i}
            onClick={() => onSelect(q)}
            className="text-sm px-4 py-3 rounded bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 hover:bg-slate-100 dark:hover:bg-slate-600 transition-colors shadow-sm text-left"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
