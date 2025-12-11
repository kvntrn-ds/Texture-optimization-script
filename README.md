# Procedural Scratched Metal – Blender (One-Click)

A tiny, clean Python script that instantly creates a **fully procedural worn & scratched metal** material and applies it to a test object.

✅ No UVs needed  
✅ Works on ANY mesh – sculpted, animated, deformed, kitbash, imported  
✅ Zero setup – just run and go  
✅ Fully customizable in 10 seconds

Instructions:
1. Open Blender → Scripting workspace  
2. Click **New** → paste `scratched_metal.py` (or open the file)  
3. Press **Run Script**

→ Scene clears and Suzanne appears with random scratches.

Want to keep your current scene?  
Comment out the line `wipe_scene()` at the bottom.

### Customize in seconds (top of the file)
```python
BASE_COLOR = (0.85, 0.18, 0.04, 1)   # warm copper → change for gold, chrome, gunmetal…
NOISE_SCALE_RANGE = (8.0, 25.0)      # bigger numbers = finer scratches
COLORRAMP_NARROW = (0.46, 0.50)      # smaller gap = sharper scratches
TEST_OBJECT = "monkey"               # "sphere", "cube", "ico"
