"""Steep cohort + extra clean BRSET pool. Per fold k: test=cohort fold k; val=cohort fold k+1 + 15% of pool;
train=other 3 cohort folds + 85% of pool. Pool = diabetic BRSET patients not in cohort, laser-flagged excluded.
'shuf' permutes photo labels in train+val only."""
import pandas as pd, numpy as np, yaml
from pathlib import Path
from sklearn.model_selection import train_test_split
S=Path('data/splits/cohortpool'); S.mkdir(parents=True,exist_ok=True); C=Path('configs/cohortpool'); C.mkdir(parents=True,exist_ok=True)
b=pd.read_csv('C:/data/brset_mbrset/brazilian-ophthalmological/1.0.2/label_brset.csv')
fl=pd.read_csv('results_audit/prp_flags_firstpass.csv')
laser=set(fl[(fl.dataset=='BRSET')&(fl.laser_flag!='no')].patient.astype(int))
bc=pd.read_csv('data/splits/cohorts/brset_steep175_patients.csv'); bc['patient']=bc.patient.astype(int)
b=b[b.diabetes=='yes'].copy()
pg=b.groupby('patient_id').DR_ICDR.max()
pool=pg[~pg.index.isin(laser)&~pg.index.isin(bc.patient)]
print('pool patients',len(pool),pool.value_counts().sort_index().to_dict(),'photos',b.patient_id.isin(pool.index).sum())
coh=b[b.patient_id.isin(bc.patient)].merge(bc.rename(columns={'patient':'patient_id'}),on='patient_id')
base=yaml.safe_load(open('configs/cohort/cohort_real_f0.yaml'))
rows=[]
for k in range(5):
    v=(k+1)%5
    pv_ids,pt_ids=None,None
    pt_ids,pv_ids=train_test_split(pool.index.values,test_size=0.15,stratify=pool.clip(upper=2).values,random_state=300+k)
    te=coh[coh.fold==k]
    va=pd.concat([coh[coh.fold==v], b[b.patient_id.isin(pv_ids)]])
    tr=pd.concat([coh[~coh.fold.isin([k,v])], b[b.patient_id.isin(pt_ids)]])
    assert not set(tr.patient_id)&set(va.patient_id) and not set(tr.patient_id)&set(te.patient_id) and not set(va.patient_id)&set(te.patient_id)
    for kind in ['real','shuf']:
        rng=np.random.RandomState(500+k); trk,vak=tr.copy(),va.copy()
        if kind=='shuf':
            trk['DR_ICDR']=rng.permutation(trk.DR_ICDR.values); vak['DR_ICDR']=rng.permutation(vak.DR_ICDR.values)
        tag=f'{kind}_f{k}'
        for n,d in [('train',trk),('val',vak),('test',te)]: d.to_csv(S/f'{n}_{tag}.csv',index=False)
        cfg=yaml.safe_load(yaml.safe_dump(base)); cfg['seed']=3000+k
        d=cfg['data']; d['splits_dir']=str(S).replace('\\','/')
        for n in ['train','val','test']: d[f'{n}_csv']=f'{S.as_posix()}/{n}_{tag}.csv'
        d['external_test_csv']='data/splits/cohorts/ext_mbrset_steep.csv'
        cfg['output']['dir']=f'C:/data/cohortpool/run_{tag}'
        cfg['train']['save_last_checkpoint']=False
        yaml.safe_dump(cfg,open(C/f'cp_{tag}.yaml','w'),sort_keys=False)
    vpg=va.groupby('patient_id').DR_ICDR.max(); tpg=tr.groupby('patient_id').DR_ICDR.max()
    print(k,'train pts',len(tpg),tpg.value_counts().sort_index().to_dict(),'photos',len(tr),'| val pts',len(vpg),vpg.value_counts().sort_index().to_dict(),'photos',len(va),'| test pts',te.patient_id.nunique(),'photos',len(te))
