import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

def create_liquid_chrome_hero():
    w, h = 840, 360
    n_frames = 36
    fps = 25
    duration = int(1000 / fps)
    
    font_large_path = "C:\\Windows\\Fonts\\bahnschrift.ttf"
    font_mono_path = "C:\\Windows\\Fonts\\consola.ttf"
    
    font_large = ImageFont.truetype(font_large_path, 64)
    font_sub = ImageFont.truetype(font_large_path, 14)
    font_mono = ImageFont.truetype(font_mono_path, 11)
    
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2.0, h / 2.0 + 10
    
    # Normalized coords
    nx = (x - cx) / 320.0
    ny = (y - cy) / 160.0
    dist = np.sqrt(nx**2 + ny**2)
    
    frames = []
    bg_color = np.array([13, 17, 23], dtype=np.float32) # GitHub dark #0d1117
    
    for f in range(n_frames):
        phase = 2.0 * np.pi * f / n_frames
        
        # 3D fluid heightmap calculation using harmonic rotating waves
        z = (np.sin(nx * 3.2 + np.cos(phase) * 1.5 + ny * 2.1) *
             np.cos(ny * 2.8 + np.sin(phase) * 1.5 - nx * 1.8))
        
        z += 0.5 * np.sin(nx * 5.0 - phase * 2.0 + ny * 3.5)
        z += 0.3 * np.cos(np.sqrt(nx**2 + ny**2) * 6.0 - phase)
        
        # Elliptical fluid envelope
        mask = np.clip(1.0 - (dist / 1.35)**2, 0.0, 1.0)
        mask = mask**1.5
        z_masked = z * mask
        
        # Compute normals via gradient
        dz_dx = np.gradient(z_masked, axis=1) * 8.0
        dz_dy = np.gradient(z_masked, axis=0) * 8.0
        
        # Normal vector N = (-dz_dx, -dz_dy, 1) normalized
        len_n = np.sqrt(dz_dx**2 + dz_dy**2 + 1.0)
        nx_n = -dz_dx / len_n
        ny_n = -dz_dy / len_n
        nz_n = 1.0 / len_n
        
        # Lighting 1: Key metallic light (moving slightly)
        lx1, ly1, lz1 = np.sin(phase * 0.5) * 0.4 - 0.5, -0.6, 0.8
        l_len = np.sqrt(lx1**2 + ly1**2 + lz1**2)
        lx1, ly1, lz1 = lx1/l_len, ly1/l_len, lz1/l_len
        
        diffuse1 = np.clip(nx_n * lx1 + ny_n * ly1 + nz_n * lz1, 0.0, 1.0)
        
        # Halfway vector for specular
        vx, vy, vz = 0.0, 0.0, 1.0 # viewer
        hx1, hy1, hz1 = (lx1 + vx)/2, (ly1 + vy)/2, (lz1 + vz)/2
        h_len = np.sqrt(hx1**2 + hy1**2 + hz1**2)
        hx1, hy1, hz1 = hx1/h_len, hy1/h_len, hz1/h_len
        
        ndoth = np.clip(nx_n * hx1 + ny_n * hy1 + nz_n * hz1, 0.0, 1.0)
        specular1 = ndoth**32.0 # Sharp chrome glint
        specular_broad = ndoth**8.0
        
        # Iridescent rim / Fresnel
        fresnel = np.clip(1.0 - nz_n, 0.0, 1.0)**2.5
        
        # Color composition: Liquid Obsidian & Chrome with subtle bismuth/iridescent fringe
        # Base chrome tone
        chrome = (diffuse1 * 0.35 + specular_broad * 0.45 + specular1 * 0.9) * mask
        
        # Iridescent chromatic fringe (cyan/violet split based on normal angle)
        angle = np.arctan2(ny_n, nx_n) + phase
        r_fringe = 0.5 + 0.5 * np.cos(angle)
        g_fringe = 0.5 + 0.5 * np.cos(angle + 2.094)
        b_fringe = 0.5 + 0.5 * np.cos(angle + 4.188)
        
        # Fluid RGB
        fr = bg_color[0] + chrome * 220 + fresnel * mask * (r_fringe * 70)
        fg = bg_color[1] + chrome * 225 + fresnel * mask * (g_fringe * 95)
        fb = bg_color[2] + chrome * 240 + fresnel * mask * (b_fringe * 130)
        
        # Ambient obsidian glow in center
        glow = np.exp(-dist * 1.8) * 0.25
        fr += glow * 30
        fg += glow * 45
        fb += glow * 70
        
        img_arr = np.stack([np.clip(fr, 0, 255), np.clip(fg, 0, 255), np.clip(fb, 0, 255)], axis=-1).astype(np.uint8)
        frame_img = Image.fromarray(img_arr, mode='RGB')
        
        # Overlay typographic and editorial design elements onto the frame
        draw = ImageDraw.Draw(frame_img)
        
        # Monumental Name - Optical kerning and placement
        name_text = "YASHVARDHAN"
        bbox = draw.textbbox((0, 0), name_text, font=font_large)
        tw = bbox[2] - bbox[0]
        tx = int((w - tw) / 2)
        ty = int(cy - 48)
        
        # Elegant subtle shadow for typography
        draw.text((tx, ty + 2), name_text, fill=(5, 7, 10, 180), font=font_large)
        # Crisp white with slight metallic transparency
        draw.text((tx, ty), name_text, fill=(245, 248, 252), font=font_large)
        
        # Editorial Subtitle: Spaced uppercase
        sub_text = "CREATIVE TECHNOLOGIST  ×  SOFTWARE ENGINEER"
        bbox_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
        tw_sub = bbox_sub[2] - bbox_sub[0]
        tx_sub = int((w - tw_sub) / 2)
        ty_sub = ty + 76
        
        draw.text((tx_sub, ty_sub), sub_text, fill=(160, 175, 195), font=font_sub)
        
        # Editorial Micro-Metadata at corners
        draw.text((28, 24), "FIGURE 01 // AUTONOMOUS FLUID MANIFOLD", fill=(100, 115, 135), font=font_mono)
        draw.text((w - 240, 24), "19.0760° N, 72.8777° E  [BOM]", fill=(100, 115, 135), font=font_mono)
        
        draw.text((28, h - 34), "REAL-TIME NAVIER-STOKES GLSL LOOP", fill=(80, 95, 115), font=font_mono)
        draw.text((w - 200, h - 34), f"PHASE {int(f * 10):03d} / 360° // 60 FPS", fill=(80, 95, 115), font=font_mono)
        
        # Hairline registration marks
        draw.line([(28, 42), (48, 42)], fill=(45, 55, 70), width=1)
        draw.line([(w - 48, 42), (w - 28, 42)], fill=(45, 55, 70), width=1)
        draw.line([(28, h - 42), (48, h - 42)], fill=(45, 55, 70), width=1)
        draw.line([(w - 48, h - 42), (w - 28, h - 42)], fill=(45, 55, 70), width=1)
        
        frames.append(frame_img)
        
    os.makedirs("assets", exist_ok=True)
    out_path = "assets/hero_liquid_chrome.webp"
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        quality=90,
        method=4
    )
    print(f"Saved {out_path}, size: {os.path.getsize(out_path) / 1024:.1f} KB")

if __name__ == "__main__":
    create_liquid_chrome_hero()
