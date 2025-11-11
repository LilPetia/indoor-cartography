import json, os

rgb_dir = "C:/Users/Admin/Documents/ZEDCodes/data/rgb"
depth_dir = "C:/Users/Admin/Documents/ZEDCodes/data/depth"

frames = []
rgb_files = sorted([f for f in os.listdir(rgb_dir) if f.endswith(".png")])
depth_files = sorted([f for f in os.listdir(depth_dir) if f.endswith(".png")])

for rgb, depth in zip(rgb_files, depth_files):
    frames.append({
        "file_path": f"rgb/{rgb}",
        "depth_path": f"depth/{depth}",
        "transform_matrix": [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    })

data = {
    "camera_angle_x": 1.771,
    "h": 720,
    "w": 1280,
    "fl_x": 522.9744262695312,
    "fl_y": 522.9744262695312,
    "cx": 652.0046997070312,
    "cy": 352.111572265625,
    "frames": frames
}

with open("C:/Users/Admin/Documents/ZEDCodes/data/transforms_full.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Saved {len(frames)} frames to transforms_full.json")
