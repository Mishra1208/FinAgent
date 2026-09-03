import React, { useState } from 'react';
import { 
  ChevronDown, 
  ChevronUp, 
  Lightbulb, 
  Wrench, 
  Target, 
  Copy, 
  Check, 
  Code2,
  BookOpen,
  Sparkles,
  HelpCircle,
  FileText
} from 'lucide-react';

export default function CodeSection({ section, isExpandedDefault = true }) {
  const [isExpanded, setIsExpanded] = useState(isExpandedDefault);
  const [copied, setCopied] = useState(false);

  const handleCopy = (e) => {
    e.stopPropagation();
    navigator.clipboard.writeText(section.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="border border-slate-200 rounded-2xl overflow-hidden bg-white card-shadow transition-all hover:border-slate-300 mb-5">
      {/* Code Header Bar */}
      <div 
        onClick={() => setIsExpanded(!isExpanded)}
        className="px-5 py-3.5 bg-slate-50/90 border-b border-slate-200 flex items-center justify-between cursor-pointer hover:bg-slate-100 transition-colors select-none"
      >
        <div className="flex items-center gap-3 min-w-0">
          <span className="px-2.5 py-1 text-[11px] font-mono font-bold text-blue-700 bg-blue-50 border border-blue-200 rounded-md shadow-2xs">
            Lines {section.startLine}–{section.endLine}
          </span>
          <h4 className="text-xs sm:text-sm font-bold text-slate-800 truncate flex items-center gap-2">
            <Code2 className="w-4 h-4 text-blue-600 shrink-0" />
            {section.title}
          </h4>
        </div>

        <div className="flex items-center gap-2.5 shrink-0">
          <button
            onClick={handleCopy}
            title="Copy snippet"
            className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-white rounded-lg border border-transparent hover:border-slate-200 transition-all cursor-pointer"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
          </button>
          
          <div className="flex items-center gap-1 text-xs font-bold text-blue-700 bg-blue-100/70 hover:bg-blue-200/80 px-3 py-1.5 rounded-lg transition-colors shadow-2xs">
            <span>{isExpanded ? "Hide Explanation" : "Explain Code Line-by-Line"}</span>
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </div>
        </div>
      </div>

      {/* Code Snippet Box */}
      <div className="bg-slate-900 text-slate-100 p-5 font-mono text-xs overflow-x-auto border-b border-slate-800 leading-relaxed selection:bg-blue-600 selection:text-white">
        <pre>
          <code>{section.code}</code>
        </pre>
      </div>

      {/* Expandable Deep-Dive Beginner-Friendly Explanation Drawer */}
      {isExpanded && (
        <div className="p-5 md:p-6 bg-gradient-to-b from-slate-50/80 via-white to-slate-50/30 divide-y divide-slate-100 space-y-5">
          {/* 1. Line-by-Line Breakdown */}
          {section.lineByLine && section.lineByLine.length > 0 && (
            <div className="pt-2 first:pt-0 space-y-3">
              <div className="flex items-center gap-2 text-xs font-bold text-slate-900 uppercase tracking-wider">
                <FileText className="w-4 h-4 text-indigo-600" />
                <span>Line-by-Line Code Breakdown:</span>
              </div>
              <div className="bg-white border border-slate-200 rounded-xl p-4 space-y-2.5 shadow-2xs">
                {section.lineByLine.map((lineDesc, idx) => (
                  <div key={idx} className="text-xs sm:text-sm text-slate-700 leading-relaxed flex items-start gap-2.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-2 shrink-0"></span>
                    <div dangerouslySetInnerHTML={{ __html: lineDesc.replace(/`([^`]+)`/g, '<code class="px-1.5 py-0.5 bg-slate-100 text-blue-700 rounded font-mono text-xs font-semibold">$1</code>') }} />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 2. Python & GenAI Concepts Glossary */}
          {section.beginnerConcepts && section.beginnerConcepts.length > 0 && (
            <div className="pt-4 space-y-3">
              <div className="flex items-center gap-2 text-xs font-bold text-slate-900 uppercase tracking-wider">
                <Sparkles className="w-4 h-4 text-purple-600" />
                <span>Python & GenAI Beginner Concepts Explained:</span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {section.beginnerConcepts.map((item, idx) => (
                  <div key={idx} className="bg-purple-50/50 border border-purple-100 rounded-xl p-3.5 space-y-1">
                    <div className="text-xs font-bold text-purple-900 font-mono flex items-center gap-1.5">
                      <BookOpen className="w-3.5 h-3.5 text-purple-600" />
                      {item.term}
                    </div>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      {item.explanation}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 3. Plain English Overview */}
          {section.simpleExplanation && (
            <div className="pt-4 space-y-2">
              <div className="flex items-center gap-2 text-xs font-bold text-slate-900 uppercase tracking-wider">
                <Lightbulb className="w-4 h-4 text-amber-500" />
                <span>In Simple Terms (Plain English):</span>
              </div>
              <p className="text-xs sm:text-sm text-slate-700 leading-relaxed pl-6 border-l-2 border-amber-400 font-medium">
                {section.simpleExplanation}
              </p>
            </div>
          )}

          {/* 4. Why written this way */}
          {section.whyWrittenThisWay && (
            <div className="pt-4 space-y-2">
              <div className="flex items-center gap-2 text-xs font-bold text-slate-900 uppercase tracking-wider">
                <Wrench className="w-4 h-4 text-blue-600" />
                <span>Why It's Written This Way (Engineering & Architecture):</span>
              </div>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed pl-6 border-l-2 border-blue-400">
                {section.whyWrittenThisWay}
              </p>
            </div>
          )}

          {/* 5. Interview Talking Points */}
          {section.interviewTips && (
            <div className="pt-4 -mx-5 -mb-5 md:-mx-6 md:-mb-6 p-5 bg-gradient-to-r from-amber-50 via-orange-50/60 to-amber-50 rounded-b-2xl border-t border-amber-200/70 space-y-2">
              <div className="flex items-center gap-2 text-xs font-bold text-amber-900 uppercase tracking-wider">
                <Target className="w-4 h-4 text-amber-600" />
                <span>Interview Talking Point & Model Answer:</span>
              </div>
              <p className="text-xs sm:text-sm text-amber-950 font-medium leading-relaxed pl-6 border-l-2 border-amber-500">
                {section.interviewTips}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
