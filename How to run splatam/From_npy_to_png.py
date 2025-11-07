import numpy as np
import imageio
import os

depth_dir = "C:/Users/Admin/Documents/ZEDCodes/data/depth_old"
out_dir = "C:/Users/Admin/Documents/ZEDCodes/data/depth_png"
os.makedirs(out_dir, exist_ok=True)

for f in os.listdir(depth_dir):
    if f.endswith(".npy"):
        arr = np.load(os.path.join(depth_dir, f))
        arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
        # если глубина в метрах, переводим в миллиметры
        arr_mm = (arr * 1000).astype(np.uint16)
        out_path = os.path.join(out_dir, f.replace(".npy", ".png"))
        imageio.imwrite(out_path, arr_mm)

print("✅ Converted depth to millimeter scale (uint16 PNG)")

