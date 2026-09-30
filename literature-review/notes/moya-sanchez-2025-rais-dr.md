# Design and Validation of a Responsible Artificial Intelligence-based System for the Referral of Diabetic Retinopathy Patients (RAIS-DR)

**Citation:** Moya-Sanchez EU, Sanchez-Perez A, Nanclares Da Veiga R, Zarate-Macias A, Villareal E, Sanchez-Montes A, Jauregui-Ulloa E, Moreno H, Cortes U. Design and Validation of a Responsible Artificial Intelligence-based System for the Referral of Diabetic Retinopathy Patients. arXiv:2508.12506; posted 17 August 2025. Venue: arXiv. **Preprint, listed as under review.**
**Year:** 2025
**Dataset(s) used:** Local retinal fundus photograph data, evaluated per patient and per image
**Model(s)/method(s):** RAIS-DR compared against the FDA-approved EyeArt system. Fairness measured with Disparate Impact and Equal Opportunity Difference across sex, image projection type, laterality and age.

## Summary (plain English)
This team built a diabetic retinopathy referral system and treated fairness as a required part of validation rather than an afterthought. Referral means deciding who needs to see a specialist. They compared their system against EyeArt, a commercially approved product, which is a rare and useful benchmark. For fairness they used two standard measures. Disparate Impact compares the rate of positive decisions between groups, where 1 means equal treatment. Equal Opportunity Difference compares how often the system correctly catches disease in each group, where 0 means equal.

## Key finding (plain English)
RAIS-DR beat EyeArt with accuracy up to 19 percentage points higher. On fairness, Disparate Impact stayed between 0.984 and 1.031 and Equal Opportunity Difference stayed close to zero across sex, projection type, laterality and age, indicating little measurable bias.

## Relevance to my research (plain English)
**Partially conflicts with my expectation, and supplies my fairness metrics.** It reports near-equal performance across sex and age, which is a reminder that demographic gaps are not guaranteed and my study could legitimately find none. That is a healthy caution against assuming my hypothesis. The bigger contribution to my work is practical: Disparate Impact and Equal Opportunity Difference are established, interpretable fairness measures with clear reference values, and I can pair them with subgroup AUC. The authors also note that models can predict sex or age from a retinal photo, which is the same shortcut worry raised by the mBRSET papers.
