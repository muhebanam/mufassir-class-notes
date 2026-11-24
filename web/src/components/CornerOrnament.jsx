import React from 'react';

export default function CornerOrnament({ color = 'currentColor', className = '' }) {
  return (
    <svg
      viewBox="0 0 40 40"
      fill="none"
      className={`w-7 h-7 pointer-events-none select-none opacity-60 ${className}`}
      aria-hidden="true"
    >
      <path
        d="M2 38V12C2 6.477 6.477 2 12 2H38"
        stroke={color}
        strokeWidth="1.5"
      />
      <path
        d="M7 34V14C7 10.134 10.134 7 14 7H34"
        stroke={color}
        strokeWidth="1"
        strokeDasharray="2 2"
      />
      <circle cx="11" cy="11" r="2" fill={color} />
    </svg>
  );
}
