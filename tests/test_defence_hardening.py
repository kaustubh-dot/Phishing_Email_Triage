"""Security invariants and label preservation, without loading model weights."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import pandas as pd
import defence_hardening as defence
from mcp_indicator_server import extract_urls, check_domain_lookalike


def indicators(text):
    urls=extract_urls(text)
    return {'urls':urls,'domains':[check_domain_lookalike(url) for url in urls]}


class IndicatorReviewTests(unittest.TestCase):
    def test_explicit_secret_requests_and_security_disabling_require_review(self):
        for text in [
            'Enter your password and backup codes at https://account-reset.example/check.',
            'Pay at https://parcel.example/pay. The page requires your banking password.',
            'Disable antivirus and install https://repair.example/fix.exe.',
        ]:
            with self.subTest(text=text):
                self.assertTrue(defence.indicator_review_reasons(text,indicators(text)))

    def test_negated_security_reminders_are_not_secret_requests(self):
        for text in [
            'Never enter your password at https://account-reset.example/check.',
            'Our team will never ask you to provide your password at https://help.example/.',
            'Do not disable antivirus or install https://unknown.example/fix.exe.',
            'The meeting agenda is at https://project.example/agenda.',
        ]:
            with self.subTest(text=text):
                self.assertEqual(defence.indicator_review_reasons(text,indicators(text)),[])

    def test_deceptive_userinfo_does_not_get_exact_brand_exception(self):
        text='Enter your password at https://paypal.com@evil.example/login.'
        self.assertTrue(defence.indicator_review_reasons(text,indicators(text)))


class AugmentationTests(unittest.TestCase):
    def test_true_labels_are_preserved_and_requested_labels_are_independent(self):
        class Tokenizer:
            def encode(self,text,**kwargs): return text.split()
        frame=pd.DataFrame([{'text':f'Original email {i} with ordinary content.',
                             'label':i%2,'email_id':f'id{i}'} for i in range(6)])
        context={'tokenizer':Tokenizer(),'shorten_email':lambda text:text}
        with patch.dict(defence.DEFENCE_SETTINGS,{'clean_plain_examples':4,'adversarial_examples':8}):
            rows=defence.defence_training_records(frame,context)
        original=frame.set_index('email_id').label.to_dict()
        self.assertTrue(all(row['label']==original[row['source_id']] for row in rows))
        attacks=[row for row in rows if row['kind']=='adversarial']
        for label in [0,1]:
            for requested in [0,1]:
                self.assertEqual(sum(row['label']==label and row['requested_label']==requested
                                     for row in attacks),2)

    def test_frozen_holdout_uses_disjoint_email_identities_and_payloads(self):
        root=Path(__file__).resolve().parents[1]
        dev=json.loads((root/'artifacts/security/development_specs.json').read_text())
        held=json.loads((root/'artifacts/security/heldout_specs.json').read_text())
        train_ids=set(pd.read_csv(root/'artifacts/results/full/split_manifest.csv').query("split=='train'").email_id)
        dev_ids={r['control_id']for r in dev['cases']}
        held_ids={r['control_id']for r in held['cases']}
        self.assertTrue(dev_ids.isdisjoint(held_ids))
        self.assertTrue(train_ids.isdisjoint(dev_ids|held_ids))
        self.assertTrue({r['payload']for r in dev['cases']}.isdisjoint(r['payload']for r in held['cases']))
        self.assertFalse(held['selection_allowed'])


if __name__=='__main__':
    unittest.main()
