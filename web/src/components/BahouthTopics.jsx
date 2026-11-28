import React, { useState, useEffect } from 'react';
import { 
  Tag, Search, Filter, ChevronDown, ChevronUp, 
  BookOpen, Layers, Sparkles, Globe, Target
} from 'lucide-react';

export default function BahouthTopics({ ayah }) {
  const [activeFilter, setActiveFilter] = useState('all'); // 'all', 'global', 'local'
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedTopics, setExpandedTopics] = useState({});
  const [sortBy, setSortBy] = useState('relevance'); // 'relevance', 'ayah_count', 'topic_id'

  // Load topics from ayah.topics (injected by build pipeline)
  const topics = ayah?.topics || [];
  
  // Separate global and local topics
  const globalTopics = topics.filter(t => t.scope === 'global');
  const localTopics = topics.filter(t => t.scope === 'local');

  const getFilteredTopics = () => {
    let list = activeFilter === 'global' ? globalTopics : 
               activeFilter === 'local' ? localTopics : topics;
    
    if (searchQuery.trim()) {
      const q = searchQuery.trim().toLowerCase();
      list = list.filter(t => 
        t.topic_text?.toLowerCase().includes(q) ||
        t.topic_arabic?.toLowerCase().includes(q) ||
        String(t.topic_id).includes(q)
      );
    }
    
    // Sort
    if (sortBy === 'ayah_count') {
      list = [...list].sort((a, b) => (b.global_ayah_count || 0) - (a.global_ayah_count || 0));
    } else if (sortBy === 'topic_id') {
      list = [...list].sort((a, b) => (a.topic_id || 0) - (b.topic_id || 0));
    }
    // relevance: default order from source
    
    return list;
  };

  const filteredTopics = getFilteredTopics();

  const toggleExpand = (topicId) => {
    setExpandedTopics(prev => ({ ...prev, [topicId]: !prev[topicId] }));
  };

  const formatAyahRange = (ayahs) => {
    if (!ayahs || ayahs.length === 0) return '';
    if (ayahs.length === 1) return `আয়াত ${ayahs[0]}`;
    return `আয়াত ${ayahs[0]}–${ayahs[ayahs.length - 1]} (${ayahs.length}টি আয়াত)`;
  };

  if (!topics || topics.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-xs border border-gray-200 dark:border-gray-700 text-center">
        <div className="flex items-center justify-center gap-2 text-emerald-700 dark:text-emerald-400 mb-3">
          <Tag className="w-6 h-6" />
          <span className="font-bold text-emerald-900 dark:text-emerald-300">বাহাউথ থিমেটিক শনাক্তকরণ</span>
        </div>
        <p className="text-gray-500 dark:text-gray-400 font-bengali text-sm">
          এই আয়াতের জন্য বাহাউথ থিমেটিক ডেটা সংকলনাধীন।
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-700">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-xl bg-amber-50 dark:bg-amber-950/60 flex items-center justify-center text-amber-700 dark:text-amber-300">
            <Tag className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-bold text-amber-900 dark:text-amber-300 font-bengali">বাহাউথ থিমেটিক শনাক্তকরণ</h3>
            <p className="text-xs text-gray-500 dark:text-gray-400 font-bengali">
              মাদীনা মুনাওয়ারা প্রামাণ্য ডেটাবেস থেকে আধারিত
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span className="font-mono bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 px-2 py-0.5 rounded border border-amber-200 dark:border-amber-800">
            মোট: {topics.length}
          </span>
          <span className="font-mono bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 px-2 py-0.5 rounded border border-emerald-200 dark:border-emerald-800">
            গ্লোবাল: {globalTopics.length}
          </span>
          <span className="font-mono bg-blue-100 dark:bg-blue-950/60 text-blue-800 dark:text-blue-300 px-2 py-0.5 rounded border border-blue-200 dark:border-blue-800">
            লোকাল: {localTopics.length}
          </span>
        </div>
      </div>

      {/* Toolbar: Search, Filter, Sort */}
      <div className="flex flex-wrap items-center gap-3 bg-gray-50 dark:bg-gray-700/40 p-3 rounded-xl border border-gray-100 dark:border-gray-700">
        {/* Search */}
        <div className="relative flex-1 min-w-[200px] max-w-xs">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="বিষয়, আরবি, আইডি দিয়ে খুঁজুন..."
            className="w-full pl-9 pr-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-800 text-xs sm:text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500"
          />
        </div>

        {/* Filter */}
        <div className="flex items-center gap-1 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-0.5">
          {['all', 'global', 'local'].map((f) => (
            <button
              key={f}
              onClick={() => setActiveFilter(f)}
              className={`px-2.5 py-1 rounded-md text-[11px] font-semibold font-bengali transition ${
                activeFilter === f
                  ? 'bg-amber-500 text-white shadow-xs'
                  : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100'
              }`}
            >
              {f === 'all' && <Layers className="w-3 h-3 mr-1" />}
              {f === 'global' && <Globe className="w-3 h-3 mr-1" />}
              {f === 'local' && <Target className="w-3 h-3 mr-1" />}
              {f === 'all' ? 'সব' : f === 'global' ? 'গ্লোবাল' : 'লোকাল'}
            </button>
          ))}
        </div>

        {/* Sort */}
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="px-2.5 py-1.5 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-800 text-xs font-bengali text-gray-700 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-amber-500"
        >
          <option value="relevance">সম্পর্কিততার অনুযায়ী</option>
          <option value="ayah_count">আয়াত সংখ্যা (ঘটানোর ক্রম)</option>
          <option value="topic_id">টপিক আইডি অনুযায়ী</option>
        </select>
      </div>

      {/* Topics List */}
      <div className="space-y-3">
        {filteredTopics.length === 0 ? (
          <div className="text-center py-8 text-gray-500 dark:text-gray-400 font-bengali">
            <Search className="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p>ফিল্টারের সাথে মিলে কোনো বিষয় পাওয়া যায়নি।</p>
          </div>
        ) : (
          filteredTopics.map((topic, idx) => {
            const isExpanded = expandedTopics[topic.topic_id];
            const hasGlobalData = topic.global_ayah_count && topic.global_ayah_count > 0;
            
            return (
              <div
                key={`${topic.topic_id}-${idx}`}
                className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden transition-all hover:border-amber-200 dark:hover:border-amber-800"
              >
                {/* Topic Header */}
                <button
                  onClick={() => toggleExpand(topic.topic_id)}
                  className="w-full px-4 py-3 flex items-center justify-between gap-3 text-left hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                >
                  <div className="flex items-center gap-3 flex-1 min-w-0">
                    {/* Scope Badge */}
                    <span className={`shrink-0 px-2 py-0.5 rounded-full text-[10px] font-bold font-mono ${
                      topic.scope === 'global' 
                        ? 'bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800'
                        : 'bg-blue-100 dark:bg-blue-950/80 text-blue-800 dark:text-blue-300 border border-blue-200 dark:border-blue-800'
                    }`}>
                      {topic.scope === 'global' ? 'গ্লোবাল' : 'লোকাল'}
                    </span>
                    
                    {/* Topic ID */}
                    <span className="shrink-0 font-mono text-xs text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/50 px-2 py-0.5 rounded border border-gray-200 dark:border-gray-600">
                      #{topic.topic_id}
                    </span>
                    
                    {/* Topic Text */}
                    <div className="min-w-0">
                      <p className="font-semibold text-gray-900 dark:text-gray-100 font-bengali truncate">
                        {topic.topic_text || topic.topic_arabic || 'বিষয়'}
                      </p>
                      {topic.topic_arabic && topic.topic_arabic !== topic.topic_text && (
                        <p className="text-xs text-gray-500 dark:text-gray-400 font-arabic truncate" dir="rtl">
                          {topic.topic_arabic}
                        </p>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2 shrink-0">
                    {hasGlobalData && (
                      <span className="text-[10px] font-mono bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 px-2 py-0.5 rounded border border-emerald-200 dark:border-emerald-800">
                        قرآنে {topic.global_ayah_count} আয়াত
                      </span>
                    )}
                    <span className={`text-lg transition-transform ${isExpanded ? 'rotate-180' : ''}`}>
                      <ChevronDown className="w-4 h-4 text-gray-400" />
                    </span>
                  </div>
                </button>

                {/* Expanded Details */}
                {isExpanded && (
                  <div className="px-4 pb-4 border-t border-gray-100 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-700/30 animate-in slide-in-from-top-2 duration-200">
                    <div className="space-y-3 pt-3">
                      
                      {/* Global Concordance */}
                      {hasGlobalData && (
                        <div className="bg-emerald-50/70 dark:bg-emerald-950/30 rounded-xl p-3 border border-emerald-100 dark:border-emerald-900/40 space-y-2">
                          <div className="flex items-center gap-2 text-xs font-bold text-emerald-900 dark:text-emerald-300 font-bengali">
                            <Globe className="w-3.5 h-3.5 text-emerald-600" />
                            <span>গ্লোবাল সমানুপাতিক (কুরআন-ব্যাপি)</span>
                          </div>
                          <p className="text-xs text-gray-700 dark:text-gray-300 font-bengali">
                            এই বিষয় পূরণ কুরআনে <strong className="font-mono">{topic.global_ayah_count}</strong>টি আয়াতে আবির্ভূত হয়েছে।
                          </p>
                          {topic.global_ayahs && topic.global_ayahs.length > 0 && (
                            <div className="flex flex-wrap gap-1.5">
                              {topic.global_ayahs.slice(0, 8).map((v, i) => (
                                <span
                                  key={i}
                                  className="px-2 py-0.5 rounded-full text-[10px] font-mono bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-200 border border-emerald-200 dark:border-emerald-800 hover:bg-emerald-100 dark:hover:bg-emerald-900/50 cursor-pointer transition"
                                >
                                  {v.surah}:{v.ayah}
                                </span>
                              ))}
                              {topic.global_ayahs.length > 8 && (
                                <span className="px-2 py-0.5 rounded-full text-[10px] font-mono bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400">
                                  +{topic.global_ayahs.length - 8} আরও
                                </span>
                              )}
                            </div>
                          )}
                        </div>
                      )}

                      {/* Local Context */}
                      {topic.local_context && (
                        <div className="bg-blue-50/70 dark:bg-blue-950/30 rounded-xl p-3 border border-blue-100 dark:border-blue-900/40 space-y-2">
                          <div className="flex items-center gap-2 text-xs font-bold text-blue-900 dark:text-blue-300 font-bengali">
                            <Target className="w-3.5 h-3.5 text-blue-600" />
                            <span>স্থানীয় প্রসঙ্গ (এই রুকু/সূরাতেই)</span>
                          </div>
                          <p className="text-xs text-gray-700 dark:text-gray-300 font-bengali bn-justify">
                            {topic.local_context}
                          </p>
                          {topic.local_ayahs && topic.local_ayahs.length > 0 && (
                            <div className="flex flex-wrap gap-1.5">
                              {topic.local_ayahs.map((v, i) => (
                                <span
                                  key={i}
                                  className="px-2 py-0.5 rounded-full text-[10px] font-mono bg-white dark:bg-gray-800 text-blue-800 dark:text-blue-200 border border-blue-200 dark:border-blue-800"
                                >
                                  {v}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      )}

                      {/* Source Attribution */}
                      <div className="text-[10px] text-gray-500 dark:text-gray-400 font-bengali flex items-center gap-1">
                        <BookOpen className="w-3 h-3" />
                        <span>সূত্র: বাহাউথ (মাদীনা মুনাওয়ারা) থিমেটিক ডেটাবেস</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}