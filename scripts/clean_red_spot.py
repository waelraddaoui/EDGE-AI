import os
from PIL import Image
import numpy as np

def remove_spot():
    input_path = r"C:\Users\marie\.gemini\antigravity\brain\1ba22b9c-a45e-477d-93ff-5bd8da06d09f\flawless_iot_breadboard_1790025574777.jpg"
    output_path = r"C:\Users\marie\Desktop\Projets\Stage antigravity\figures\banc_iot_operationnel_final.jpg"
    
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return
        
    img = Image.open(input_path).convert("RGB")
    w, h = img.size
    print(f"Loaded image size: {w}x{h}")
    
    # In flawless_iot_breadboard_1790025574777.jpg (resolution ~ 1280x960):
    # The red artifact is right next to the right edge of the ESP32 board, near the micro-USB connector.
    # Relative coordinates:
    # x is around 0.39 to 0.46 of width
    # y is around 0.46 to 0.52 of height
    arr = np.array(img)
    
    # We find the red spot by detecting high red channel ratio in that region:
    x_min, x_max = int(w * 0.38), int(w * 0.48)
    y_min, y_max = int(h * 0.45), int(h * 0.55)
    
    region = arr[y_min:y_max, x_min:x_max].astype(float)
    # Red dominance: R > 150 and R > G * 1.3 and R > B * 1.3
    r = region[:, :, 0]
    g = region[:, :, 1]
    b = region[:, :, 2]
    
    mask = (r > 130) & (r > g * 1.25) & (r > b * 1.25)
    print(f"Found {np.sum(mask)} red-tinted pixels to clean in region.")
    
    # We can replace the red tint with neutral breadboard color sampled from clean nearby breadboard:
    # A clean patch above this region:
    clean_sample = arr[int(h * 0.38):int(h * 0.44), x_min:x_max]
    
    # Apply interpolation/desaturation to the masked pixels to remove the red light:
    for y_idx in range(y_min, y_max):
        for x_idx in range(x_min, x_max):
            r_val = float(arr[y_idx, x_idx, 0])
            g_val = float(arr[y_idx, x_idx, 1])
            b_val = float(arr[y_idx, x_idx, 2])
            
            # Check if this pixel is contaminated by the red flare
            if r_val > 120 and r_val > g_val * 1.2 and r_val > b_val * 1.2:
                # Neutralize red to match breadboard off-white/grey tone
                avg_gb = (g_val + b_val) / 2.0
                arr[y_idx, x_idx, 0] = int(min(255, avg_gb * 1.05))
                arr[y_idx, x_idx, 1] = int(min(255, avg_gb * 1.02))
                arr[y_idx, x_idx, 2] = int(min(255, avg_gb))
                
    result = Image.fromarray(arr)
    result.save(output_path, quality=95)
    
    # Also save to artifacts directory so it can be previewed
    artifact_copy = r"C:\Users\marie\.gemini\antigravity\brain\1ba22b9c-a45e-477d-93ff-5bd8da06d09f\banc_iot_operationnel_final.jpg"
    result.save(artifact_copy, quality=95)
    print(f"Cleaned image successfully saved to:\n- {output_path}\n- {artifact_copy}")

if __name__ == "__main__":
    remove_spot()
