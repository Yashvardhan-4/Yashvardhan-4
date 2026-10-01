import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

# GitHub dark background color
BG_COLOR = (13, 17, 23)
BG_RGB_NP = np.array([13, 17, 23], dtype=np.float32)

FONT_LARGE_PATH = "C:\\Windows\\Fonts\\bahnschrift.ttf"
FONT_MONO_PATH = "C:\\Windows\\Fonts\\consola.ttf"

font_hero = ImageFont.truetype(FONT_LARGE_PATH, 58)
font_sub = ImageFont.truetype(FONT_LARGE_PATH, 13)
font_title = ImageFont.truetype(FONT_LARGE_PATH, 22)
font_body = ImageFont.truetype(FONT_LARGE_PATH, 14)
font_mono = ImageFont.truetype(FONT_MONO_PATH, 11)
font_mono_small = ImageFont.truetype(FONT_MONO_PATH, 9)

# ==============================================================================
# 1. HERO: MOLTEN LIQUID CHROME / MERCURY ENGINE
# ==============================================================================
def generate_hero():
    print("Generating Hero Liquid Chrome...")
    w, h = 880, 380
    n_frames = 36
    fps = 25
    duration = int(1000 / fps)
    
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2.0, h / 2.0 + 12
    
    nx = (x - cx) / 360.0
    ny = (y - cy) / 160.0
    dist = np.sqrt(nx**2 + ny**2)
    
    frames = []
    
    for f in range(n_frames):
        phase = 2.0 * np.pi * f / n_frames
        
        # Complex multi-octave viscous liquid fluid heightmap
        # Wave 1: Large sweeping swells
        z1 = np.sin(nx * 2.8 + np.cos(phase) * 1.8 + ny * 1.5) * np.cos(ny * 2.4 + np.sin(phase) * 1.4 - nx * 1.2)
        # Wave 2: Fast counter-rotating ripples (creates liquid mercury tension)
        z2 = 0.45 * np.sin(nx * 5.2 - phase * 2.0 + ny * 3.8 + np.cos(phase * 1.5))
        # Wave 3: Radial ripple emitting from center
        r_dist = np.sqrt(nx**2 * 1.2 + ny**2 * 2.5)
        z3 = 0.35 * np.cos(r_dist * 8.0 - phase * 2.0)
        # Wave 4: High-frequency surface ripple
        z4 = 0.20 * np.sin(nx * 9.0 + ny * 7.0 + phase * 3.0)
        
        z = z1 + z2 + z3 + z4
        
        # Organic fluid drop / pool envelope mask
        envelope = np.clip(1.0 - (dist / 1.42)**2, 0.0, 1.0)**2.0
        z_masked = z * envelope
        
        # Calculate surface normal vectors via spatial gradient
        dz_dx = np.gradient(z_masked, axis=1) * 12.0
        dz_dy = np.gradient(z_masked, axis=0) * 12.0
        
        len_n = np.sqrt(dz_dx**2 + dz_dy**2 + 1.0)
        nx_n = -dz_dx / len_n
        ny_n = -dz_dy / len_n
        nz_n = 1.0 / len_n
        
        # Studio Light 1: Overhead key chrome reflection
        lx1, ly1, lz1 = np.sin(phase) * 0.35 - 0.4, -0.65, 0.75
        l_norm = np.sqrt(lx1**2 + ly1**2 + lz1**2)
        lx1, ly1, lz1 = lx1/l_norm, ly1/l_norm, lz1/l_norm
        
        # Halfway vector
        hx, hy, hz = lx1, ly1, lz1 + 1.0
        h_norm = np.sqrt(hx**2 + hy**2 + hz**2)
        hx, hy, hz = hx/h_norm, hy/h_norm, hz/h_norm
        
        ndoth = np.clip(nx_n * hx + ny_n * hy + nz_n * hz, 0.0, 1.0)
        
        # Multiple specular lobes for metallic liquid chrome sheen
        spec_tight = ndoth**48.0   # pinpoint mercury glint
        spec_mid = ndoth**16.0     # silky chrome shine
        spec_broad = ndoth**4.0    # ambient liquid reflection
        
        # Studio Light 2: Subtle bottom-right electric cyan rim light
        lx2, ly2, lz2 = 0.6, 0.5, 0.4
        diffuse2 = np.clip(nx_n * lx2 + ny_n * ly2 + nz_n * lz2, 0.0, 1.0)
        
        # Fresnel edge calculation (metallic look)
        fresnel = np.clip(1.0 - nz_n, 0.0, 1.0)**2.2
        
        # Iridescent chromatic fringe based on curvature and angle
        angle = np.arctan2(ny_n, nx_n) + phase
        r_fringe = 0.5 + 0.5 * np.cos(angle)
        g_fringe = 0.5 + 0.5 * np.cos(angle + 2.094)
        b_fringe = 0.5 + 0.5 * np.cos(angle + 4.188)
        
        # Composite metallic color
        chrome_val = (spec_broad * 0.25 + spec_mid * 0.55 + spec_tight * 1.1) * envelope
        
        r_chan = BG_RGB_NP[0] + chrome_val * 225 + fresnel * envelope * (r_fringe * 60 + 20)
        g_chan = BG_RGB_NP[1] + chrome_val * 230 + fresnel * envelope * (g_fringe * 90 + diffuse2 * 40)
        b_chan = BG_RGB_NP[2] + chrome_val * 245 + fresnel * envelope * (b_fringe * 140 + diffuse2 * 70)
        
        # Core fluid ambient illumination
        ambient_core = np.exp(-dist * 2.2) * envelope * 0.28
        r_chan += ambient_core * 35
        g_chan += ambient_core * 65
        b_chan += ambient_core * 110
        
        img_arr = np.stack([np.clip(r_chan, 0, 255), np.clip(g_chan, 0, 255), np.clip(b_chan, 0, 255)], axis=-1).astype(np.uint8)
        frame_img = Image.fromarray(img_arr, mode='RGB')
        
        # Draw typographic plate
        draw = ImageDraw.Draw(frame_img)
        
        # Hero Name: YASHVARDHAN
        name_str = "YASHVARDHAN"
        bbox = draw.textbbox((0, 0), name_str, font=font_hero)
        tw = bbox[2] - bbox[0]
        tx = int((w - tw) / 2)
        ty = int(cy - 46)
        
        # Subtle drop blur/shadow for optical contrast
        draw.text((tx, ty + 2), name_str, fill=(5, 8, 12), font=font_hero)
        # Crisp pure white display typography
        draw.text((tx, ty), name_str, fill=(248, 250, 255), font=font_hero)
        
        # Subtitle
        sub_str = "CREATIVE TECHNOLOGIST  ×  SOFTWARE ENGINEER"
        bbox_sub = draw.textbbox((0, 0), sub_str, font=font_sub)
        tw_sub = bbox_sub[2] - bbox_sub[0]
        tx_sub = int((w - tw_sub) / 2)
        ty_sub = ty + 70
        draw.text((tx_sub, ty_sub), sub_str, fill=(165, 185, 210), font=font_sub)
        
        # Editorial Micro-Metadata
        draw.text((32, 26), "MONUMENT // 01 · VOLUMETRIC FLUID DYNAMICS", fill=(110, 130, 155), font=font_mono)
        draw.text((w - 235, 26), "19.0760° N, 72.8777° E  [MUMBAI]", fill=(110, 130, 155), font=font_mono)
        
        draw.text((32, h - 36), "HIGH-VISCOSITY LIQUID CHROME CORE", fill=(85, 105, 125), font=font_mono)
        draw.text((w - 210, h - 36), f"ORBITAL LOOP // 60 FPS // V-4.0", fill=(85, 105, 125), font=font_mono)
        
        # Hairline alignment guides
        draw.line([(32, 44), (64, 44)], fill=(45, 58, 75), width=1)
        draw.line([(w - 64, 44), (w - 32, 44)], fill=(45, 58, 75), width=1)
        draw.line([(32, h - 46), (64, h - 46)], fill=(45, 58, 75), width=1)
        draw.line([(w - 64, h - 46), (w - 32, h - 46)], fill=(45, 58, 75), width=1)
        
        frames.append(frame_img)
        
    out_file = "assets/hero_liquid_chrome.webp"
    frames[0].save(out_file, save_all=True, append_images=frames[1:], duration=duration, loop=0, quality=90, method=4)
    print(f"Hero generated: {out_file}, {os.path.getsize(out_file)/1024:.1f} KB")


