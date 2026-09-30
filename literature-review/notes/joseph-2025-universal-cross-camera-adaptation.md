# Enhancing AI-based diabetic retinopathy diagnosis through universal cross-camera image adaptation

**Citation:** Joseph S, Chen X, Liu C, Zhu Z, Ramasamy K, Ravilla TD, Ge Z, He M. Enhancing AI-based diabetic retinopathy diagnosis through universal cross-camera image adaptation. BMJ Open Ophthalmology. 2025;10(1):e002238. doi: 10.1136/bmjophth-2025-002238. Venue: BMJ Open Ophthalmology. **Peer reviewed.**
**Year:** 2025
**Dataset(s) used:** Fundus images from multiple camera types, including the portable Optain camera
**Model(s)/method(s):** A style alignment model for cross-camera image adaptation, applied before an existing diabetic retinopathy AI system

## Summary (plain English)
Different eye cameras produce pictures that look different in colour, brightness and sharpness. That difference alone can confuse an AI model. This team built a step that runs before the AI and repaints incoming pictures into one consistent house style. They call it "universal" because, unlike older methods, it does not need example images from the original camera and does not need retraining for each new camera. They tested it with a portable camera called Optain.

## Key finding (plain English)
Standardising image style before the AI sees the picture reduces the accuracy loss caused by switching cameras. This lets a portable camera be plugged into an existing screening programme without rebuilding the AI.

## Relevance to my research (plain English)
**Supports my gap and points at the fix.** It confirms that camera differences on their own are a recognised, measurable problem in diabetic retinopathy AI, which is the premise of my study. For the product decision at my company it is one of the most useful papers here, because it suggests a middle path: instead of retraining a whole model on our own device data, we might only need a lightweight image-normalising step in front of it. I should treat "does simple preprocessing close the gap" as a comparison arm in my own design.
