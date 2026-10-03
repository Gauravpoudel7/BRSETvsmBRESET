"""Summarise steep-cohort runs: real vs shuffled, photo + patient level, val (Youden) cut-off, per-grade catch rates."""
import pandas as pd, numpy as np, json
from sklearn.metrics import roc_auc_score, roc_curve
S='data/splits/cohorts/'; R='C:/data/cohort/'
ext=pd.read_csv(S+'ext_mbrset_steep.csv')
def youden(y,p):
    f,t,th=roc_curve(y,p); return th[np.argmax(t-f)]
def pat(df,pcol,gcol):
    g=df.groupby(pcol).agg(prob=('prob','max'),grade=(gcol,'first')); g['y']=(g.grade>0).astype(int); return g
rows=[]; grade_rows=[]; ens=[]
for kind in ['shuf','real']:
    for k in range(5):
        tag=f'{kind}_f{k}'
        te=pd.read_csv(S+f'test_{tag}.csv'); pt=pd.read_csv(R+f'run_{tag}/predictions.csv')
        assert len(te)==len(pt) and (te.patient_id.values==pt.patient_id.values).all(), tag
        te['prob']=pt.prob.values
        pe=pd.read_csv(R+f'run_{tag}/mbrset_external/predictions.csv'); assert len(ext)==len(pe) and (ext.patient.values==pe.patient_id.values).all()
        e=ext.copy(); e['prob']=pe.prob.values
        thr=np.nan
        try:
            v=pd.read_csv(R+f'run_{tag}/val_predictions.csv'); thr=youden(v.label,v.prob)
        except Exception as ex: pass
        tp=pat(te,'patient_id','patient_grade'); ep=pat(e,'patient','patient_grade')
        rows.append(dict(run=tag,kind=kind,fold=k,brset_photo_auc=roc_auc_score(te.DR_ICDR>0,te.prob),brset_pat_auc=roc_auc_score(tp.y,tp.prob),
            mb_photo_auc=roc_auc_score(e.final_icdr>0,e.prob),mb_pat_auc=roc_auc_score(ep.y,ep.prob),thr=thr))
        for ds,p in [('BRSET',tp),('mBRSET',ep)]:
            p=p.copy(); p['flag']=p.prob>=thr; p['run']=tag; p['kind']=kind; p['ds']=ds; grade_rows.append(p.reset_index()[['run','kind','ds','grade','flag']])
        if kind=='real': ens.append(ep.prob.rename(tag))
r=pd.DataFrame(rows); r.to_csv('results_cohort_runs.csv',index=False)
pd.set_option('display.width',200)
print(r.round(3).to_string(index=False))
print('\nMEAN by kind'); print(r.groupby('kind')[['brset_photo_auc','brset_pat_auc','mb_photo_auc','mb_pat_auc']].agg(['mean','min','max']).round(3).T.to_string())
g=pd.concat(grade_rows)
print('\nCatch rate by grade (patient level, val Youden cut-off). BRSET pooled over 5 test folds (each patient once); mBRSET averaged over 5 models.')
t=g.groupby(['kind','ds','grade']).flag.agg(['mean','count']); t['mean']=(t['mean']*100).round(0); print(t.to_string())
# pooled out-of-fold BRSET patient AUROC
for kind in ['shuf','real']:
    pp=[]
    for k in range(5):
        tag=f'{kind}_f{k}'; te=pd.read_csv(S+f'test_{tag}.csv'); te['prob']=pd.read_csv(R+f'run_{tag}/predictions.csv').prob.values; pp.append(pat(te,'patient_id','patient_grade'))
    pp=pd.concat(pp); print(kind,'BRSET pooled OOF patient AUROC (175 pts):',round(roc_auc_score(pp.y,pp.prob),3))
E=pd.concat(ens,axis=1); y=(ext.groupby('patient').patient_grade.first().loc[E.index]>0)
print('mBRSET 5-model ensemble patient AUROC:',round(roc_auc_score(y,E.mean(1)),3))
# per-grade AUROC vs none (patient level, real)
for ds in ['BRSET','mBRSET']: pass
