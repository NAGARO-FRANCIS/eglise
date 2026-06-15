from PIL import Image, ImageDraw

icon_dir_static = r'c:\projet\CCR\eglise\static\icons'
icon_dir_static_files = r'c:\projet\CCR\staticfiles\icons'

def create_church_maskable_icon(size, output_path):
    """Create a maskable church icon (Android style) - solid design"""
    
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Use solid blue/purple for maskable icons
    PRIMARY_COLOR = (94, 114, 228, 255)  # #5e72e4
    
    # Calculate proportions with safe area (for maskable icons)
    margin = size * 0.15  # Safe area margin
    
    # Draw white church building
    building_left = size * 0.3
    building_top = size * 0.45
    building_right = size * 0.7
    building_bottom = size * 0.85
    
    # Main building
    draw.rectangle(
        [building_left, building_top, building_right, building_bottom],
        fill=PRIMARY_COLOR,
    )
    
    # Roof (triangle)
    roof_peak = size * 0.3
    draw.polygon(
        [
            (size * 0.5, roof_peak),  # top
            (building_left, building_top),  # bottom left
            (building_right, building_top)  # bottom right
        ],
        fill=PRIMARY_COLOR,
    )
    
    # Door (lighter)
    door_width = size * 0.12
    door_height = size * 0.22
    door_x = size * 0.44
    door_y = size * 0.58
    draw.rectangle(
        [door_x, door_y, door_x + door_width, door_y + door_height],
        fill=(255, 255, 255, 200),  # Semi-transparent white
    )
    
    # Cross on top (white)
    cross_width = size * 0.08
    cross_height = size * 0.15
    cross_center_x = size * 0.5
    cross_center_y = roof_peak * 0.7
    
    # Vertical bar
    draw.rectangle(
        [cross_center_x - cross_width * 0.25, cross_center_y - cross_height * 0.5,
         cross_center_x + cross_width * 0.25, cross_center_y + cross_height * 0.5],
        fill=(255, 255, 255, 255)
    )
    
    # Horizontal bar
    draw.rectangle(
        [cross_center_x - cross_width * 0.5, cross_center_y - cross_width * 0.25,
         cross_center_x + cross_width * 0.5, cross_center_y + cross_width * 0.25],
        fill=(255, 255, 255, 255)
    )
    
    # Save
    img.save(output_path, 'PNG')
    print(f"✅ Created maskable: {output_path}")

# Generate maskable versions
for size in [192, 512]:
    output_static = rf'c:\projet\CCR\eglise\static\icons\icon-{size}x{size}-maskable.png'
    create_church_maskable_icon(size, output_static)
    
    output_staticfiles = rf'c:\projet\CCR\staticfiles\icons\icon-{size}x{size}-maskable.png'
    create_church_maskable_icon(size, output_staticfiles)

print("\n✅ Icônes maskable générées avec succès !")
