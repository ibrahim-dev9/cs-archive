from PIL import Image, ImageDraw, ImageFont
import os
import platform

def create_og_image():
    # 1. Setup Dimensions and Colors (Tailwind Blue-600)
    width, height = 1200, 630
    bg_color = (37, 99, 235) # #2563eb
    text_color = (255, 255, 255) # White
    
    # 2. Create Image
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # 3. Add Decorative Elements (Subtle Circles)
    # Draw some transparent-ish circles for modern look
    draw.ellipse((-100, -100, 300, 300), fill=(59, 130, 246), outline=None) # Lighter blue
    draw.ellipse((900, 400, 1400, 900), fill=(29, 78, 216), outline=None) # Darker blue
    
    # 4. Load Font
    # Try to find a system font
    font_size_main = 80
    font_size_sub = 40
    font_path = None
    
    system = platform.system()
    try:
        if system == "Windows":
            font_path = "arialbd.ttf" # Arial Bold
        elif system == "Darwin": # macOS
            font_path = "/Library/Fonts/Arial.ttf"
        else: # Linux
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            
        font_main = ImageFont.truetype(font_path, font_size_main)
        font_sub = ImageFont.truetype(font_path, font_size_sub)
    except:
        # Fallback to default if custom font fails
        print("System font not found, using default.")
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # 5. Draw Text
    title = "CS Exams Archive"
    subtitle = "Student Library & Schedule"
    
    # Calculate text position to center it
    # Note: textbbox is available in newer Pillow versions, textsize is deprecated
    try:
        left, top, right, bottom = draw.textbbox((0, 0), title, font=font_main)
        title_w, title_h = right - left, bottom - top
        
        left, top, right, bottom = draw.textbbox((0, 0), subtitle, font=font_sub)
        sub_w, sub_h = right - left, bottom - top
    except AttributeError:
        # Fallback for older Pillow
        title_w, title_h = draw.textsize(title, font=font_main)
        sub_w, sub_h = draw.textsize(subtitle, font=font_sub)

    x_title = (width - title_w) / 2
    y_title = (height - title_h) / 2 - 30
    
    x_sub = (width - sub_w) / 2
    y_sub = y_title + title_h + 20

    draw.text((x_title, y_title), title, font=font_main, fill=text_color)
    draw.text((x_sub, y_sub), subtitle, font=font_sub, fill=(219, 234, 254)) # Light blue text

    # 6. Save
    # Ensure directory exists
    output_dir = "exams/static/images"
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "og_preview.png")
    img.save(output_path)
    print(f"Successfully created OG Image at: {output_path}")

if __name__ == "__main__":
    create_og_image()