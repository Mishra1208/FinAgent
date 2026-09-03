import React, { useState } from 'react';
import { 
  Folder, 
  FileCode2, 
  ChevronRight, 
  ChevronDown, 
  Search,
  Filter,
  CheckCircle2,
  Cpu,
  Layers
} from 'lucide-react';

export default function Sidebar({ 
  modules, 
  activeModuleId, 
  onSelectModule,
  searchTerm,
  setSearchTerm
}) {
  // Group modules by category
  const categories = modules.reduce((acc, mod) => {
    if (!acc[mod.category]) {
      acc[mod.category] = [];
    }
    acc[mod.category].push(mod);
    return acc;
  }, {});

  // State for collapsed categories (all open by default)
  const [collapsed, setCollapsed] = useState({});

  const toggleCategory = (cat) => {
    setCollapsed(prev => ({ ...prev, [cat]: !prev[cat] }));
  };

  const filteredCategories = Object.keys(categories).reduce((acc, cat) => {
    const matched = categories[cat].filter(m => 
      m.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      m.path.toLowerCase().includes(searchTerm.toLowerCase()) ||
      m.summary.toLowerCase().includes(searchTerm.toLowerCase())
    );
    if (matched.length > 0) {
      acc[cat] = matched;
    }
    return acc;
  }, {});

  return (
    <aside className="w-80 bg-white border-r border-slate-200 flex flex-col h-[calc(100vh-61px)] sticky top-[61px] select-none">
      {/* Search and filter header */}
      <div className="p-3.5 border-b border-slate-200">
        <div className="relative">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Filter files or modules..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-8.5 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all placeholder:text-slate-400"
          />
          {searchTerm && (
            <button 
              onClick={() => setSearchTerm('')}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-xs text-slate-400 hover:text-slate-600"
            >
              ×
            </button>
          )}
        </div>
        <div className="flex items-center justify-between mt-2.5 px-1 text-[11px] text-slate-500 font-medium">
          <span className="flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-blue-600" />
            FinAgent Architecture
          </span>
          <span className="px-1.5 py-0.5 bg-slate-100 rounded text-slate-600 font-semibold">
            {modules.length} Components
          </span>
        </div>
      </div>

      {/* File Tree List */}
      <div className="flex-1 overflow-y-auto p-2.5 space-y-3">
        {Object.keys(filteredCategories).length === 0 ? (
          <div className="text-center py-8 text-xs text-slate-400">
            No matching files found for "{searchTerm}"
          </div>
        ) : (
          Object.keys(filteredCategories).map((categoryName) => {
            const isCategoryCollapsed = collapsed[categoryName];
            const items = filteredCategories[categoryName];

            return (
              <div key={categoryName} className="space-y-1">
                {/* Category Header */}
                <button
                  onClick={() => toggleCategory(categoryName)}
                  className="w-full flex items-center justify-between px-2.5 py-1.5 text-xs font-bold text-slate-700 hover:text-blue-700 hover:bg-slate-50 rounded-md transition-colors group cursor-pointer text-left"
                >
                  <span className="flex items-center gap-1.5 truncate">
                    {isCategoryCollapsed ? (
                      <ChevronRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600" />
                    ) : (
                      <ChevronDown className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600" />
                    )}
                    <span className="truncate">{categoryName}</span>
                  </span>
                  <span className="text-[10px] font-semibold text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded">
                    {items.length}
                  </span>
                </button>

                {/* Items in Category */}
                {!isCategoryCollapsed && (
                  <div className="ml-3 pl-2.5 border-l border-slate-200 space-y-0.5 mt-0.5">
                    {items.map((mod) => {
                      const isActive = mod.id === activeModuleId;
                      return (
                        <button
                          key={mod.id}
                          onClick={() => onSelectModule(mod.id)}
                          className={`w-full flex items-start gap-2 px-2.5 py-2 rounded-lg text-left transition-all text-xs cursor-pointer group ${
                            isActive
                              ? 'bg-blue-50 text-blue-900 font-medium border border-blue-200/80 shadow-2xs'
                              : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                          }`}
                        >
                          <FileCode2 
                            className={`w-3.5 h-3.5 mt-0.5 shrink-0 transition-colors ${
                              isActive ? 'text-blue-600' : 'text-slate-400 group-hover:text-slate-600'
                            }`} 
                          />
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center justify-between gap-1">
                              <span className={`truncate font-medium ${isActive ? 'text-blue-900 font-semibold' : 'text-slate-700'}`}>
                                {mod.title}
                              </span>
                            </div>
                            <div className="text-[10px] text-slate-400 font-mono truncate mt-0.5">
                              {mod.path}
                            </div>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Bottom status */}
      <div className="p-3 border-t border-slate-200 bg-slate-50/70 text-[11px] text-slate-500 flex items-center justify-between">
        <span className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
          All 32 Files Audited
        </span>
        <span className="text-slate-400">100% Pass</span>
      </div>
    </aside>
  );
}
