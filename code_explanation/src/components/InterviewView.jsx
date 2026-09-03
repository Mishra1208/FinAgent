import React, { useState } from 'react';
import { 
  Award, 
  Sparkles, 
  ChevronDown, 
  ChevronUp, 
  CheckCircle2, 
  HelpCircle,
  BookOpen,
  Target,
  Eye,
  EyeOff
} from 'lucide-react';
import { INTERVIEW_QUESTIONS } from '../data/interviewQs';

export default function InterviewView() {
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [expandedItems, setExpandedItems] = useState({});
  const [showAllAnswers, setShowAllAnswers] = useState(true);

  const categories = ["All", ...INTERVIEW_QUESTIONS.map(g => g.category)];

  const toggleItem = (id) => {
    setExpandedItems(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const handleToggleAll = () => {
    const nextState = !showAllAnswers;
    setShowAllAnswers(nextState);
    const newExpanded = {};
    INTERVIEW_QUESTIONS.forEach(group => {
      group.items.forEach(item => {
        newExpanded[item.id] = nextState;
      });
    });
    setExpandedItems(newExpanded);
  };

  const filteredGroups = selectedCategory === "All" 
    ? INTERVIEW_QUESTIONS 
    : INTERVIEW_QUESTIONS.filter(g => g.category === selectedCategory);

  return (
    <main className="flex-1 overflow-y-auto p-6 md:p-8 space-y-8 max-w-5xl mx-auto">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-amber-500 via-orange-600 to-amber-700 text-white rounded-3xl p-8 card-shadow space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-black/20 border border-white/20 text-xs font-semibold text-amber-100">
          <Award className="w-3.5 h-3.5 text-amber-200" />
          Job Interview Preparation Masterclass
        </div>
        <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
          FinAgent GenAI Interview Questions & Model Answers
        </h2>
        <p className="text-sm sm:text-base text-amber-50 max-w-3xl leading-relaxed">
          Curated collection of high-frequency GenAI and financial AI interview questions designed to help you speak with authority on Hybrid RAG, LangGraph orchestration, deterministic math tools, and Ragas evaluations.
        </p>
      </div>

      {/* Filter and Mode Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-white p-4 rounded-2xl border border-slate-200 card-shadow">
        {/* Category Pills */}
        <div className="flex flex-wrap items-center gap-2">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                selectedCategory === cat
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Reveal/Hide Toggle */}
        <button
          onClick={handleToggleAll}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors cursor-pointer"
        >
          {showAllAnswers ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
          <span>{showAllAnswers ? "Hide All Answers (Practice Mode)" : "Show All Answers"}</span>
        </button>
      </div>

      {/* Question Groups */}
      <div className="space-y-8">
        {filteredGroups.map((group) => (
          <div key={group.category} className="space-y-4">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
              {group.category}
            </h3>

            <div className="space-y-4">
              {group.items.map((item) => {
                const isExpanded = expandedItems[item.id] ?? showAllAnswers;
                return (
                  <div 
                    key={item.id}
                    className="bg-white border border-slate-200 rounded-2xl overflow-hidden card-shadow hover:border-slate-300 transition-all"
                  >
                    {/* Question Header */}
                    <div 
                      onClick={() => toggleItem(item.id)}
                      className="p-5 flex items-start justify-between gap-4 cursor-pointer hover:bg-slate-50 transition-colors select-none"
                    >
                      <div className="flex items-start gap-3">
                        <span className="w-6 h-6 rounded-full bg-amber-100 text-amber-800 flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                          Q
                        </span>
                        <h4 className="text-sm sm:text-base font-bold text-slate-900 leading-snug">
                          {item.question}
                        </h4>
                      </div>

                      <div className="shrink-0 text-slate-400 hover:text-slate-600 p-1">
                        {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                      </div>
                    </div>

                    {/* Answer Drawer */}
                    {isExpanded && (
                      <div className="p-5 bg-gradient-to-b from-slate-50/60 to-white border-t border-slate-100 space-y-4">
                        <div className="space-y-2">
                          <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-800">
                            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                            <span>Recommended Model Answer:</span>
                          </div>
                          <p className="text-xs sm:text-sm text-slate-700 leading-relaxed pl-5.5">
                            {item.answer}
                          </p>
                        </div>

                        {/* Bulleted Talking Points */}
                        {item.keyPoints && (
                          <div className="bg-amber-50/70 border border-amber-200/60 rounded-xl p-3.5 space-y-1.5">
                            <div className="text-xs font-bold text-amber-900 flex items-center gap-1.5">
                              <Target className="w-3.5 h-3.5 text-amber-600" />
                              <span>Key Takeaways for Your Interview:</span>
                            </div>
                            <ul className="list-disc list-inside space-y-1 text-xs text-amber-950">
                              {item.keyPoints.map((pt, idx) => (
                                <li key={idx} className="font-medium">{pt}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
