from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
PRESET_PATH = ROOT / "src" / "preset" / "Maya Operator.json"


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AssertionError(f"Duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _element_values(element):
    yield element
    for child in element.get("element", {}).values():
        yield from _element_values(child)


class MayaOperatorPresetTests(unittest.TestCase):
    def test_inset_faces_uses_the_inset_operator(self):
        with PRESET_PATH.open(encoding="utf-8") as handle:
            preset = json.load(handle, object_pairs_hook=_reject_duplicate_keys)

        inset_faces = [
            element
            for gesture in preset["gesture"].values()
            for root in gesture.get("element", {}).values()
            for element in _element_values(root)
            if element.get("name") == "Inset Faces"
        ]

        self.assertEqual(len(inset_faces), 1)
        self.assertEqual(inset_faces[0].get("operator_bl_idname"), "mesh.inset")


if __name__ == "__main__":
    unittest.main()
