/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Sōvēs design system — dark luxury
        void: '#070D14',       // near-black background
        abyss: '#0D1825',      // card/surface
        slate: '#1A3C5E',      // navy accent
        gold: '#F4A535',       // amber primary
        'gold-dim': '#C4821E', // amber dark
        'gold-light': '#FFD080', // amber light
        mist: '#8BA4BC',       // muted text
        frost: '#D0DDE8',      // light text
        snow: '#F0F5FA',       // near-white
      },
      fontFamily: {
        display: ['"Cinzel"', 'Georgia', 'serif'],
        body: ['"Inter"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-gold': 'pulseGold 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: { from: { opacity: 0 }, to: { opacity: 1 } },
        slideUp: { from: { opacity: 0, transform: 'translateY(12px)' }, to: { opacity: 1, transform: 'translateY(0)' } },
        pulseGold: {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(244, 165, 53, 0)' },
          '50%': { boxShadow: '0 0 0 6px rgba(244, 165, 53, 0.15)' },
        },
      },
    },
  },
  plugins: [],
}
