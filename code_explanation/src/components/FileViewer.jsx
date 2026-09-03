import React, { useState } from 'react';
import { 
  FileCode, 
  Copy, 
  Check, 
  HelpCircle, 
  Layers, 
  Sparkles, 
  ArrowRight,
  Maximize2,
  Minimize2,
  Bookmark,
  Award
} from 'lucide-react';
import CodeSection from './CodeSection';

export default function FileViewer({ module }) {
  const [expandAllKey, setExpandAllKey] = useState(0);
  const [defaultExpand, setDefaultExpand] = useState(true);
  const [copiedAll, setCopiedAll] = useState(false);

  if (!module) {
    return (
      <div className="flex-1 flex items-center justify-center p-12 text-slate-400">
        Select a component from the sidebar to view detailed line-by-line explanation.
      </div>
    );
  }

  const handleExpandAll = () => {
    setDefaultExpand(true);
    setExpandAllKey(prev => prev + 1);
  };

  const handleCollapseAll = () => {
    setDefaultExpand(false);
    setExpandAllKey(prev => prev + 1);
  };

  const handleCopyFullCode = () => {
    const fullCode = module.sections.map(s => s.code).join("\n\n");
    navigator.clipboard.writeText(fullCode);
    setCopiedAll(true);
    setTimeout(() => setCopiedAll(false), 2000);
  };

  return (
    <main className="flex-1 overflow-y-auto p-6 md:p-8 space-y-6 max-w-5xl mx-auto">
      {/* Top File Header & Metadata */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 card-shadow space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-1 text-xs font-bold text-blue-700 bg-blue-50 border border-blue-200 rounded-lg">
              {module.category}
            </span>
            <span className="text-slate-300">/</span>
            <span className="font-mono text-xs text-slate-500 bg-slate-50 px-2 py-0.5 rounded border border-slate-200">
              {module.path}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopyFullCode}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg transition-colors cursor-pointer"
            >
              {copiedAll ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5 text-slate-500" />}
              <span>{copiedAll ? "Copied All" : "Copy Full File"}</span>
            </button>
          </div>
        </div>

        <div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
            {module.title}
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed mt-2">
            {module.summary}
          </p>
        </div>

        {/* Key Concepts Tags */}
        {module.keyConcepts && module.keyConcepts.length > 0 && (
          <div className="pt-2 border-t border-slate-100 flex flex-wrap items-center gap-2">
            <span className="text-xs font-bold text-slate-500 flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-amber-500" /> Core Concepts:
            </span>
            {module.keyConcepts.map((concept, idx) => (
              <span 
                key={idx} 
                className="text-[11px] font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 px-2.5 py-0.5 rounded-full transition-colors"
              >
                {concept}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Section Code Actions Bar */}
      <div className="flex items-center justify-between px-1">
        <div className="flex items-center gap-2">
          <h3 className="text-sm font-bold text-slate-800 flex items-center gap-1.5">
            <FileCode className="w-4 h-4 text-blue-600" />
            Line-by-Line Code Breakdown ({module.sections.length} Sections)
          </h3>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleExpandAll}
            className="flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-slate-600 hover:text-blue-700 hover:bg-white rounded-md border border-transparent hover:border-slate-200 transition-all cursor-pointer"
          >
            <Maximize2 className="w-3 h-3" /> Expand All
          </button>
          <span className="text-slate-300">|</span>
          <button
            onClick={handleCollapseAll}
            className="flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-slate-600 hover:text-blue-700 hover:bg-white rounded-md border border-transparent hover:border-slate-200 transition-all cursor-pointer"
          >
            <Minimize2 className="w-3 h-3" /> Collapse All
          </button>
        </div>
      </div>

      {/* Sections List */}
      <div key={expandAllKey} className="space-y-4">
        {module.sections.map((section) => (
          <CodeSection 
            key={section.sectionId} 
            section={section} 
            isExpandedDefault={defaultExpand} 
          />
        ))}
      </div>

      {/* Dedicated Interview Q&A for this file */}
      {module.interviewQuestions && module.interviewQuestions.length > 0 && (
        <div className="bg-gradient-to-br from-amber-50/70 via-white to-orange-50/40 border border-amber-200/80 rounded-2xl p-6 card-shadow space-y-4 mt-8">
          <div className="flex items-center gap-2 text-amber-900 font-bold text-sm">
            <Award className="w-4 h-4 text-amber-600" />
            <span>Targeted Interview Questions for {module.title}</span>
          </div>

          <div className="space-y-3">
            {module.interviewQuestions.map((q, idx) => (
              <div key={idx} className="bg-white border border-amber-200/60 rounded-xl p-4 space-y-2">
                <div className="text-xs sm:text-sm font-bold text-slate-900 flex items-start gap-2">
                  <span className="text-amber-600 font-mono">Q{idx + 1}:</span>
                  <span>{q.question}</span>
                </div>
                <div className="text-xs sm:text-sm text-slate-700 leading-relaxed pl-6 border-l-2 border-amber-400">
                  <strong className="text-slate-900 block mb-1">Recommended Interview Answer:</strong>
                  {q.answer}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </main>
  );
}