# ==============================================================================
# 2. TRACE-X: LIVING FORENSIC NODE INTELLIGENCE (FORCE-DIRECTED NETWORK)
# ==============================================================================
def generate_tracex_graph():
    print("Generating TRACE-X Dynamic Graph Simulation...")
    w, h = 880, 420
    n_frames = 36
    fps = 25
    duration = int(1000 / fps)
    
    # 22 nodes representing transaction accounts, synthetic identities, offshore trusts
    np.random.seed(42)
    num_nodes = 22
    
    # Base positions clustered into 3 communities
    cluster_centers = [
        (w * 0.35, h * 0.48),  # Primary cluster (Target Account Syndicate)
        (w * 0.65, h * 0.42),  # Secondary cluster (Offshore Layering Shells)
        (w * 0.50, h * 0.72)   # Smurfing intermediary nodes
    ]
    
    node_clusters = [0]*8 + [1]*8 + [2]*6
    base_pos = []
    for c in node_clusters:
        ccx, ccy = cluster_centers[c]
        ang = np.random.uniform(0, 2*np.pi)
        rad = np.random.uniform(30, 95)
        base_pos.append((ccx + rad * np.cos(ang), ccy + rad * np.sin(ang)))
        
    # Edges between nodes
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (4, 5), (5, 2), (2, 6), (6, 7), (7, 1),
        (8, 9), (9, 10), (10, 11), (11, 8), (8, 12), (12, 13), (13, 10), (10, 14), (14, 15),
        (16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 16),
        # Inter-cluster cross-flows (high-risk bridge links)
        (2, 8), (3, 12), (7, 16), (15, 18), (5, 20)
    ]
    
    frames = []
    
    for f in range(n_frames):
        phase = 2.0 * np.pi * f / n_frames
        
        # Create base canvas with dark background
        img = Image.new("RGB", (w, h), BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        # Dynamic node positions with harmonic gentle physics sway
        current_pos = []
        for i, (bx, by) in enumerate(base_pos):
            dx = 8.0 * np.sin(phase + i * 0.5)
            dy = 8.0 * np.cos(phase + i * 0.7)
            current_pos.append((bx + dx, by + dy))
            
        # Draw radar pulse expanding from target node (Node 2)
        pulse_r = (phase / (2 * np.pi) * 220) % 220
        t_pos = current_pos[2]
        pulse_bbox = [t_pos[0] - pulse_r, t_pos[1] - pulse_r, t_pos[0] + pulse_r, t_pos[1] + pulse_r]
        pulse_alpha = int(140 * (1.0 - pulse_r / 220))
        draw.ellipse(pulse_bbox, outline=(244, 63, 94), width=1)
        
        # Second counter-radar from offshore hub (Node 10)
        pulse_r2 = ((phase / (2 * np.pi) + 0.5) * 200) % 200
        t_pos2 = current_pos[10]
        pulse_bbox2 = [t_pos2[0] - pulse_r2, t_pos2[1] - pulse_r2, t_pos2[0] + pulse_r2, t_pos2[1] + pulse_r2]
        draw.ellipse(pulse_bbox2, outline=(6, 182, 212), width=1)
        
        # Draw edges
        for u, v in edges:
            x1, y1 = current_pos[u]
            x2, y2 = current_pos[v]
            
            is_cross = (node_clusters[u] != node_clusters[v])
            edge_color = (180, 50, 75) if is_cross else (35, 55, 75)
            draw.line([(x1, y1), (x2, y2)], fill=edge_color, width=2 if is_cross else 1)
            
            # Animate glowing data packets traveling along edges
            packet_t = (phase / (2 * np.pi) * 3.0 + (u + v) * 0.15) % 1.0
            px = x1 + (x2 - x1) * packet_t
            py = y1 + (y2 - y1) * packet_t
            
            packet_col = (255, 90, 120) if is_cross else (56, 189, 248)
            draw.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=packet_col)
            
        # Draw nodes with multi-layered glow
        for i, (nx, ny) in enumerate(current_pos):
            c = node_clusters[i]
            is_hub = (i in [2, 10, 16])
            
            r = 7.0 if is_hub else 4.0
            
            if is_hub:
                # Highlighted anomaly rings
                glow_r = r + 6.0 + 3.0 * np.sin(phase * 2 + i)
                hub_col = (244, 63, 94) if i == 2 else (6, 182, 212)
                draw.ellipse([nx - glow_r, ny - glow_r, nx + glow_r, ny + glow_r], outline=hub_col, width=1)
                draw.ellipse([nx - r, ny - r, nx + r, ny + r], fill=hub_col)
                # Node id tag
                draw.text((nx + 10, ny - 6), f"ENTITY::{i:02d}", fill=(220, 230, 245), font=font_mono_small)
            else:
                base_c = (200, 70, 90) if c == 0 else ((50, 180, 210) if c == 1 else (140, 160, 180))
                draw.ellipse([nx - r, ny - r, nx + r, ny + r], fill=base_c)
                
        # Header and Editorial Overlay
        draw.text((32, 26), "TRACE-X // INSTITUTIONAL FINANCIAL CRIME OS", fill=(240, 245, 255), font=font_title)
        draw.text((32, 54), "AUTONOMOUS SYNTHETIC RISK GRAPH ENGINE · REACT FLOW + FASTAPI GRAPH CLUSTERING", fill=(120, 140, 165), font=font_mono)
        
        # Real-time Telemetry readouts at top right
        draw.text((w - 260, 26), "SYNTHETIC SYNDICATE: DETECTED", fill=(244, 63, 94), font=font_mono)
        draw.text((w - 260, 42), f"CORRELATION VELOCITY: {1420 + int(np.sin(phase)*180)} TPS", fill=(56, 189, 248), font=font_mono)
        draw.text((w - 260, 58), "SUBGRAPH ANOMALY SCORE: 0.948", fill=(210, 220, 235), font=font_mono)
        
        # Bottom status and metrics
        draw.line([(32, h - 50), (w - 32, h - 50)], fill=(30, 42, 58), width=1)
        draw.text((32, h - 36), "LIVE DEMO → frontend-chi-pied-40.vercel.app", fill=(56, 189, 248), font=font_mono)
        draw.text((w - 240, h - 36), "100+ ENTITIES EVALUATED // REALTIME", fill=(100, 120, 145), font=font_mono)
        
        frames.append(img)
        
    out_file = "assets/tracex_graph_core.webp"
    frames[0].save(out_file, save_all=True, append_images=frames[1:], duration=duration, loop=0, quality=90, method=4)
    print(f"TRACE-X generated: {out_file}, {os.path.getsize(out_file)/1024:.1f} KB")


