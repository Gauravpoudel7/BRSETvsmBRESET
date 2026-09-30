# Improving Consistency in Cardiovascular Disease Risk Assessment: Cross-Camera Adaptation for Retinal Images

**Citation:** Zhang W, Shi D, He M. Improving Consistency in Cardiovascular Disease Risk Assessment: Cross-Camera Adaptation for Retinal Images. In: 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW). IEEE; 2024:5194-5199. doi: 10.1109/cvprw63382.2024.00527. Venue: CVPR Workshops. **Peer reviewed conference workshop paper.**
**Year:** 2024
**Dataset(s) used:** Retinal image datasets captured with both conventional and portable cameras
**Model(s)/method(s):** Cross-camera domain adaptation with an ordinal risk classification approach and a "risk consistency loss" added to an image translation model

## Summary (plain English)
This paper is about predicting heart disease risk from eye photos rather than eye disease itself, but the camera problem is the same. The team wanted a model to give the same risk answer whether the picture came from a big clinic camera or a portable one. They translated images between camera styles, and added an extra training rule that punishes the model when the translated image produces a different risk score than the original. They also treated risk as ordered levels, low to high, rather than unrelated categories.

## Key finding (plain English)
Forcing the model to give consistent risk scores across camera types improves agreement between conventional and portable camera images.

## Relevance to my research (plain English)
**Supports my gap from a different angle.** It shows the camera problem is not specific to diabetic retinopathy, it affects anything predicted from a retina photo. Its most transferable idea for me is "consistency" as a metric: instead of only asking whether accuracy dropped, I could ask whether the same patient-like image gets the same risk score across devices. Since BRSET and mBRSET contain different patients, I cannot do that directly, but it is a useful framing for a future study where our company photographs the same eye on both devices.
