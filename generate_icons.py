#!/usr/bin/env python
"""
Script pour générer les icônes PWA pour l'application Gestion d'Église CCR.
Génère des icônes SVG et des images PNG si possible.
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire du projet au chemin
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

def create_svg_icon(size=192, filename='icon.svg', with_mask=False):
    """Créer une icône SVG"""
    color = '#5e72e4'
    background = '#ffffff'
    mask_color = '#000000'
    
    # SVG avec un design simple: croix (église)
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
  <!-- Background -->
  <rect width="{size}" height="{size}" fill="{background}"/>
  
  <!-- Background circle -->
  <circle cx="{size//2}" cy="{size//2}" r="{int(size*0.45)}" fill="{color if not with_mask else mask_color}"/>
  
  <!-- Church cross shape -->
  <g fill="white" opacity="1">
    <!-- Vertical bar -->
    <rect x="{int(size*0.4)}" y="{int(size*0.2)}" width="{int(size*0.2)}" height="{int(size*0.6)}" rx="{int(size*0.05)}"/>
    
    <!-- Horizontal bar -->
    <rect x="{int(size*0.25)}" y="{int(size*0.4)}" width="{int(size*0.5)}" height="{int(size*0.2)}" rx="{int(size*0.05)}"/>
    
    <!-- Top triangle (roof) -->
    <polygon points="{size//2},{int(size*0.1)} {int(size*0.3)},{int(size*0.2)} {int(size*0.7)},{int(size*0.2)}"/>
  </g>
</svg>'''
    
    return svg_content

def generate_icons():
    """Générer toutes les icônes nécessaires"""
    icons_dir = PROJECT_DIR / 'eglise' / 'static' / 'icons'
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    # Tailles d'icônes à générer
    sizes = [96, 192, 512]
    
    print(f"Génération des icônes PWA dans {icons_dir}...")
    
    for size in sizes:
        # Icône standard
        svg_content = create_svg_icon(size=size)
        svg_file = icons_dir / f'icon-{size}x{size}.svg'
        with open(svg_file, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✓ Créé: {svg_file.name}")
        
        # Icône maskable (pour différents OS)
        svg_content_mask = create_svg_icon(size=size, with_mask=True)
        svg_file_mask = icons_dir / f'icon-{size}x{size}-maskable.svg'
        with open(svg_file_mask, 'w', encoding='utf-8') as f:
            f.write(svg_content_mask)
        print(f"✓ Créé: {svg_file_mask.name}")
    
    # Essayer de convertir SVG en PNG avec PIL/Pillow si disponible
    try:
        from PIL import Image, ImageDraw
        print("\nPillow détecté - Génération des PNG...")
        
        for size in sizes:
            # Créer une image PNG
            img = Image.new('RGBA', (size, size), (255, 255, 255, 255))
            draw = ImageDraw.Draw(img)
            
            # Cercle de fond bleu
            circle_radius = int(size * 0.45)
            center_x = size // 2
            center_y = size // 2
            draw.ellipse(
                [(center_x - circle_radius, center_y - circle_radius),
                 (center_x + circle_radius, center_y + circle_radius)],
                fill=(94, 114, 228, 255)
            )
            
            # Croix blanche
            bar_width = int(size * 0.2)
            bar_height = int(size * 0.6)
            bar_x = int(size * 0.4)
            bar_y = int(size * 0.2)
            
            # Barre verticale
            draw.rectangle(
                [(bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height)],
                fill=(255, 255, 255, 255)
            )
            
            # Barre horizontale
            bar_h_width = int(size * 0.5)
            bar_h_height = int(size * 0.2)
            bar_h_x = int(size * 0.25)
            bar_h_y = int(size * 0.4)
            
            draw.rectangle(
                [(bar_h_x, bar_h_y), (bar_h_x + bar_h_width, bar_h_y + bar_h_height)],
                fill=(255, 255, 255, 255)
            )
            
            # Sauvegarder l'image
            png_file = icons_dir / f'icon-{size}x{size}.png'
            img.save(png_file, 'PNG')
            print(f"✓ Créé: {png_file.name}")
            
            # Créer une version maskable
            img_mask = Image.new('RGBA', (size, size), (0, 0, 0, 255))
            draw_mask = ImageDraw.Draw(img_mask)
            
            # Croix noire pour maskable
            draw_mask.rectangle(
                [(bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height)],
                fill=(0, 0, 0, 255)
            )
            draw_mask.rectangle(
                [(bar_h_x, bar_h_y), (bar_h_x + bar_h_width, bar_h_y + bar_h_height)],
                fill=(0, 0, 0, 255)
            )
            
            png_file_mask = icons_dir / f'icon-{size}x{size}-maskable.png'
            img_mask.save(png_file_mask, 'PNG')
            print(f"✓ Créé: {png_file_mask.name}")
    
    except ImportError:
        print("\n⚠ Pillow n'est pas installé - Utilisation des icônes SVG uniquement")
        print("  Pour générer des PNG, installez: pip install Pillow")
    
    # Créer des images de capture d'écran placeholder
    screenshots_dir = icons_dir
    screenshot_sizes = [
        (540, 720, 'screenshot-1'),
        (540, 720, 'screenshot-2')
    ]
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        print("\nGénération des screenshots...")
        
        for width, height, name in screenshot_sizes:
            img = Image.new('RGB', (width, height), color=(94, 114, 228))
            draw = ImageDraw.Draw(img)
            
            # Ajouter du texte
            text = f"{name.replace('-', ' ').title()}\nGestion d'Église CCR"
            
            # Centrer le texte
            bbox = draw.textbbox((0, 0), text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            draw.text((x, y), text, fill=(255, 255, 255))
            
            png_file = screenshots_dir / f'{name}.png'
            img.save(png_file, 'PNG')
            print(f"✓ Créé: {png_file.name}")
    
    except ImportError:
        print("\n⚠ Impossible de créer les screenshots (Pillow non installé)")
    
    print("\n✅ Génération des icônes terminée!")
    print(f"📁 Les icônes sont dans: {icons_dir}")

if __name__ == '__main__':
    generate_icons()
