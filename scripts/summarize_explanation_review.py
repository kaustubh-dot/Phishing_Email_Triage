"""Summarize a supplementary explanation assessment; never edits rating sheets.

Scores are subjective judgments recorded with case-specific notes. This paired
comparison is separate from the required rating sheet and is not a blinded study.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/submission/explanation_review'
DIMENSIONS=['correctness','grounding','usefulness']
IMMUTABLE=['email_id','email','dataset_label','verdict','reason','quote','fallback_used']


def fingerprint(row):
    value={key:row[key].replace('\r\n','\n') for key in IMMUTABLE}
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def main():
    def load(path):
        with path.open(newline='',encoding='utf-8') as stream: return list(csv.DictReader(stream))
    paths={'historical':ROOT/'artifacts/human_explanation_ratings.csv',
           'current':ROOT/'artifacts/human_explanation_ratings_9b10d09848942b57.csv'}
    current={row['email_id']:row for row in load(paths['current'])}
    historical={row['email_id']:row for row in load(paths['historical'])}
    entries=json.loads((OUT/'score_entries.json').read_text())
    assert len(entries)==len(current)==30
    assert [entry['case'] for entry in entries]==list(range(1,31))
    assert {entry['email_id'] for entry in entries}==set(current)==set(historical)
    rows=[]
    for item in entries:
        row=current[item['email_id']]
        for version,key in [('historical','old'),('current','new')]:
            source=row if version=='current' else historical[row['email_id']]
            assert fingerprint(source)==item[version+'_snapshot_sha256'], 'An explanation snapshot changed; reassess it before reusing scores.'
            scores=item[key]
            assert len(scores)==3 and all(isinstance(v,int) and 1<=v<=5 for v in scores)
            rows.append({'case':item['case'],'email_id':row['email_id'],'snapshot':version,
                'dataset_label':source['dataset_label'],'verdict':source['verdict'],
                'reason':source['reason'],'quote':source['quote'],
                'fallback_used':source['fallback_used'],
                'review_scope':'supplementary explanation assessment',
                **{f'assessment_{name}_1_to_5':value for name,value in zip(DIMENSIONS,scores)},
                'review_note':item[key+'_comment']})
    path=OUT/'supplementary_explanation_assessment.csv'
    with path.open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    means={snapshot:{dimension:sum(row[f'assessment_{dimension}_1_to_5'] for row in rows if row['snapshot']==snapshot)/30
           for dimension in DIMENSIONS}for snapshot in ['historical','current']}
    comparisons={}
    for j,name in enumerate(DIMENSIONS):
        deltas=[entry['new'][j]-entry['old'][j] for entry in entries]
        comparisons[name]={'mean_difference_current_minus_historical':sum(deltas)/30,
            'current_higher':sum(v>0 for v in deltas),'tied':sum(v==0 for v in deltas),
            'current_lower':sum(v<0 for v in deltas)}
    summary={'review_scope':'supplementary explanation assessment','human_ratings':False,
        'date':'2026-11-11','paired_emails':30,'assessed_explanations':60,
        'blind_review':False,'independent_human_review':False,
        'selection_policy':'Both snapshots and every case are retained. These test-case judgments are not used to retune or select the classifier/security policy.',
        'score_scale':'1 to 5; dimensions reported separately, not combined into an overall mark',
        'means':means,'paired_comparisons':comparisons,
        'source_files_sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths.values()},
        'human_ratings_provided_by_this_assessment':0,
        'limitations':['Single non-blinded assessment; subjective diagnostic scores.',
                      'Two workflow verdicts differ between snapshots; this is not an isolated explainer-method experiment.',
                      'The same 30 saved test cases were inspected; no new generalization or significance claim.',
                      'Historical human means use a different review process and are not directly comparable to these supplementary means.']}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'means':means,'paired_comparisons':comparisons},indent=2))


if __name__=='__main__': main()
