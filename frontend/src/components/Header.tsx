'use client';

import React from 'react';
import Link from 'next/link';
import { useLanguage } from '../i18n/LanguageContext';
import { Language } from '../types';
import { Compass, MessageSquare, BookOpen, Info, ShieldCheck } from 'lucide-react';

export function Header() {
  const { language, setLanguage, t } = useLanguage();

  return (
    <header className="border-b border-gray-200 bg-white sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo / Brand */}
          <Link href="/" className="flex items-center space-x-3 group">
            <div className="w-10 h-10 rounded-lg bg-saarthi-700 flex items-center justify-center text-white shadow-md group-hover:bg-saarthi-800 transition">
              <Compass className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight text-navy-900 group-hover:text-saarthi-700 transition">
                {t.appName}
              </span>
              <span className="block text-xs font-medium text-gray-500">
                Maharashtra Guidance Platform
              </span>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="hidden md:flex space-x-6 text-sm font-medium text-gray-700">
            <Link href="/services" className="hover:text-saarthi-700 flex items-center space-x-1.5 transition">
              <BookOpen className="w-4 h-4 text-saarthi-600" />
              <span>{t.browseAllServices}</span>
            </Link>
            <Link href="/assistant" className="hover:text-saarthi-700 flex items-center space-x-1.5 transition">
              <MessageSquare className="w-4 h-4 text-saarthi-600" />
              <span>{t.askAssistant}</span>
            </Link>
            <Link href="/about" className="hover:text-saarthi-700 flex items-center space-x-1.5 transition">
              <Info className="w-4 h-4 text-gray-500" />
              <span>{t.about}</span>
            </Link>
          </nav>

          {/* Language Selector */}
          <div className="flex items-center space-x-2">
            <div className="bg-gray-100 p-1 rounded-lg flex space-x-1 border border-gray-200">
              {(['en', 'hi', 'mr'] as Language[]).map((lang) => (
                <button
                  key={lang}
                  onClick={() => setLanguage(lang)}
                  className={`px-2.5 py-1 text-xs font-semibold rounded-md transition ${
                    language === lang
                      ? 'bg-saarthi-700 text-white shadow-xs'
                      : 'text-gray-600 hover:text-navy-900 hover:bg-gray-200'
                  }`}
                >
                  {lang === 'en' ? 'English' : lang === 'hi' ? 'हिन्दी' : 'मराठी'}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
