import React, { useState, useEffect } from 'react';
import { 
  Search, 
  X, 
  FileCode2, 
  Code2, 
  Award, 
  ArrowRight,
  Sparkles
} from 'lucide-react';

export default function SearchModal({ 
  isOpen, 
  onClose, 
  modules, 
  onSelectModule 
}) {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const results = query.trim() ? modules.filter(m => {
    const q = query.toLowerCase();
    const matchMeta = m.title.toLowerCase().includes(q) ||
                      m.path.toLowerCase().includes(q) ||
                      m.summary.toLowerCase().includes(q) ||
                      (m.keyConcepts && m.keyConcepts.some(c => c.toLowerCase().includes(q)));
    const matchCode = m.sections.some(s => 
      s.title.toLowerCase().includes(q) ||
      s.code.toLowerCase().includes(q) ||
      s.simpleExplanation.toLowerCase().includes(q)
    );
    return matchMeta || matchCode;
  }) : modules.slice(0, 6);

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-slate-900/40 backdrop-blur-xs animate-in fade-in duration-150">
      <div className="bg-white border border-slate-200 w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[80vh]">
        {/* Search Input Bar */}
        <div className="p-4 border-b border-slate-200 flex items-center gap-3 bg-slate-50/50">
          <Search className="w-5 h-5 text-blue-600 shrink-0" />
          <input
            autoFocus
            type="text"
            placeholder="Search files, code snippets, functions, or interview topics..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 bg-transparent text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none"
          />
          {query && (
            <button
              onClick={() => setQuery('')}
              className="text-xs text-slate-400 hover:text-slate-600 px-1.5 py-0.5"
            >
              Clear
            </button>
          )}
          <button
            onClick={onClose}
            className="p-1 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Results List */}
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-2 py-1">
            {query.trim() ? `Search Results (${results.length})` : 'Recommended Files'}
          </div>

          {results.length === 0 ? (
            <div className="text-center py-12 text-sm text-slate-400">
              No results found for "{query}". Try searching for "RRF", "margin", "loader", or "guardrail".
            </div>
          ) : (
            results.map((m) => (
              <div
                key={m.id}
                onClick={() => {
                  onSelectModule(m.id);
                  onClose();
                }}
                className="p-3 rounded-xl border border-slate-100 hover:border-blue-200 hover:bg-blue-50/50 transition-all cursor-pointer group flex items-start gap-3"
              >
                <div className="w-8 h-8 rounded-lg bg-blue-100/70 text-blue-700 flex items-center justify-center shrink-0 mt-0.5 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                  <FileCode2 className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2">
                    <h4 className="text-xs sm:text-sm font-bold text-slate-800 group-hover:text-blue-900 truncate">
                      {m.title}
                    </h4>
                    <span className="text-[10px] font-mono text-slate-400 shrink-0">
                      {m.path}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 line-clamp-1 mt-0.5">
                    {m.summary}
                  </p>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-300 group-hover:text-blue-600 shrink-0 self-center transition-colors" />
              </div>
            ))
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-3 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-[11px] text-slate-500">
          <span>Press <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded font-semibold text-slate-600">ESC</kbd> to exit</span>
          <span className="flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-amber-500" />
            FinAgent Code Explorer
          </span>
        </div>
      </div>
    </div>
  );
}
