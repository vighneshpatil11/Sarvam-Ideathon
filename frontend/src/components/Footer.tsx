'use client';

import React from 'react';
import Link from 'next/link';
import { useLanguage } from '../i18n/LanguageContext';
import { ShieldAlert, ExternalLink, HelpCircle } from 'lucide-react';

export function Footer() {
  const { t } = useLanguage();

  return (
    <footer className="bg-slate-900 text-slate-300 border-t border-slate-800 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Mandatory Transparency Disclaimer Box */}
        <div className="bg-slate-800/80 border border-amber-500/30 rounded-xl p-5 mb-8 flex items-start space-x-3 text-amber-200/90 text-sm">
          <ShieldAlert className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold text-amber-300">Official Disclaimer: </span>
            {t.disclaimerBanner}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8 text-sm">
          <div>
            <h4 className="text-white font-semibold text-base mb-3">{t.appName}</h4>
            <p className="text-slate-400 text-xs leading-relaxed">
              An independent multilingual public service navigation initiative for citizens in Maharashtra (Pilot: Pune district). Built to eliminate reliance on predatory commercial intermediaries.
            </p>
          </div>

          <div>
            <h4 className="text-white font-semibold text-base mb-3">Official Government Portals</h4>
            <ul className="space-y-2 text-xs text-slate-400">
              <li>
                <a 
                  href="https://aaplesarkar.mahaonline.gov.in" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="hover:text-amber-400 flex items-center space-x-1"
                >
                  <span>Aaple Sarkar (आपले सरकार)</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a 
                  href="https://mahadbt.maharashtra.gov.in" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="hover:text-amber-400 flex items-center space-x-1"
                >
                  <span>MahaDBT Scholarship Portal</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a 
                  href="https://pune.gov.in" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="hover:text-amber-400 flex items-center space-x-1"
                >
                  <span>Pune District Collectorate</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-white font-semibold text-base mb-3">Platform Governance</h4>
            <ul className="space-y-2 text-xs text-slate-400">
              <li><Link href="/about" className="hover:text-white">{t.about}</Link></li>
              <li><Link href="/feedback" className="hover:text-white">{t.feedback}</Link></li>
              <li><Link href="/admin" className="hover:text-white">{t.admin}</Link></li>
              <li className="text-slate-500">Pilot Version 1.0.0 (Maharashtra)</li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-800 pt-6 text-center text-xs text-slate-500">
          © {new Date().getFullYear()} SAARTHI. Zero commercial monetization. Grounded strictly in verified government publications.
        </div>
      </div>
    </footer>
  );
}
