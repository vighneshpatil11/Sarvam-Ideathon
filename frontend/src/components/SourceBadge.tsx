import React from 'react';
import { ShieldCheck, Clock } from 'lucide-react';

interface SourceBadgeProps {
  status: string;
  lastVerifiedAt?: string;
}

export function SourceBadge({ status, lastVerifiedAt }: SourceBadgeProps) {
  const isVerified = status === 'verified';

  return (
    <div className="inline-flex items-center space-x-2 text-xs">
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full font-medium ${
        isVerified ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' : 'bg-amber-100 text-amber-800 border border-amber-200'
      }`}>
        <ShieldCheck className="w-3.5 h-3.5 mr-1" />
        {isVerified ? 'Official Verified' : 'Under Review'}
      </span>
      {lastVerifiedAt && (
        <span className="text-gray-500 inline-flex items-center text-xs">
          <Clock className="w-3 h-3 mr-1 text-gray-400" />
          {lastVerifiedAt}
        </span>
      )}
    </div>
  );
}
