import React from 'react';
import { 
  BookOpen, 
  GitBranch, 
  Award, 
  Search, 
  ShieldCheck, 
  FolderTree,
  ExternalLink
} from 'lucide-react';

export default function Header({ 
  activeTab, 
  setActiveTab, 
  onOpenSearch, 
  totalModules 
}) {
  return (
    <header className="sticky top-0 z-30 bg-white border-b border-slate-200 px-6 py-3.5 card-shadow flex items-center justify-between">
      {/* Left branding */}
      <div className="flex items-center gap-3.5">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
          <ShieldCheck className="w-5 h-5" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-lg font-bold text-slate-900 tracking-tight flex items-center gap-1.5">
              FinAgent <span className="text-blue-600 font-semibold text-xs px-2 py-0.5 bg-blue-50 border border-blue-200 rounded-full">Interview Masterclass</span>
            </h1>
            <span className="hidden sm:inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              96.4% Grounded
            </span>
          </div>
          <p className="text-xs text-slate-500 truncate max-w-[280px] sm:max-w-md">
            Beginner-Friendly SEC Multi-Agent Financial Architecture & Code Guide
          </p>
        </div>
      </div>

      {/* Center Navigation Tabs */}
      <div className="hidden md:flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200">
        <button
          onClick={() => setActiveTab('code')}
          className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            activeTab === 'code'
              ? 'bg-white text-blue-700 shadow-sm border border-slate-200/60'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
          }`}
        >
          <BookOpen className="w-3.5 h-3.5" />
          Code Explanation ({totalModules})
        </button>

        <button
          onClick={() => setActiveTab('structure')}
          className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            activeTab === 'structure'
              ? 'bg-white text-blue-700 shadow-sm border border-slate-200/60'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
          }`}
        >
          <FolderTree className="w-3.5 h-3.5 text-blue-600" />
          File Structure & Hierarchy
        </button>

        <button
          onClick={() => setActiveTab('architecture')}
          className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            activeTab === 'architecture'
              ? 'bg-white text-blue-700 shadow-sm border border-slate-200/60'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
          }`}
        >
          <GitBranch className="w-3.5 h-3.5 text-purple-600" />
          Multi-Agent Workflow
        </button>

        <button
          onClick={() => setActiveTab('interview')}
          className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            activeTab === 'interview'
              ? 'bg-white text-blue-700 shadow-sm border border-slate-200/60'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
          }`}
        >
          <Award className="w-3.5 h-3.5 text-amber-600" />
          Interview Q&A Guide
        </button>
      </div>

      {/* Right Search Action */}
      <div className="flex items-center gap-2.5">
        <button
          onClick={onOpenSearch}
          className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium text-slate-500 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg transition-colors cursor-pointer group"
        >
          <Search className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600 transition-colors" />
          <span className="hidden sm:inline">Search codebase & concepts...</span>
          <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] font-semibold text-slate-400 bg-white border border-slate-200 rounded shadow-2xs">
            ⌘K
          </kbd>
        </button>
      </div>
    </header>
  );
}
