"""Make split CSVs + configs for the steep-cohort 5-fold runs (real labels and shuffled-label baseline)."""
import pandas as pd, numpy as np, yaml, os
from pathlib import Path
R=Path('.'); S=R/'data/splits/cohorts'; C=R/'configs/cohort'; C.mkdir(parents=True,exist_ok=True)
b=pd.read_csv('C:/data/brset_mbrset/brazilian-ophthalmological/1.0.2/label_brset.csv')
m=pd.read_csv('C:/data/brset_mbrset/mbrset/1.0/labels_mbrset.csv')
bc=pd.read_csv(S/'brset_steep175_patients.csv'); mc=pd.read_csv(S/'mbrset_steep324_patients.csv')
bc['patient']=bc.patient.astype(int); mc['patient']=mc.patient.astype(int)
bb=b[b.patient_id.isin(bc.patient)&(b.diabetes=='yes')].merge(bc.rename(columns={'patient':'patient_id'}),on='patient_id')
mm=m[m.patient.isin(mc.patient)&m.final_icdr.notna()].merge(mc,on='patient')
mm.to_csv(S/'ext_mbrset_steep.csv',index=False)
base=yaml.safe_load(open('configs/mccv/mccv_r01.yaml'))
for k in range(5):
    v=(k+1)%5
    te=bb[bb.fold==k]; va=bb[bb.fold==v]; tr=bb[~bb.fold.isin([k,v])]
    for kind in ['real','shuf']:
        rng=np.random.RandomState(100+k)
        trk,vak=tr.copy(),va.copy()
        if kind=='shuf':
            trk['DR_ICDR']=rng.permutation(trk.DR_ICDR.values); vak['DR_ICDR']=rng.permutation(vak.DR_ICDR.values)
        tag=f'{kind}_f{k}'
        trk.to_csv(S/f'train_{tag}.csv',index=False); vak.to_csv(S/f'val_{tag}.csv',index=False); te.to_csv(S/f'test_{tag}.csv',index=False)
        cfg=yaml.safe_load(yaml.safe_dump(base)); cfg['seed']=2000+k
        d=cfg['data']; d['splits_dir']='data/splits/cohorts'
        d['train_csv']=f'data/splits/cohorts/train_{tag}.csv'; d['val_csv']=f'data/splits/cohorts/val_{tag}.csv'; d['test_csv']=f'data/splits/cohorts/test_{tag}.csv'
        d['external_test_csv']='data/splits/cohorts/ext_mbrset_steep.csv'
        cfg['output']['dir']=f'C:/data/cohort/run_{tag}'
        yaml.safe_dump(cfg,open(C/f'cohort_{tag}.yaml','w'),sort_keys=False)
    print(k,'train',len(tr),tr.patient_id.nunique(),'pos',(tr.DR_ICDR>0).sum(),'| val',len(va),'pos',(va.DR_ICDR>0).sum(),'| test',len(te),te.patient_id.nunique())
print('external photos',len(mm),'patients',mm.patient.nunique())
