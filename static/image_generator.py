import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Create images/ folder if it doesn't exist
os.makedirs('images', exist_ok=True)

# Define the 15 options with themes (for color/pattern inspiration)
options = [
    # Q1: Art preference
    ("q1_opt1", "Bright, vibrant colors that provide energy", [255, 100, 100], [200, 50, 50]),  # Energetic red-orange
    ("q1_opt2", "Soft, calm tones that are soothing", [150, 200, 255], [100, 150, 200]),      # Soft blue
    ("q1_opt3", "Dark, dramatic contrasts", [50, 50, 50], [150, 0, 0]),                      # Dark gray with red accent
    
    # Q2: Space feeling
    ("q2_opt1", "Energetic and inspiring", [255, 200, 100], [255, 150, 0]),                 # Warm yellow
    ("q2_opt2", "Calm and meditative", [100, 200, 150], [50, 150, 100]),                    # Muted green
    ("q2_opt3", "Sophisticated and dramatic", [80, 40, 120], [120, 60, 180]),               # Deep purple
    
    # Q3: Art style
    ("q3_opt1", "Abstract Expressionism - free and emotional", [255, 100, 150], [200, 50, 100]),  # Pinkish abstract
    ("q3_opt2", "Minimalism - simple and serene", [200, 200, 200], [150, 150, 150]),        # Neutral gray
    ("q3_opt3", "Modern Realism with depth", [100, 80, 60], [150, 120, 90]),                # Earthy brown
    
    # Q4: Mood preference
    ("q4_opt1", "Joyful and uplifting", [255, 255, 100], [255, 200, 0]),                    # Sunny yellow
    ("q4_opt2", "Calm and contemplative", [150, 180, 200], [100, 130, 160]),               # Pale blue-gray
    ("q4_opt3", "Intense and provocative", [100, 20, 20], [200, 50, 50]),                   # Deep crimson
    
    # Q5: Size preference
    ("q5_opt1", "Large accent pieces", [255, 150, 150], [255, 100, 100]),                   # Bold pink
    ("q5_opt2", "Medium works for balance", [180, 180, 100], [140, 140, 60]),               # Balanced olive
    ("q5_opt3", "Small, intimate works", [120, 100, 150], [80, 60, 120])                    # Intimate lavender
]

def generate_image(filename, description, base_color, accent_color):
    fig, ax = plt.subplots(figsize=(0.833, 0.833))  # 60px at 72 DPI ≈ 0.833 inches
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Base gradient background
    gradient = np.linspace(0, 1, 256).reshape(256, -1)
    ax.imshow(gradient, extent=[0, 1, 0, 1], cmap=plt.cm.colors.ListedColormap([
        [base_color[0]/255, base_color[1]/255, base_color[2]/255],
        [accent_color[0]/255, accent_color[1]/255, accent_color[2]/255]
    ]), aspect='auto', origin='lower')
    
    # Subtle pattern (e.g., abstract lines or dots for theme)
    if 'energy' in description.lower() or 'joyful' in description.lower():
        # Dynamic swirls/lines
        theta = np.linspace(0, 2*np.pi, 100)
        r = np.linspace(0.1, 0.3, 100)
        x = 0.5 + r * np.cos(theta)
        y = 0.5 + r * np.sin(theta)
        ax.plot(x, y, color='white', alpha=0.6, linewidth=2)
    elif 'calm' in description.lower() or 'minimal' in description.lower():
        # Soft dots
        for i in range(5):
            ax.scatter(np.random.rand(), np.random.rand(), c='white', s=10, alpha=0.3)
    else:
        # Dramatic lines
        ax.plot([0, 1], [0, 1], color='white', alpha=0.4, linewidth=1)
        ax.plot([1, 0], [0, 1], color='white', alpha=0.4, linewidth=1)
    
    plt.savefig(f'images/{filename}.jpg', bbox_inches='tight', pad_inches=0, dpi=72, facecolor='none')
    plt.close()

# Generate all images
for filename, desc, base, accent in options:
    generate_image(filename, desc, base, accent)
    print(f"Generated: images/{filename}.jpg")

print("All images generated! Place the 'images/' folder next to your HTML file.")