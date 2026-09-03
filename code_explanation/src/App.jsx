import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import FileViewer from './components/FileViewer';
import FileStructureView from './components/FileStructureView';
import ArchitectureView from './components/ArchitectureView';
import InterviewView from './components/InterviewView';
import SearchModal from './components/SearchModal';
import { PROJECT_MODULES } from './data/projectData';

export default function App() {
  const [activeTab, setActiveTab] = useState('code');
  const [activeModuleId, setActiveModuleId] = useState(PROJECT_MODULES[0]?.id || '');
  const [searchTerm, setSearchTerm] = useState('');
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  // Active module object
  const activeModule = PROJECT_MODULES.find(m => m.id === activeModuleId) || PROJECT_MODULES[0];

  // Cmd+K or Ctrl+K shortcut to trigger search modal
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsSearchOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleSelectModule = (id) => {
    if (id) {
      setActiveModuleId(id);
      setActiveTab('code');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col selection:bg-blue-100 selection:text-blue-900 font-sans">
      {/* Top Header */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenSearch={() => setIsSearchOpen(true)}
        totalModules={PROJECT_MODULES.length}
      />

      {/* Main Body */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar (shown on 'code' tab) */}
        {activeTab === 'code' && (
          <Sidebar
            modules={PROJECT_MODULES}
            activeModuleId={activeModuleId}
            onSelectModule={handleSelectModule}
            searchTerm={searchTerm}
            setSearchTerm={setSearchTerm}
          />
        )}

        {/* Content Area based on Active Tab */}
        {activeTab === 'code' && (
          <FileViewer module={activeModule} />
        )}

        {activeTab === 'structure' && (
          <FileStructureView onSelectFile={handleSelectModule} />
        )}

        {activeTab === 'architecture' && (
          <ArchitectureView onSelectFile={handleSelectModule} />
        )}

        {activeTab === 'interview' && (
          <InterviewView />
        )}
      </div>

      {/* Global Search Modal */}
      <SearchModal
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        modules={PROJECT_MODULES}
        onSelectModule={handleSelectModule}
      />
    </div>
  );
}
