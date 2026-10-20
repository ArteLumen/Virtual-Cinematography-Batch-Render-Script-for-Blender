# 🎬 Virtual Cinematography Batch Render Toolkit

A lightweight Python automation toolkit for **virtual cinematography** workflows in Blender. This tool allows filmmakers, 3D artists, and pipeline developers to automate camera setups, apply cinematic lens properties, and batch render scenes in headless mode (command line).

---

## 📸 Key Features

* **Automated Multi-Camera Rendering:** Detects all cameras in a scene and renders them sequentially.
* **Cinematic Camera Setup:** Applies standardized lens properties (e.g., 35mm focal length, full-frame sensor, $f/2.8$ depth of field).
* **Headless Execution:** Designed to run in background mode (`-b`) without launching Blender’s GUI—saving RAM and GPU resources.
* **Dynamic Directory Management:** Automatically creates output paths for clean asset organization.

---

## 📁 Repository Structure

```text
virtual-cinematography-toolkit/
│
├── scripts/
│   └── batch_render.py       # Main Python automation script
├── scenes/
│   └── sample_scene.blend    # Sample 3D scene (optional)
├── renders/                  # Default output directory for rendered frames
├── .gitignore                # Git ignore rules for heavy/temp files
└── README.md                 # Project documentation
