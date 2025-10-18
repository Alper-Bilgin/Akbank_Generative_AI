import React from "react";
import { Link, useLocation } from "react-router-dom";
import { FaMoon, FaComments } from "react-icons/fa";

export default function Navbar() {
  const { pathname } = useLocation();
  return (
    <header className="border-b border-slate-800">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3">
          <div className="w-8 h-8 bg-sky-500 rounded-full flex items-center justify-center">NB</div>
          <span className="font-bold text-lg">NewsBot</span>
        </Link>

        <nav className="flex items-center gap-4">
          <Link to="/about" className={`px-3 py-2 rounded ${pathname === "/about" ? "bg-slate-700" : "hover:bg-slate-800"}`}>
            Proje Hakkında
          </Link>
          <Link to="/" className={`px-3 py-2 rounded ${pathname === "/" ? "bg-slate-700" : "hover:bg-slate-800"}`}>
            Sohbet
          </Link>
          <button className="p-2 rounded hover:bg-slate-800">
            <FaMoon />
          </button>
        </nav>
      </div>
    </header>
  );
}