# ==============================================================================
# 3. SNMS: 3D PARAMETRIC BOTANICAL SPECIMEN (SPATIAL THREE.JS ENGINE)
# ==============================================================================
def generate_snms_spatial():
    print("Generating SNMS 3D Spatial Botanical Mesh...")
    w, h = 880, 400
    n_frames = 36
    fps = 25
    duration = int(1000 / fps)
    
    # 3D Double-Helix / Golden Ratio Botanical Phyllotaxis spiral
    n_points = 64
    spiral_points = []
    for i in range(n_points):
        theta = i * 2.39996 # Golden angle in radians
        rad = 18.0 + math.sqrt(i) * 16.0
        z_coord = (i - n_points/2) * 4.5
        x_coord = rad * math.cos(theta)
        y_coord = rad * math.sin(theta)
        spiral_points.append((x_coord, y_coord, z_coord))
        
    frames = []
    
    for f in range(n_frames):
        phase = 2.0 * np.pi * f / n_frames
        
        img = Image.new("RGB", (w, h), BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        # Isometric / Perspective projection matrix with continuous 360 rotation
        rot_y = phase
        rot_x = 0.45 + 0.15 * math.sin(phase * 0.5)
        
        proj_points = []
        cx, cy = w * 0.55, h * 0.54
        
        for px, py, pz in spiral_points:
            # Rotate around Y
            rx = px * math.cos(rot_y) + pz * math.sin(rot_y)
            ry = py
            rz = -px * math.sin(rot_y) + pz * math.cos(rot_y)
            
            # Rotate around X
            rx2 = rx
            ry2 = ry * math.cos(rot_x) - rz * math.sin(rot_x)
            rz2 = ry * math.sin(rot_x) + rz * math.cos(rot_x)
            
            # Perspective divide
            fov = 360.0
            scale = fov / (fov + rz2)
            sx = cx + rx2 * scale
            sy = cy + ry2 * scale
            proj_points.append((sx, sy, rz2, scale))
            
        # Draw spatial wireframe connections
        for i in range(len(proj_points) - 1):
            x1, y1, z1, s1 = proj_points[i]
            x2, y2, z2, s2 = proj_points[i+1]
            
            # Depth attenuation
            depth_factor = np.clip((z1 + 180.0) / 360.0, 0.15, 1.0)
            col_g = int(50 + 175 * depth_factor)
            col_b = int(70 + 120 * depth_factor)
            col_r = int(20 + 40 * depth_factor)
            
            draw.line([(x1, y1), (x2, y2)], fill=(col_r, col_g, col_b), width=int(1 + 2 * depth_factor))
            
            # Cross lattice connections for structural mesh look
            if i + 5 < len(proj_points):
                x3, y3, z3, s3 = proj_points[i+5]
                draw.line([(x1, y1), (x3, y3)], fill=(25, int(60 * depth_factor), int(70 * depth_factor)), width=1)
                
        # Draw glowing node vertices sorted by depth
        sorted_nodes = sorted(enumerate(proj_points), key=lambda item: item[1][2])
        for idx, (sx, sy, sz, sc) in sorted_nodes:
            depth_factor = np.clip((sz + 180.0) / 360.0, 0.2, 1.0)
            nr = int(3.5 * sc)
            
            # Emerald / botanical fluorescent vertex
            node_r = int(30 * depth_factor)
            node_g = int(240 * depth_factor)
            node_b = int(180 * depth_factor)
            
            draw.ellipse([sx - nr, sy - nr, sx + nr, sy + nr], fill=(node_r, node_g, node_b))
            
        # Draw 3D spatial coordinate gimbal and grid lines in background
        draw.line([(cx - 160, cy + 90), (cx + 160, cy + 90)], fill=(25, 35, 48), width=1)
        draw.line([(cx - 120, cy + 120), (cx + 120, cy + 120)], fill=(20, 28, 38), width=1)
        
        # Left-aligned editorial information
        draw.text((32, 26), "SHIVKUSH HI-TECH NURSERY (SNMS)", fill=(240, 245, 255), font=font_title)
        draw.text((32, 54), "PARAMETRIC HORTICULTURE PLATFORM · THREE.JS 3D ENGINE + SUPABASE RLS", fill=(120, 140, 165), font=font_mono)
        
        # Architectural Spec Readouts on Left Column
        draw.text((32, 110), "SPECIFICATION // GEOMETRY", fill=(52, 211, 153), font=font_mono)
        draw.text((32, 130), "· 3D Interactive Model Viewer", fill=(190, 205, 225), font=font_body)
        draw.text((32, 150), "· High-Density Canopy Architecture", fill=(190, 205, 225), font=font_body)
        draw.text((32, 170), "· Dual-Language PWA (Marathi / English)", fill=(190, 205, 225), font=font_body)
        draw.text((32, 190), "· Automated B2B Wholesale Inventory", fill=(190, 205, 225), font=font_body)
        
        draw.text((32, 235), "DEPLOYMENT ARCHITECTURE", fill=(110, 130, 155), font=font_mono)
        draw.text((32, 255), "· Next.js App Router · TypeScript · Tailwind", fill=(150, 170, 195), font=font_mono)
        draw.text((32, 275), "· Supabase PostgreSQL Row Level Security", fill=(150, 170, 195), font=font_mono)
        
        # Bottom status and metrics
        draw.line([(32, h - 50), (w - 32, h - 50)], fill=(30, 42, 58), width=1)
        draw.text((32, h - 36), "COMMERCIAL PRODUCTION PLATFORM // VERIFIED", fill=(52, 211, 153), font=font_mono)
        draw.text((w - 250, h - 36), f"ROTATION AZIMUTH: {int(math.degrees(phase)):03d}° / 360°", fill=(100, 120, 145), font=font_mono)
        
        frames.append(img)
        
    out_file = "assets/snms_spatial_botanical.webp"
    frames[0].save(out_file, save_all=True, append_images=frames[1:], duration=duration, loop=0, quality=90, method=4)
    print(f"SNMS generated: {out_file}, {os.path.getsize(out_file)/1024:.1f} KB")


# ==============================================================================
# 4. KINETIC TICKER / DATA MATRIX STREAM
# ==============================================================================
def generate_kinetic_stream():
    print("Generating Kinetic Activity Matrix Stream...")
    w, h = 880, 180
    n_frames = 30
    fps = 25
    duration = int(1000 / fps)
    
    # 52 weeks x 7 days heatmap matrix
    np.random.seed(137)
    activity_matrix = np.random.choice([0, 1, 2, 3, 4], size=(7, 48), p=[0.45, 0.25, 0.15, 0.10, 0.05])
    
    color_map = [
        (22, 27, 34),    # empty
        (14, 68, 41),    # low
        (0, 109, 50),    # mid
        (38, 166, 65),   # high
        (57, 211, 83)    # peak
    ]
    
    frames = []
    
    for f in range(n_frames):
        phase = 2.0 * np.pi * f / n_frames
        
        img = Image.new("RGB", (w, h), BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        draw.text((32, 20), "ANNUAL VERIFIED CONTRIBUTION SPECTRUM // 174 COMMITS RECORDED", fill=(210, 225, 245), font=font_mono)
        draw.text((w - 210, 20), "ACTIVITY MATRIX // ACTIVE", fill=(57, 211, 83), font=font_mono)
        
        # Render dynamic heatmap blocks with subtle wave breathing
        start_x = 32
        start_y = 50
        cell_size = 13
        spacing = 4
        
        for row in range(7):
            for col in range(48):
                cx = start_x + col * (cell_size + spacing)
                cy = start_y + row * (cell_size + spacing)
                
                lvl = activity_matrix[row, col]
                base_c = color_map[lvl]
                
                # Dynamic wave pulse traversing the grid
                wave = np.sin(col * 0.25 - phase * 2.0 + row * 0.3)
                if lvl > 0 and wave > 0.6:
                    # illuminate with pulse
                    boost = int(40 * wave)
                    c = (min(255, base_c[0] + boost), min(255, base_c[1] + boost), min(255, base_c[2] + boost))
                else:
                    c = base_c
                    
                draw.rectangle([cx, cy, cx + cell_size, cy + cell_size], fill=c)
                
        frames.append(img)
        
    out_file = "assets/activity_kinetic_stream.webp"
    frames[0].save(out_file, save_all=True, append_images=frames[1:], duration=duration, loop=0, quality=90, method=4)
    print(f"Kinetic stream generated: {out_file}, {os.path.getsize(out_file)/1024:.1f} KB")

if __name__ == "__main__":
    generate_hero()
    generate_tracex_graph()
    generate_snms_spatial()
    generate_kinetic_stream()
    print("ALL ASSETS GENERATED SUCCESSFULLY.")
