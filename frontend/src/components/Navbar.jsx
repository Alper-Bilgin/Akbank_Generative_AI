import React from "react";
import { Link, useLocation } from "react-router-dom";
import { FaMoon, FaSun } from "react-icons/fa";
import { GiNewspaper } from "react-icons/gi";
import { useTheme } from "../context/ThemeContext";

export default function Navbar() {
  const { pathname } = useLocation();
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="border-b border-slate-300 dark:border-slate-700 bg-slate-200 dark:bg-slate-900 transition-colors duration-300">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-3">
          <div
            className="w-8 h-8 rounded-full flex items-center justify-center text-xl
            bg-black text-white dark:bg-white dark:text-black transition-colors duration-300"
          >
            <GiNewspaper />
          </div>
          <span className="font-bold text-lg">NewsBot</span>
        </Link>

        {/* Dinamik navigasyon */}
        <nav className="flex items-center gap-4">
          {pathname !== "/about" && (
            <Link to="/about" className="px-3 py-2 rounded hover:bg-slate-300 dark:hover:bg-slate-800 transition-colors">
              Proje Hakkında
            </Link>
          )}
          {pathname !== "/" && (
            <Link to="/" className="px-3 py-2 rounded hover:bg-slate-300 dark:hover:bg-slate-800 transition-colors">
              Sohbet
            </Link>
          )}

          {/* Tema değiştirici */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded hover:bg-slate-300 dark:hover:bg-slate-700 transition-colors text-xl"
            title={theme === "dark" ? "Aydınlık Moda Geç" : "Karanlık Moda Geç"}
          >
            {theme === "dark" ? <FaSun className="text-yellow-400" /> : <FaMoon />}
          </button>
        </nav>
      </div>
    </header>
  );
}
