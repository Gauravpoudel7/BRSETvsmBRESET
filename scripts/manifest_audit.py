"""Audit of the image manifest and spreadsheets (BRSET diabetic + all mBRSET).
Checks: files listed vs present, exact duplicates (SHA256), near-duplicates (64-bit dHash + 32x32 correlation),
per-patient inconsistencies (age, sex, diabetes duration), per-eye grade disagreements, missing labels.
Writes results_audit/*.csv and a summary to stdout."""
import hashlib, os, numpy as np, pandas as pd
from PIL import Image
from collections import defaultdict
OUT="results_audit"; os.makedirs(OUT,exist_ok=True)
BR=r"C:\data\brset_mbrset\brazilian-ophthalmological\1.0.2"; MB=r"C:\data\brset_mbrset\mbrset\1.0"
b=pd.read_csv(BR+r"\label_brset.csv"); m=pd.read_csv(MB+r"\labels_mbrset.csv")
b["path"]=BR+r"\fundus_photos\\"+b.image_id.astype(str)+".jpg"
m["path"]=MB+r"\images\\"+m.file.astype(str)
b["ds"]="BRSET"; m["ds"]="mBRSET"
b2=b.rename(columns={"exam_eye":"eye"}); b2["eye"]=b2.eye.map({1:"right",2:"left"}).fillna(b2.eye.astype(str))
m2=m.rename(columns={"patient":"patient_id","final_icdr":"DR_ICDR","laterality":"eye","file":"image_id","age":"patient_age","sex":"patient_sex","dm_time":"diabetes_time_y"})
cols=["ds","image_id","patient_id","eye","DR_ICDR","patient_age","patient_sex","diabetes_time_y","path"]
allr=pd.concat([b2[cols],m2[cols]],ignore_index=True)
print("rows",allr.groupby("ds").size().to_dict())
miss=allr[~allr.path.map(os.path.exists)]; print("listed but file missing:",miss.groupby("ds").size().to_dict()); miss.to_csv(OUT+"/missing_files.csv",index=False)
print("missing DR label:",allr[allr.DR_ICDR.isna()].groupby("ds").size().to_dict())
# per patient consistency
for ds,d in allr.groupby("ds"):
    g=d.groupby("patient_id")
    inc={k:int((g[k].nunique(dropna=True)>1).sum()) for k in ["patient_age","patient_sex","diabetes_time_y"]}
    per_eye=d.groupby(["patient_id","eye"]).DR_ICDR.nunique(); 
    print(ds,"patients with >1 value:",inc,"| eyes with different grades on their photos:",int((per_eye>1).sum()),"of",len(per_eye))
    print(ds,"photos per patient:",g.size().value_counts().sort_index().to_dict())
    d[d.set_index(["patient_id","eye"]).index.isin(per_eye[per_eye>1].index)].to_csv(OUT+f"/{ds}_eye_grade_conflicts.csv",index=False)
# hashes: BRSET only diabetic photos + all mBRSET (scan everything present)
use=allr[allr.path.map(os.path.exists)].copy()
def feats(p):
    im=Image.open(p).convert("L")
    a=np.asarray(im.resize((9,8),Image.BILINEAR),dtype=np.float32); dh=(a[:,1:]>a[:,:-1]).flatten()
    s=np.asarray(im.resize((32,32),Image.BILINEAR),dtype=np.float32).flatten(); s=(s-s.mean())/(s.std()+1e-6)
    return dh,s
sha=[];DH=[];SM=[]
for i,p in enumerate(use.path):
    with open(p,"rb") as f: sha.append(hashlib.sha256(f.read()).hexdigest())
    dh,s=feats(p); DH.append(dh); SM.append(s)
    if i%3000==0: print("hashed",i,flush=True)
use["sha"]=sha; DH=np.array(DH); SM=np.array(SM,dtype=np.float32)
ex=use[use.duplicated("sha",keep=False)].sort_values("sha"); print("exact duplicate files:",len(ex)); ex.to_csv(OUT+"/exact_duplicates.csv",index=False)
# near-dups: correlation of 32x32 thumbnails, blockwise
pairs=[]; n=len(use); SMn=SM/np.sqrt((SM**2).sum(1,keepdims=True))
for st in range(0,n,2000):
    C=SMn[st:st+2000]@SMn.T
    I,J=np.where(C>0.985)
    for i,j in zip(I+st,J):
        if j>i:
            ham=int((DH[i]!=DH[j]).sum()); pairs.append((i,j,float(C[i-st,j]),ham))
pr=pd.DataFrame(pairs,columns=["i","j","corr","dhash_dist"])
if len(pr):
    for side in "ij":
        r=use.iloc[pr[side]].reset_index(drop=True)
        for k in ["ds","image_id","patient_id","eye","DR_ICDR"]: pr[f"{k}_{side}"]=r[k].values
    pr["same_patient"]=(pr.ds_i==pr.ds_j)&(pr.patient_id_i==pr.patient_id_j)
    pr["grade_differs"]=pr.DR_ICDR_i!=pr.DR_ICDR_j
pr.to_csv(OUT+"/near_duplicate_pairs.csv",index=False)
print("near-duplicate pairs (corr>0.985):",len(pr))
if len(pr):
    print(" strong (dhash<=8):",int((pr.dhash_dist<=8).sum()))
    s=pr[pr.dhash_dist<=8]
    print(" strong, different patients:",int((~s.same_patient).sum())," of which cross-dataset:",int((s.ds_i!=s.ds_j).sum())," with different grade:",int(s.grade_differs.sum()))
    print(s.groupby(["ds_i","ds_j","same_patient"]).size())
