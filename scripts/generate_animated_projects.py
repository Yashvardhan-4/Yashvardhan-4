import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math
import os

BG_COLOR = (13, 17, 23)
SURFACE_COLOR = (22, 27, 34)
BORDER_COLOR = (48, 54, 61)

FONT_PATH = "C:\\Windows\\Fonts\\bahnschrift.ttf"
FONT_MONO_PATH = "C:\\Windows\\Fonts\\consola.ttf"

font_title = ImageFont.truetype(FONT_PATH, 16)
font_sub = ImageFont.truetype(FONT_PATH, 13)
font_mono = ImageFont.truetype(FONT_MONO_PATH, 11)
font_mono_small = ImageFont.truetype(FONT_MONO_PATH, 10)
font_big_speed = ImageFont.truetype(FONT_PATH, 24)
font_body = ImageFont.truetype(FONT_PATH, 15)

# ==============================================================================
# 1. TURBOIDM ANIMATED SIMULATOR
# ==============================================================================
def generate_turboidm_simulator():
    print("Generating TurboIDM Animated UI Simulator...")
    w, h = 880, 420
    n_frames = 36
    fps = 25
    duration = int(1000 / fps)
    
    frames = []
    
    for f in range(n_frames):
        phase = 2.0 * np.pi * f / n_frames
        
        img = Image.new("RGB", (w, h), BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        # Window Shell
        draw.rounded_rectangle([20, 16, w - 20, h - 16], radius=10, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
        
        # Window Titlebar
        draw.ellipse([40, 34, 50, 44], fill=(239, 68, 68))
        draw.ellipse([58, 34, 68, 44], fill=(234, 179, 8))
        draw.ellipse([76, 34, 86, 44], fill=(34, 197, 94))
        
        draw.text((105, 32), "turbo-idm.app // FAST PARALLEL DOWNLOAD ACCELERATOR", fill=(139, 148, 158), font=font_mono)
        draw.text((w - 230, 32), "STATUS: 32 ACTIVE THREADS", fill=(56, 189, 248), font=font_mono)
        
        draw.line([(20, 58), (w - 20, 58)], fill=BORDER_COLOR, width=1)
        
        # File Download Item Card
        draw.text((40, 80), "debian-12.8.0-amd64-netinst.iso", fill=(240, 246, 252), font=font_title)
        draw.text((40, 104), "SOURCE: cdn.debian.org/iso/debian-12.8.0.iso  [4.2 GB]", fill=(139, 148, 158), font=font_mono)
        
        # Live Speed Counter
        speed_mb = 138.4 + 14.0 * np.sin(phase * 2.0)
        draw.text((w - 280, 80), f"{speed_mb:.1f} MB/s", fill=(56, 189, 248), font=font_big_speed)
        draw.text((w - 280, 110), "8x ACCELERATION ACTIVE", fill=(34, 197, 94), font=font_mono_small)
        
        # Overall Progress Bar
        overall_progress = 0.55 + 0.38 * (f / n_frames)
        bar_w = w - 80
        draw.rounded_rectangle([40, 138, 40 + bar_w, 154], radius=4, fill=(13, 17, 23))
        draw.rounded_rectangle([40, 138, 40 + int(bar_w * overall_progress), 154], radius=4, fill=(56, 189, 248))
        
        draw.text((40, 164), f"COMPLETED: {overall_progress * 100:.1f}%  |  ETA: 4 SECONDS", fill=(139, 148, 158), font=font_mono_small)
        draw.text((w - 210, 164), "DIRECT TO DISK (ZERO MERGE)", fill=(234, 179, 8), font=font_mono_small)
        
        # 32 Parallel Streams Grid (8 columns x 4 rows)
        draw.text((40, 198), "PARALLEL STREAM MATRIX (32 CONCURRENT HTTP/2 CHUNKS):", fill=(201, 209, 217), font=font_mono)
        
        chunk_w = (w - 80 - 7 * 8) / 8
        chunk_h = 24
        
        for r in range(4):
            for c in range(8):
                idx = r * 8 + c
                cx = 40 + c * (chunk_w + 8)
                cy = 224 + r * (chunk_h + 8)
                
                # Dynamic stream fill with animated waves
                stream_phase = phase + idx * 0.4
                stream_fill = np.clip(0.4 + 0.6 * np.sin(stream_phase), 0.1, 1.0)
                
                draw.rectangle([cx, cy, cx + chunk_w, cy + chunk_h], fill=(13, 17, 23), outline=BORDER_COLOR)
                draw.rectangle([cx, cy, cx + chunk_w * stream_fill, cy + chunk_h], fill=(30, 64, 120))
                draw.rectangle([cx, cy, cx + chunk_w * stream_fill * 0.9, cy + chunk_h], fill=(56, 189, 248))
                
                draw.text((cx + 6, cy + 6), f"T{idx+1:02d}", fill=(240, 246, 252), font=font_mono_small)
                draw.text((cx + chunk_w - 28, cy + 6), f"{int(stream_fill*100)}%", fill=(139, 148, 158), font=font_mono_small)
                
        # Bottom Status Bar
        draw.line([(20, h - 54), (w - 20, h - 54)], fill=BORDER_COLOR, width=1)
        draw.text((40, h - 38), "BENCHMARK: 8X VELOCITY BOOST  ·  NODE.JS + ELECTRON + REACT 19 + CHROME MV3", fill=(139, 148, 158), font=font_mono_small)
        draw.text((w - 240, h - 38), "LIVE: turbo-idm.vercel.app", fill=(56, 189, 248), font=font_mono_small)
        
        frames.append(img)
        
    out_file = "assets/turboidm_animated.webp"
    frames[0].save(out_file, save_all=True, append_images=frames[1:], duration=duration, loop=0, quality=90, method=4)
    print(f"TurboIDM animated: {out_file}, {os.path.getsize(out_file)/1024:.1f} KB")


# ==============================================================================
# 2. INKLESS ANIMATED SIMULATOR
# ==============================================================================
def generate_inkless_simulator():
    print("Generating Inkless Animated UI Simulator...")
    w, h = 880, 420
    n_frames = 36
    fps = 25
    duration = int(1000 / fps)
    
    full_sentence = "The best ideas are born in quiet spaces where thought flows uninterrupted..."
    
    frames = []
    
    for f in range(n_frames):
        phase = 2.0 * np.pi * f / n_frames
        
        img = Image.new("RGB", (w, h), BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        # Window Shell
        draw.rounded_rectangle([20, 16, w - 20, h - 16], radius=10, fill=(10, 12, 16), outline=BORDER_COLOR, width=1)
        
        # Window Titlebar
        draw.ellipse([40, 34, 50, 44], fill=(48, 54, 61))
        draw.ellipse([58, 34, 68, 44], fill=(48, 54, 61))
        draw.ellipse([76, 34, 86, 44], fill=(48, 54, 61))
        
        draw.text((105, 32), "inkless-ashen.vercel.app // DISTRACTION-FREE DIGITAL JOURNAL", fill=(139, 148, 158), font=font_mono)
        
        # Local Sync Status with subtle pulse
        sync_saved = (f % 12 > 2)
        status_col = (34, 197, 94) if sync_saved else (234, 179, 8)
        status_text = "INDEXEDDB SAVED < 2ms [ONLINE / OFFLINE]" if sync_saved else "SYNCING BUFFER..."
        draw.text((w - 290, 32), status_text, fill=status_col, font=font_mono)
        
        draw.line([(20, 58), (w - 20, 58)], fill=BORDER_COLOR, width=1)
        
        # Ambient subtle canvas glow in center
        cx, cy = w / 2.0, h / 2.0 + 20
        y_g, x_g = np.ogrid[60:h-55, 25:w-25]
        dist_g = np.sqrt(((x_g - cx)/320.0)**2 + ((y_g - cy)/140.0)**2)
        ambient_mask = np.clip(1.0 - dist_g, 0.0, 1.0)**2.0
        # Gentle wave modulation
        wave = 0.5 + 0.5 * math.sin(phase)
        
        # Journal Title
        draw.text((60, 95), "November Reflections // The Speed of Thought", fill=(240, 246, 252), font=font_title)
        draw.text((60, 124), "120 FPS FLUID TEXT CANVAS  ·  ZERO DATA LOSS GUARANTEE", fill=(139, 148, 158), font=font_mono_small)
        
        # Dynamic typewriter text
        num_chars = int((f / n_frames) * len(full_sentence))
        current_text = full_sentence[:num_chars]
        
        draw.text((60, 180), current_text, fill=(230, 235, 245), font=font_body)
        
        # Cursor
        bbox = draw.textbbox((60, 180), current_text, font=font_body)
        cur_x = bbox[2] + 4 if num_chars > 0 else 60
        if math.sin(phase * 4.0) > -0.2:
            draw.rectangle([cur_x, 178, cur_x + 2, 198], fill=(56, 189, 248))
            
        # Subtle journal excerpt lines below
        draw.text((60, 230), "Writing without friction transforms fleeting thoughts into permanent structures.", fill=(110, 118, 129), font=font_body)
        draw.text((60, 260), "Every keystroke commits atomically to IndexedDB with zero latency.", fill=(85, 95, 105), font=font_body)
        
        # Bottom Status Bar
        draw.line([(20, h - 54), (w - 20, h - 54)], fill=BORDER_COLOR, width=1)
        draw.text((40, h - 38), "BENCHMARK: < 5MS LOCAL SAVE  ·  NEXT.JS + THREE.JS + INDEXEDDB + SUPABASE", fill=(139, 148, 158), font=font_mono_small)
        draw.text((w - 240, h - 38), "LIVE: inkless-ashen.vercel.app", fill=(56, 189, 248), font=font_mono_small)
        
        frames.append(img)
        
    out_file = "assets/inkless_animated.webp"
    frames[0].save(out_file, save_all=True, append_images=frames[1:], duration=duration, loop=0, quality=90, method=4)
    print(f"Inkless animated: {out_file}, {os.path.getsize(out_file)/1024:.1f} KB")


# ==============================================================================
# 3. SHIVKUSH NURSERY ANIMATED SIMULATOR
# ==============================================================================
def generate_shivkush_simulator():
    print("Generating Shivkush Nursery 3D Viewer Simulator...")
    w, h = 880, 420
    n_frames = 36
    fps = 25
    duration = int(1000 / fps)
    
    # 3D Botanical phyllotaxis wireframe
    n_pts = 48
    pts = []
    for i in range(n_pts):
        theta = i * 2.39996
        rad = 14.0 + math.sqrt(i) * 15.0
        z_c = (i - n_pts/2) * 5.0
        x_c = rad * math.cos(theta)
        y_c = rad * math.sin(theta)
        pts.append((x_c, y_c, z_c))
        
    frames = []
    
    for f in range(n_frames):
        phase = 2.0 * np.pi * f / n_frames
        
        img = Image.new("RGB", (w, h), BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        # Window Shell
        draw.rounded_rectangle([20, 16, w - 20, h - 16], radius=10, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
        
        # Window Titlebar
        draw.ellipse([40, 34, 50, 44], fill=(48, 54, 61))
        draw.ellipse([58, 34, 68, 44], fill=(48, 54, 61))
        draw.ellipse([76, 34, 86, 44], fill=(48, 54, 61))
        
        draw.text((105, 32), "shivkush-nursery.app // COMMERCIAL AGRO-ECOMMERCE & 3D CANOPY", fill=(139, 148, 158), font=font_mono)
        draw.text((w - 230, 32), "DRACO 3D ENGINE // 60 FPS", fill=(34, 197, 94), font=font_mono)
        
        draw.line([(20, 58), (w - 20, 58)], fill=BORDER_COLOR, width=1)
        
        # Left Panel: Product & Spec Information
        draw.text((40, 85), "Mahogany & Teak Horticultural Specimen", fill=(240, 246, 252), font=font_title)
        draw.text((40, 110), "COMMERCIAL B2B BULK CONTRACT ENGINE  [मराठी / ENGLISH]", fill=(34, 197, 94), font=font_mono_small)
        
        draw.text((40, 145), "CANOPY METRICS", fill=(139, 148, 158), font=font_mono_small)
        draw.text((40, 165), "· Draco Geometry: 84% Compression", fill=(201, 209, 217), font=font_sub)
        draw.text((40, 188), "· 2G/3G Optimized: Sub-second Load", fill=(201, 209, 217), font=font_sub)
        draw.text((40, 211), "· Live Inventory: 4,500 Units Available", fill=(201, 209, 217), font=font_sub)
        draw.text((40, 234), "· Zero Stock Conflicts via PostgreSQL RLS", fill=(201, 209, 217), font=font_sub)
        
        draw.rounded_rectangle([40, 275, 220, 310], radius=6, fill=(34, 197, 94, 40), outline=(34, 197, 94))
        draw.text((54, 285), "ONLINE ORDERING ACTIVE", fill=(34, 197, 94), font=font_mono_small)
        
        # Right Viewport: Rotating 3D Specimen
        cx, cy = w * 0.65, h * 0.52
        draw.rectangle([w * 0.45, 75, w - 40, h - 70], fill=(10, 13, 18), outline=BORDER_COLOR)
        draw.text((w * 0.45 + 16, 90), f"3D CANOPY VIEWPORT  [ROTATION: {int(math.degrees(phase)):03d}°]", fill=(139, 148, 158), font=font_mono_small)
        
        rot_y = phase
        rot_x = 0.35 + 0.1 * math.sin(phase * 0.5)
        
        proj = []
        for px, py, pz in pts:
            rx = px * math.cos(rot_y) + pz * math.sin(rot_y)
            ry = py
            rz = -px * math.sin(rot_y) + pz * math.cos(rot_y)
            
            rx2 = rx
            ry2 = ry * math.cos(rot_x) - rz * math.sin(rot_x)
            rz2 = ry * math.sin(rot_x) + rz * math.cos(rot_x)
            
            fov = 320.0
            scale = fov / (fov + rz2)
            sx = cx + rx2 * scale
            sy = cy + ry2 * scale
            proj.append((sx, sy, rz2, scale))
            
        # Draw wireframe lines
        for i in range(len(proj) - 1):
            x1, y1, z1, s1 = proj[i]
            x2, y2, z2, s2 = proj[i+1]
            depth = np.clip((z1 + 160.0) / 320.0, 0.15, 1.0)
            draw.line([(x1, y1), (x2, y2)], fill=(int(20*depth), int(180*depth), int(100*depth)), width=1)
            
        # Draw botanical nodes
        for sx, sy, sz, sc in proj:
            depth = np.clip((sz + 160.0) / 320.0, 0.2, 1.0)
            r_dot = int(3.0 * sc)
            draw.ellipse([sx - r_dot, sy - r_dot, sx + r_dot, sy + r_dot], fill=(int(34*depth), int(220*depth), int(120*depth)))
            
        # Bottom Status Bar
        draw.line([(20, h - 54), (w - 20, h - 54)], fill=BORDER_COLOR, width=1)
        draw.text((40, h - 38), "BENCHMARK: 84% DRACO COMPRESSION  ·  NEXT.JS + THREE.JS + POSTGRESQL + TAILWIND", fill=(139, 148, 158), font=font_mono_small)
        draw.text((w - 240, h - 38), "LIVE: shivkush-hi-tech-nursery.vercel.app", fill=(34, 197, 94), font=font_mono_small)
        
        frames.append(img)
        
    out_file = "assets/shivkush_animated.webp"
    frames[0].save(out_file, save_all=True, append_images=frames[1:], duration=duration, loop=0, quality=90, method=4)
    print(f"Shivkush animated: {out_file}, {os.path.getsize(out_file)/1024:.1f} KB")

if __name__ == "__main__":
    generate_turboidm_simulator()
    generate_inkless_simulator()
    generate_shivkush_simulator()
    print("ALL PROJECT ANIMATORS COMPLETED.")
