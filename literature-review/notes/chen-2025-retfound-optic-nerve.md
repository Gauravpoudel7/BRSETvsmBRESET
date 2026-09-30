# Independent Evaluation of RETFound Foundation Model's Performance on Optic Nerve Analysis Using Fundus Photography

**Citation:** Chen MS, Ravindranath R, Chang R, Zhou Y, Keane PA, Wang SY. Independent Evaluation of RETFound Foundation Model's Performance on Optic Nerve Analysis Using Fundus Photography. Ophthalmology Science. 2025;5(3):100720. doi: 10.1016/j.xops.2025.100720. Venue: Ophthalmology Science. **Peer reviewed.**
**Year:** 2025
**Dataset(s) used:** An independent clinical dataset of fundus photographs with matched optic nerve measurements
**Model(s)/method(s):** RETFound used as a feature extractor, then models trained to predict cup-to-disc ratio and retinal nerve fibre layer thickness overall, by quadrant and by clock hour

## Summary (plain English)
This study reused RETFound for jobs it was not originally built to do. Instead of classifying a disease, they asked it to estimate physical measurements of the optic nerve, which is the cable carrying signals from eye to brain. Cup-to-disc ratio and nerve fibre layer thickness are numbers that eye doctors track to watch for glaucoma. Using RETFound as a "feature extractor" means keeping it frozen and letting it turn each photo into a set of numbers, then training a small model on those numbers. The point was to see if a limited local dataset is enough when you start from RETFound.

## Key finding (plain English)
RETFound's learned features supported reasonable prediction of optic nerve measurements even from a small dataset, showing it transfers to tasks it was never trained for.

## Relevance to my research (plain English)
**Supports my gap through its stated limitation.** The finding itself is about a different task, but the authors' own caveat is the part I need. They note that most of their fundus images came from a single machine, which may limit how well the model generalises to other devices, and they warn this could produce biased or less accurate predictions on images from different imaging systems. That is an independent group flagging the device problem as unresolved and calling for validation across a wide variety of machines. It is a clean citation for why my study needs doing.
