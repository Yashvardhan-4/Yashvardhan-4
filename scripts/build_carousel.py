import os

tech_items = [
    ("C++", "#00599C", "cpp"),
    ("JavaScript", "#F7DF1E", "js"),
    ("TypeScript", "#3178C6", "ts"),
    ("Python", "#3776AB", "py"),
    ("React 19", "#61DAFB", "react"),
    ("Next.js 16", "#FFFFFF", "nextjs"),
    ("Three.js", "#A855F7", "threejs"),
    ("Tailwind", "#38BDF8", "tailwind"),
    ("PostgreSQL", "#336791", "postgres"),
    ("Supabase", "#3ECF8E", "supabase"),
    ("MongoDB", "#47A248", "mongodb"),
    ("Electron", "#47848F", "electron"),
    ("Docker", "#2496ED", "docker"),
    ("Figma", "#F24E1E", "figma"),
]

card_w = 125
card_h = 42
gap = 14
step = card_w + gap
total_w = len(tech_items) * step

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 64" width="100%" height="64">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600&amp;family=Fira+Code:wght@600&amp;display=swap');
      
      .pill-card {{
        rx: 8px;
        ry: 8px;
        fill: #161b22;
        stroke: #30363d;
        stroke-width: 1px;
      }}
      
      .pill-text {{
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        font-size: 13px;
        font-weight: 600;
        fill: #e6edf3;
      }}

      .track {{
        animation: scrollCarousel 22s linear infinite;
      }}

      @keyframes scrollCarousel {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-{total_w}px); }}
      }}

      .fade-left {{
        fill: url(#fadeL);
      }}
      .fade-right {{
        fill: url(#fadeR);
      }}
    </style>

    <linearGradient id="fadeL" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0d1117" stop-opacity="1" />
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />
    </linearGradient>

    <linearGradient id="fadeR" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0d1117" stop-opacity="0" />
      <stop offset="100%" stop-color="#0d1117" stop-opacity="1" />
    </linearGradient>

    <g id="carouselTrack">
'''

for i, (name, color, key) in enumerate(tech_items):
    x_pos = i * step
    svg_content += f'''      <g transform="translate({x_pos}, 11)">
        <rect width="{card_w}" height="{card_h}" class="pill-card" stroke="{color}" stroke-opacity="0.35" />
        <circle cx="20" cy="{card_h//2}" r="5" fill="{color}" />
        <text x="34" y="{card_h//2 + 5}" class="pill-text">{name}</text>
      </g>
'''

svg_content += f'''    </g>
  </defs>

  <rect width="920" height="64" fill="#0d1117" />

  <g class="track">
    <use href="#carouselTrack" x="0" />
    <use href="#carouselTrack" x="{total_w}" />
    <use href="#carouselTrack" x="{total_w * 2}" />
  </g>

  <!-- Left and Right Gradient Fades for Infinite Horizon -->
  <rect x="0" y="0" width="70" height="64" class="fade-left" pointer-events="none" />
  <rect x="850" y="0" width="70" height="64" class="fade-right" pointer-events="none" />
</svg>
'''

with open('assets/tech_carousel.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print(f"Generated assets/tech_carousel.svg ({total_w}px total width)")
