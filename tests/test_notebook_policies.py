"""Exercise the notebook's actual decision/validation functions without loading models."""
import ast
import json
from pathlib import Path
import re
import unittest

from pydantic import BaseModel, Field
from defence_hardening import defence_decision


ROOT = Path(__file__).resolve().parents[1]
CELLS = json.loads((ROOT / 'Phishing_Email_Triage.ipynb').read_text())['cells']


def source_containing(marker):
    return next(''.join(c['source']) for c in CELLS if marker in ''.join(c['source']))


NAMESPACE = {'json':json, 're':re, 'BaseModel':BaseModel, 'Field':Field,
             'FUSION_MIN_VOTES':5, 'defence_decision':defence_decision}
baseline = source_containing('CUES = {')
exec(baseline[:baseline.index('def cue_names')], NAMESPACE)
definitions = ast.parse(source_containing('def decision_from_score('))
selected = [item for item in definitions.body
            if isinstance(item, (ast.FunctionDef, ast.ClassDef)) and item.name in {
                'decision_from_score', 'Explanation', 'EvidenceExplanation', 'quote_candidates',
                'validate_legacy_explanation', 'validate_explanation', 'explanation_claim_error'}]
exec(compile(ast.Module(body=selected, type_ignores=[]), '<notebook functions>', 'exec'), NAMESPACE)


class DecisionPolicyTests(unittest.TestCase):
    def test_retrieval_override_requires_selected_consensus_and_defence(self):
        decide = NAMESPACE['decision_from_score']
        unanimous = [{'label':'phishing'}] * 5
        mixed = [{'label':'phishing'}] * 4 + [{'label':'safe'}]
        guarded = decide(.1, unanimous, True)
        self.assertEqual(guarded['classifier_verdict'], 'safe')
        self.assertEqual(guarded['verdict'], 'phishing')
        self.assertTrue(guarded['retrieval_override'])
        self.assertEqual(decide(.1, unanimous, False)['verdict'], 'safe')
        self.assertEqual(decide(.1, mixed, True)['verdict'], 'safe')

    def test_retrieval_cannot_downgrade_a_phishing_verdict(self):
        result = NAMESPACE['decision_from_score'](.8, [{'label':'safe'}] * 5, True)
        self.assertEqual(result['verdict'], 'phishing')
        self.assertFalse(result['retrieval_override'])

    def test_either_defensive_view_can_require_review(self):
        decide = NAMESPACE['decision_from_score']
        safe_neighbors = [{'label':'safe'}] * 5
        self.assertEqual(decide(.1, safe_neighbors, True, .1, .9)['verdict'], 'phishing')
        self.assertEqual(decide(.1, safe_neighbors, True, .9, .1)['verdict'], 'phishing')
        self.assertEqual(decide(.1, safe_neighbors, False, .9, .9)['verdict'], 'safe')


class ExplanationValidationTests(unittest.TestCase):
    def setUp(self):
        self.state = {'email':'The meeting agenda is ready for tomorrow.', 'verdict':'safe',
                      'indicators':{'urls':[], 'domains':[], 'cue_groups':[]}}

    def test_selected_quote_is_resolved_from_original_email(self):
        result = NAMESPACE['validate_explanation'](
            '{"reason":"An ordinary meeting agenda.","quote_id":0}', self.state)
        self.assertFalse(result['fallback_used'])
        self.assertIn(result['quote'], self.state['email'])

    def test_invalid_evidence_and_unsupported_claims_are_visible_fallbacks(self):
        for payload in [
            '{"reason":"An agenda.","quote_id":999}',
            '{"reason":"The email contains a link.","quote_id":0}',
            '{"reason":"The domain is flagged.","quote_id":0}',
            '{"reason":"The text proves credential theft.","quote_id":0}',
        ]:
            with self.subTest(payload=payload):
                result = NAMESPACE['validate_explanation'](payload, self.state)
                self.assertTrue(result['fallback_used'])
                self.assertIn('validation_error', result)
                self.assertIn(result['quote'], self.state['email'])


if __name__ == '__main__':
    unittest.main()
