import React from 'react';
import { X, UserCheck, ShieldCheck, BookOpen, MapPin, Award, CheckCircle } from 'lucide-react';

export default function AuthorModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-3 sm:p-4 animate-in fade-in duration-200">
      <div className="bg-white dark:bg-gray-800 rounded-3xl max-w-lg w-full max-h-[90vh] overflow-y-auto shadow-2xl p-6 sm:p-8 border border-gray-200 dark:border-gray-700 space-y-5">
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-2 text-emerald-700 dark:text-emerald-400 font-bold">
            <UserCheck className="w-5 h-5" />
            <h3 className="text-base sm:text-lg">অনুবাদ ও প্রকাশনা স্বত্বাধিকার</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-full text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Author Card */}
        <div className="bg-emerald-50/70 dark:bg-emerald-950/40 p-4 rounded-2xl border border-emerald-200 dark:border-emerald-800 space-y-3">
          <div className="flex items-start gap-3">
            <div className="w-12 h-12 rounded-2xl bg-emerald-600 text-white flex items-center justify-center font-bold text-lg shrink-0 shadow-md">
              ম
            </div>
            <div>
              <div className="text-xs font-bold text-emerald-800 dark:text-emerald-300 uppercase tracking-wider">
                অনুবাদ, প্রামাণ্য তাহকীক ও সম্পাদনা
              </div>
              <h2 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-white">
                মুফতী মুহাম্মাদ মুহিব্বুল্লাহ
              </h2>
              <div className="text-xs text-gray-600 dark:text-gray-300 font-mono">
                Muheb Anam
              </div>
            </div>
          </div>

          {/* Academic Designations & Institutions */}
          <div className="pt-2 border-t border-emerald-200/60 dark:border-emerald-800/60 space-y-2 text-xs text-gray-800 dark:text-gray-200">
            <div className="flex items-start gap-2">
              <Award className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <div>
                <strong>খতীব ও ইমাম:</strong> শাতিইলমা জামে মসজিদ কমপ্লেক্স, খিলগাঁও, ঢাকা
              </div>
            </div>

            <div className="flex items-start gap-2">
              <Award className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <div>
                <strong>মুহাদ্দীস:</strong> জামিয়া দারুল উলূম নূরবাগ, খিলগাঁও, তালতলা, ঢাকা
              </div>
            </div>
          </div>
        </div>

        {/* Publisher & Edition Details */}
        <div className="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-2xl border border-gray-200 dark:border-gray-600 space-y-2.5 text-xs text-gray-800 dark:text-gray-200">
          <div className="font-bold text-gray-900 dark:text-white flex items-center gap-1.5 text-sm">
            <BookOpen className="w-4 h-4 text-emerald-600" />
            <span>প্রকাশনা সংস্থা ও গবেষণা পরিষদ</span>
          </div>

          <div className="grid grid-cols-2 gap-2 pt-1">
            <div>
              <span className="text-gray-500 dark:text-gray-400 block text-[11px]">প্রকাশনা সংস্থা:</span>
              <strong className="text-emerald-800 dark:text-emerald-300">মাকতাবাতুল ইসহাক</strong>
            </div>
            <div>
              <span className="text-gray-500 dark:text-gray-400 block text-[11px]">প্রকাশনা কার্যালয়:</span>
              <span>রিয়াজবাগ, রামপুরা, ঢাকা</span>
            </div>
          </div>

          <div className="pt-1">
            <span className="text-gray-500 dark:text-gray-400 block text-[11px]">গবেষণা ও সম্পাদনা পরিষদ:</span>
            <strong>তা'য়াল্লূম গবেষণা ও সম্পাদনা পরিষদ</strong>
          </div>
        </div>

        {/* Copyright Notice */}
        <div className="bg-amber-50 dark:bg-amber-950/30 p-4 rounded-2xl border border-amber-200 dark:border-amber-800/60 text-xs text-amber-950 dark:text-amber-200 space-y-2">
          <div className="font-bold flex items-center gap-1.5 text-amber-900 dark:text-amber-300">
            <ShieldCheck className="w-4 h-4" />
            <span>স্বত্বাধিকার ও কপিরাইট বিধান</span>
          </div>
          <p className="leading-relaxed bn-justify">
            তাফসীরুল জালালাইন বঙ্গানুবাদ ও প্রামাণ্য তাহকীক — সর্বস্বত্ব সংরক্ষিত: <strong>মুফতী মুহাম্মাদ মুহিব্বুল্লাহ</strong>।
          </p>
          <p className="text-[11px] text-amber-900/80 dark:text-amber-300/80 leading-relaxed bn-justify">
            দ্বীনি গবেষণা, ক্লাসে শিক্ষাদান ও দাওয়াতী প্রচারের স্বার্থে তথ্যসূত্র ও অনুবাদকের নাম উল্লেখসহ উন্মুক্ত ব্যবহার করা যাবে।
          </p>
        </div>

        {/* Close Button */}
        <button
          onClick={onClose}
          className="w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs sm:text-sm transition"
        >
          বন্ধ করুন
        </button>
      </div>
    </div>
  );
}
