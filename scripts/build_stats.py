svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 195" width="100%" height="auto">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@500;600;700&amp;family=Plus+Jakarta+Sans:wght@500;600;700&amp;display=swap');
      
      .panel-box {
        fill: #161b22;
        stroke: #30363d;
        stroke-width: 1px;
        rx: 10px;
        ry: 10px;
      }
      
      .panel-title {
        font-family: 'Fira Code', monospace;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        fill: #8b949e;
      }

      .metric-label {
        font-family: 'Fira Code', monospace;
        font-size: 12px;
        fill: #8b949e;
      }

      .metric-value {
        font-family: 'Fira Code', monospace;
        font-size: 13px;
        font-weight: 700;
        fill: #e6edf3;
      }

      .lang-name {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 12px;
        font-weight: 500;
        fill: #c9d1d9;
      }

      .lang-pct {
        font-family: 'Fira Code', monospace;
        font-size: 11px;
        font-weight: 600;
        fill: #8b949e;
      }

      .beacon {
        fill: #00E5FF;
        animation: pulseB 2s infinite;
      }

      @keyframes pulseB {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
      }

      .bar-fill {
        animation: loadBar 1.5s ease-out forwards;
      }
    </style>

    <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00E5FF" />
      <stop offset="100%" stop-color="#a855f7" />
    </linearGradient>
  </defs>

  <rect width="920" height="195" fill="#0d1117" />

  <!-- LEFT PANEL: GITHUB STATS & METRICS -->
  <g transform="translate(16, 10)">
    <rect width="436" height="175" class="panel-box" />

    <!-- Title -->
    <g transform="translate(20, 24)">
      <circle cx="0" cy="0" r="3.5" class="beacon" />
      <text x="12" y="4" class="panel-title">GITHUB TELEMETRY // VERIFIED METRICS</text>
    </g>

    <!-- Metrics List -->
    <g transform="translate(20, 56)">
      <text y="0" class="metric-label">★ Total Repositories:</text>
      <text x="195" y="0" class="metric-value">16 Repos</text>

      <text y="26" class="metric-label">⚡ Total Contributions:</text>
      <text x="195" y="26" class="metric-value" fill="#00E5FF">260+ Commits</text>

      <text y="52" class="metric-label">🎯 Academic Standing:</text>
      <text x="195" y="52" class="metric-value">PCCOE Pune (CGPA: 8.86)</text>

      <text y="78" class="metric-label">🏆 Certifications:</text>
      <text x="195" y="78" class="metric-value" fill="#fbbf24">NPTEL Elite · CodeChef 2★</text>

      <text y="104" class="metric-label">🛡️ Active Status:</text>
      <text x="195" y="104" class="metric-value" fill="#22c55e">Available for Collabs</text>
    </g>

    <!-- Visual Activity Ring Badge (Right side of left panel) -->
    <g transform="translate(375, 105)">
      <circle cx="0" cy="0" r="32" fill="none" stroke="#21262d" stroke-width="5" />
      <circle cx="0" cy="0" r="32" fill="none" stroke="url(#ringGrad)" stroke-width="5" stroke-dasharray="201" stroke-dashoffset="35" stroke-linecap="round" transform="rotate(-90)" />
      <text x="0" y="5" font-family="'Fira Code', monospace" font-size="16" font-weight="700" fill="#00E5FF" text-anchor="middle">A+</text>
      <text x="0" y="48" font-family="'Fira Code', monospace" font-size="9" fill="#7d8590" text-anchor="middle">ACTIVITY</text>
    </g>
  </g>

  <!-- RIGHT PANEL: TOP LANGUAGES BREAKDOWN -->
  <g transform="translate(468, 10)">
    <rect width="436" height="175" class="panel-box" />

    <!-- Title -->
    <g transform="translate(20, 24)">
      <circle cx="0" cy="0" r="3.5" fill="#38bdf8" />
      <text x="12" y="4" class="panel-title">MOST USED LANGUAGES // BREAKDOWN</text>
    </g>

    <!-- Multi-Segment Color Progress Bar -->
    <g transform="translate(20, 48)">
      <rect width="396" height="10" rx="5" ry="5" fill="#21262d" />
      <!-- JS: 58.0% -> 229.6px -->
      <rect x="0" y="0" width="230" height="10" rx="5" ry="5" fill="#F7DF1E" />
      <!-- HTML: 13.8% -> 54.6px -->
      <rect x="230" y="0" width="55" height="10" fill="#E34F26" />
      <!-- TS: 9.3% -> 36.8px -->
      <rect x="285" y="0" width="37" height="10" fill="#3178C6" />
      <!-- Python: 9.1% -> 36.0px -->
      <rect x="322" y="0" width="36" height="10" fill="#3776AB" />
      <!-- CSS: 5.5% -> 21.7px -->
      <rect x="358" y="0" width="22" height="10" fill="#563D7C" />
      <!-- C++: 4.3% -> 17.0px -->
      <rect x="380" y="0" width="16" height="10" rx="5" ry="5" fill="#F34B7D" />
    </g>

    <!-- Language Key Grid (2 Columns) -->
    <!-- Col 1 -->
    <g transform="translate(20, 80)">
      <!-- JavaScript -->
      <circle cx="5" cy="5" r="4.5" fill="#F7DF1E" />
      <text x="16" y="9" class="lang-name">JavaScript</text>
      <text x="135" y="9" class="lang-pct">58.0%</text>

      <!-- TypeScript -->
      <circle cx="5" cy="29" r="4.5" fill="#3178C6" />
      <text x="16" y="33" class="lang-name">TypeScript</text>
      <text x="135" y="33" class="lang-pct">9.3%</text>

      <!-- CSS -->
      <circle cx="5" cy="53" r="4.5" fill="#563D7C" />
      <text x="16" y="57" class="lang-name">CSS</text>
      <text x="135" y="57" class="lang-pct">5.5%</text>
    </g>

    <!-- Col 2 -->
    <g transform="translate(230, 80)">
      <!-- HTML -->
      <circle cx="5" cy="5" r="4.5" fill="#E34F26" />
      <text x="16" y="9" class="lang-name">HTML</text>
      <text x="135" y="9" class="lang-pct">13.8%</text>

      <!-- Python -->
      <circle cx="5" cy="29" r="4.5" fill="#3776AB" />
      <text x="16" y="33" class="lang-name">Python</text>
      <text x="135" y="33" class="lang-pct">9.1%</text>

      <!-- C++ -->
      <circle cx="5" cy="53" r="4.5" fill="#F34B7D" />
      <text x="16" y="57" class="lang-name">C++</text>
      <text x="135" y="57" class="lang-pct">4.3%</text>
    </g>
  </g>
</svg>
'''

with open('assets/github_stats.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("Generated assets/github_stats.svg successfully")
