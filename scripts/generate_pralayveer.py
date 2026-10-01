import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math
import os

BG_COLOR = (13, 17, 23)
FONT_LARGE_PATH = "C:\\Windows\\Fonts\\bahnschrift.ttf"
FONT_MONO_PATH = "C:\\Windows\\Fonts\\consola.ttf"

font_title = ImageFont.truetype(FONT_LARGE_PATH, 22)
font_body = ImageFont.truetype(FONT_LARGE_PATH, 14)
font_mono = ImageFont.truetype(FONT_MONO_PATH, 11)
font_mono_small = ImageFont.truetype(FONT_MONO_PATH, 9)

def generate_pralayveer_radar():
    print("Generating PralayVeer Emergency Crisis Radar...")
    w, h = 880, 360
    n_frames = 36
    fps = 25
    duration = int(1000 / fps)
    
    cx, cy = w * 0.65, h * 0.52
    max_r = 130
    
    # Emergency incident coordinates
    incidents = [
        (cx - 50, cy - 40, "SECTOR ALPHA // EVACUATION ROUTE"),
        (cx + 65, cy - 25, "SECTOR BETA // MEDICAL BEACON"),
        (cx + 20, cy + 55, "SECTOR DELTA // FLOOD LEVEL CRITICAL"),
        (cx - 80, cy + 30, "SECTOR EPSILON // SAFE ZONE 01")
    ]
    
    frames = []
    
    for f in range(n_frames):
        phase = 2.0 * np.pi * f / n_frames
        
        img = Image.new("RGB", (w, h), BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        # Draw concentric radar range rings
        for r_step in [35, 70, 105, 140]:
            draw.ellipse([cx - r_step, cy - r_step, cx + r_step, cy + r_step], outline=(25, 45, 60), width=1)
            
        # Draw crosshairs
        draw.line([(cx - 150, cy), (cx + 150, cy)], fill=(25, 45, 60), width=1)
        draw.line([(cx, cy - 150), (cx, cy + 150)], fill=(25, 45, 60), width=1)
        
        # Rotating sweep beam line with fading trail
        sweep_ang = phase
        sweep_x = cx + max_r * math.cos(sweep_ang)
        sweep_y = cy + max_r * math.sin(sweep_ang)
        draw.line([(cx, cy), (sweep_x, sweep_y)], fill=(251, 146, 60), width=2)
        
        # Trailing sweep fan
        for trail_step in range(1, 12):
            trail_ang = sweep_ang - trail_step * 0.04
            tx = cx + max_r * math.cos(trail_ang)
            ty = cy + max_r * math.sin(trail_ang)
            alpha_col = int(180 * (1.0 - trail_step / 12.0))
            draw.line([(cx, cy), (tx, ty)], fill=(int(alpha_col * 0.9), int(alpha_col * 0.5), int(alpha_col * 0.2)), width=1)
            
        # Draw incident points with pulsing beacons
        for ix, iy, tag in incidents:
            # Check angle difference to sweep
            inc_ang = math.atan2(iy - cy, ix - cx)
            ang_diff = (sweep_ang - inc_ang) % (2 * math.pi)
            
            is_illuminated = (ang_diff < 0.6)
            pt_col = (251, 146, 60) if is_illuminated else (140, 70, 30)
            
            r_pt = 4.0 if not is_illuminated else 6.0
            draw.ellipse([ix - r_pt, iy - r_pt, ix + r_pt, iy + r_pt], fill=pt_col)
            
            if is_illuminated:
                draw.ellipse([ix - 12, iy - 12, ix + 12, iy + 12], outline=(251, 146, 60), width=1)
                draw.text((ix + 12, iy - 6), tag, fill=(254, 215, 170), font=font_mono_small)
                
        # Connect incident vectors (route optimization)
        for i in range(len(incidents) - 1):
            x1, y1, _ = incidents[i]
            x2, y2, _ = incidents[i+1]
            draw.line([(x1, y1), (x2, y2)], fill=(50, 65, 80), width=1)
            
        # Editorial Left Column
        draw.text((32, 26), "PRALAYVEER // SMART CRISIS GUIDANCE OS", fill=(240, 245, 255), font=font_title)
        draw.text((32, 54), "SIH HACKATHON 24-HR SPRINT · REALTIME EMERGENCY ROUTING & TRIAGE", fill=(120, 140, 165), font=font_mono)
        
        draw.text((32, 110), "HACKATHON ARCHITECTURE", fill=(251, 146, 60), font=font_mono)
        draw.text((32, 130), "· 24-Hour Continuous Competitive Sprint", fill=(190, 205, 225), font=font_body)
        draw.text((32, 150), "· Offline-Resilient Geo-Spatial Triangulation", fill=(190, 205, 225), font=font_body)
        draw.text((32, 170), "· Emergency First-Responder Triage Pipeline", fill=(190, 205, 225), font=font_body)
        draw.text((32, 190), "· Automated Threat Vector Mapping", fill=(190, 205, 225), font=font_body)
        
        draw.text((32, 235), "ENGINEERING STACK", fill=(110, 130, 155), font=font_mono)
        draw.text((32, 255), "· Modern JavaScript · GeoJSON · Leaflet Engine", fill=(150, 170, 195), font=font_mono)
        draw.text((32, 275), "· High-Concurrency WebSocket Telemetry", fill=(150, 170, 195), font=font_mono)
        
        draw.line([(32, h - 50), (w - 32, h - 50)], fill=(30, 42, 58), width=1)
        draw.text((32, h - 36), "CRISIS RADAR TELEMETRY // ACTIVE", fill=(251, 146, 60), font=font_mono)
        draw.text((w - 230, h - 36), "SMART INDIA HACKATHON BUILD", fill=(100, 120, 145), font=font_mono)
        
        frames.append(img)
        
    out_file = "assets/pralayveer_crisis_radar.webp"
    frames[0].save(out_file, save_all=True, append_images=frames[1:], duration=duration, loop=0, quality=90, method=4)
    print(f"PralayVeer generated: {out_file}, {os.path.getsize(out_file)/1024:.1f} KB")

if __name__ == "__main__":
    generate_pralayveer_radar()
