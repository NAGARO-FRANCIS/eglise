from PIL import Image, ImageDraw, ImageFilter
import os

# Create icons directory if not exists
icon_dir_static = r'c:\projet\CCR\eglise\static\icons'
icon_dir_static_files = r'c:\projet\CCR\staticfiles\icons'

# Colors
PRIMARY_COLOR = '#5e72e4'  # Bleu
SECONDARY_COLOR = '#825ee4'  # Violet
WHITE = '#FFFFFF'
ACCENT = '#2dce89'  # Vert

def create_church_icon(size, output_path):
    """Create a church icon with better contrast for mobile"""
    
    # Create image with white background
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate proportions
    margin = size * 0.1
    
    # Draw gradient background (simulate with circle)
    # Create a new image for gradient
    gradient_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient_img)
    
    # Draw blue/purple gradient circle
    for i in range(size // 2, 0, -1):
        # Calculate color for this ring
        ratio = 1 - (i / (size // 2))
        r = int(94 + (130 - 94) * ratio)  # 5e -> 82
        g = int(114 + (94 - 114) * ratio)  # 72 -> 5e
        b = int(228 + (228 - 228) * ratio)  # e4 -> e4
        
        gradient_draw.ellipse(
            [size//2 - i, size//2 - i, size//2 + i, size//2 + i],
            fill=(r, g, b, 255)
        )
    
    img = Image.alpha_composite(img, gradient_img)
    draw = ImageDraw.Draw(img)
    
    # Draw white church building
    building_left = size * 0.25
    building_top = size * 0.45
    building_right = size * 0.75
    building_bottom = size * 0.85
    
    # Main building
    draw.rectangle(
        [building_left, building_top, building_right, building_bottom],
        fill=WHITE,
        outline=WHITE,
        width=2
    )
    
    # Roof (triangle)
    roof_peak = size * 0.3
    draw.polygon(
        [
            (size * 0.5, roof_peak),  # top
            (building_left, building_top),  # bottom left
            (building_right, building_top)  # bottom right
        ],
        fill=WHITE,
        outline=WHITE
    )
    
    # Door
    door_width = size * 0.1
    door_height = size * 0.2
    door_x = size * 0.45
    door_y = size * 0.6
    draw.rectangle(
        [door_x, door_y, door_x + door_width, door_y + door_height],
        fill=(94, 114, 228, 255),  # Dark blue
    )
    
    # Door knob
    knob_size = size * 0.02
    draw.ellipse(
        [door_x + door_width - knob_size * 2, door_y + door_height * 0.4,
         door_x + door_width - knob_size, door_y + door_height * 0.4 + knob_size],
        fill=WHITE
    )
    
    # Cross on top
    cross_width = size * 0.08
    cross_height = size * 0.15
    cross_center_x = size * 0.5
    cross_center_y = roof_peak * 0.7
    
    # Vertical bar
    draw.rectangle(
        [cross_center_x - cross_width * 0.25, cross_center_y - cross_height * 0.5,
         cross_center_x + cross_width * 0.25, cross_center_y + cross_height * 0.5],
        fill=WHITE
    )
    
    # Horizontal bar
    draw.rectangle(
        [cross_center_x - cross_width * 0.5, cross_center_y - cross_width * 0.25,
         cross_center_x + cross_width * 0.5, cross_center_y + cross_width * 0.25],
        fill=WHITE
    )
    
    # Save
    img.save(output_path, 'PNG')
    print(f"✅ Created: {output_path}")

# Generate all sizes
sizes = [96, 192, 512]

for size in sizes:
    # Create static version
    output_static = os.path.join(icon_dir_static, f'icon-{size}x{size}.png')
    create_church_icon(size, output_static)
    
    # Create staticfiles version
    output_staticfiles = os.path.join(icon_dir_static_files, f'icon-{size}x{size}.png')
    create_church_icon(size, output_staticfiles)

print("\n✅ Toutes les icônes ont été générées avec succès !")
