import unittest
from rubric_lab.schema import Criterion
from rubric_lab.scoring import score_criterion, score_rubric

class TestScoring(unittest.TestCase):
    def test_deterministic_scoring(self):
        c1 = Criterion(name="a", weight=0.6, max_points=10.0)
        c2 = Criterion(name="b", weight=0.4, max_points=10.0)
        res1 = score_rubric([c1, c2], {"a": 8.0, "b": 6.0})
        res2 = score_rubric([c1, c2], {"a": 8.0, "b": 6.0})
        self.assertEqual(res1.total_score, res2.total_score)
        self.assertEqual(res1.normalized_score, res2.normalized_score)

    def test_boundary_weights(self):
        c_zero = Criterion(name="z", weight=0.0, max_points=10.0)
        res_z = score_criterion(c_zero, 10.0, 10.0)
        self.assertEqual(res_z.weighted_score, 0.0)
        c_one = Criterion(name="o", weight=1.0, max_points=10.0)
        res_o = score_criterion(c_one, 10.0, 10.0)
        self.assertEqual(res_o.weighted_score, 10.0)

    def test_malformed_inputs(self):
        with self.assertRaises(ValueError):
            Criterion(name="", weight=0.5, max_points=10.0)
        with self.assertRaises(ValueError):
            Criterion(name="neg", weight=-0.5, max_points=10.0)

    def test_missing_fields(self):
        c1 = Criterion(name="x", weight=0.5, max_points=10.0)
        c2 = Criterion(name="y", weight=0.5, max_points=10.0)
        res = score_rubric([c1, c2], {"x": 5.0})
        self.assertIn("y", res.missing_fields)

    def test_edge_cases(self):
        c = Criterion(name="e", weight=1.0, max_points=10.0)
        res = score_criterion(c, 15.0, 10.0)
        self.assertEqual(res.clamped_score, 10.0)
        with self.assertRaises(ValueError):
            score_criterion(c, -1.0, 10.0)

if __name__ == "__main__":
    unittest.main()
