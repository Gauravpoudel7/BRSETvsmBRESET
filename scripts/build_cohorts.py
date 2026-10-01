"""Build steep realistic cohorts (Nicholas's plan): no-laser PDR, worst-eye patient grade."""
import pandas as pd, numpy as np, os
from sklearn.model_selection import StratifiedKFold
rng=np.random.RandomState(42)
os.makedirs('data/splits/cohorts',exist_ok=True)
b=pd.read_csv('C:/data/brset_mbrset/brazilian-ophthalmological/1.0.2/label_brset.csv')
m=pd.read_csv('C:/data/brset_mbrset/mbrset/1.0/labels_mbrset.csv')
fl=pd.read_csv('results_audit/prp_flags_firstpass.csv')
laser={ds:set(fl[(fl.dataset==ds)&(fl.laser_flag!='no')].patient.astype(str)) for ds in ['BRSET','mBRSET']}
b=b[b.diabetes=='yes'].copy(); b['patient']=b.patient_id.astype(str); b['grade']=b.DR_ICDR
m=m[m.final_icdr.notna()].copy(); m['patient']=m.patient.astype(str); m['grade']=m.final_icdr.astype(int)
def pick(df,ds,want):
    pg=df.groupby('patient').grade.max()
    pg=pg[~pg.index.isin(laser[ds])]   # drops grade-4 patients with any likely/possible laser photo
    out=[]
    for g,n in enumerate(want):
        pool=pg[pg==g].index.values; assert len(pool)>=n,(ds,g,len(pool),n)
        out+= [(p,g) for p in rng.choice(pool,n,replace=False)]
    return pd.DataFrame(out,columns=['patient','patient_grade']), pg.value_counts().sort_index()
bc,bpool=pick(b,'BRSET',[94,52,20,7,2])
skf=StratifiedKFold(5,shuffle=True,random_state=42)
# PDR has only 2 -> stratify on grade with 3+4 merged
strat=bc.patient_grade.clip(upper=3)
bc['fold']=-1
for k,(_,te) in enumerate(skf.split(bc,strat)): bc.loc[bc.index[te],'fold']=k
mc,mpool=pick(m,'mBRSET',[174,96,37,13,4])
bc.to_csv('data/splits/cohorts/brset_steep175_patients.csv',index=False)
mc.to_csv('data/splits/cohorts/mbrset_steep324_patients.csv',index=False)
bi=b[b.patient.isin(bc.patient)].merge(bc,on='patient'); mi=m[m.patient.isin(mc.patient)].merge(mc,on='patient')
bi[['image_id','patient','grade','patient_grade','fold']].to_csv('data/splits/cohorts/brset_steep175_images.csv',index=False)
mi[['file','patient','grade','patient_grade']].to_csv('data/splits/cohorts/mbrset_steep324_images.csv',index=False)
print('BRSET pool after laser removal',bpool.to_dict()); print('mBRSET pool',mpool.to_dict())
print('BRSET cohort',bc.patient_grade.value_counts().sort_index().to_dict(),'photos',len(bi))
print(pd.crosstab(bc.fold,bc.patient_grade))
print('mBRSET cohort',mc.patient_grade.value_counts().sort_index().to_dict(),'photos',len(mi))
