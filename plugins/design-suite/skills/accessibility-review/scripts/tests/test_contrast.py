import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "contrast.py"
spec = importlib.util.spec_from_file_location("contrast", SCRIPT)
contrast = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contrast)


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


class RatioTests(unittest.TestCase):
    def test_black_on_white_is_21(self):
        self.assertEqual(contrast.check("#000", "#fff")["ratio"], 21.0)

    def test_767676_on_white_is_truncated_to_4_54(self):
        result = contrast.check("#767676", "#ffffff")
        self.assertEqual(result["ratio"], 4.54)
        self.assertTrue(result["normal-AA"])

    def test_787774_on_white_fails_normal_aa(self):
        result = contrast.check("#787774", "#ffffff")
        self.assertLess(result["ratio"], 4.5)
        self.assertFalse(result["normal-AA"])

    def test_alpha_is_composited_over_the_background(self):
        # 50% black over white is mid grey #808080 (about 3.95:1 on white).
        half = contrast.ratio("rgba(0, 0, 0, 0.5)", "#ffffff")
        grey = contrast.ratio("#808080", "#ffffff")
        self.assertAlmostEqual(half, grey, delta=0.05)

    def test_translucent_background_is_rejected(self):
        with self.assertRaises(ValueError):
            contrast.ratio("#000", "rgba(255, 255, 255, 0.5)")


class CliTests(unittest.TestCase):
    def test_passing_pair_exits_0(self):
        self.assertEqual(run("#000", "#fff").returncode, 0)

    def test_failing_pair_exits_1(self):
        self.assertEqual(run("#787774", "#ffffff").returncode, 1)

    def test_bad_colour_exits_2(self):
        self.assertEqual(run("not-a-colour", "#fff").returncode, 2)

    def test_odd_number_of_colours_exits_2(self):
        self.assertEqual(run("#000").returncode, 2)


if __name__ == "__main__":
    unittest.main()
