"""Execute bundled Python examples against recorded shapes, without network.

This catches nonexistent imports, wrong composite signatures, response-column
mistakes, and incorrect generation denominators in the instructions agents use.
"""
import copy
import json
from pathlib import Path
import re

import pandas as pd
import pytest

import eptr2
import eptr2.composite  # Load real annotations before replacing the client factory.
from eptr2.mapping import get_path_map, get_required_parameters, get_optional_parameters
from eptr2.mapping.processing import get_postprocess_function

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "src/eptr2/assets/skills"
RESPONSES = json.loads((Path(__file__).parent / "fixtures/skill_responses.json").read_text())["responses"]
EXAMPLE_FILES = sorted(p for p in SKILLS.rglob("*.md") if "```python\n" in p.read_text())


class ExampleClient:
    def __init__(self, **kwargs):
        assert kwargs.get("strict_params") is True

    def call(self, key, **kwargs):
        assert key in get_path_map(just_call_keys=True)
        params = set(get_required_parameters(key) + get_optional_parameters(key))
        options = {"postprocess", "request_kwargs", "retry_attempts", "retry_backoff", "retry_backoff_max", "retry_jitter"}
        assert not (kwargs.keys() - params - options), kwargs
        if key == "kgup":
            assert kwargs["region"] == "TR1"
            return pd.DataFrame(copy.deepcopy(RESPONSES["dpp-bulk"]["items"]))
        if key in {"dam-clearing", "idm-log"}:
            # Synthetic market shapes: these examples inspect before aggregating.
            raw = {"items": [{"date": "2026-07-01T00:00:00+03:00", "quantity": 10}]}
        else:
            raw = copy.deepcopy(RESPONSES[key])
        if kwargs.get("postprocess", True):
            return get_postprocess_function(key)(raw, key=key)
        return raw


@pytest.mark.parametrize("path", EXAMPLE_FILES, ids=lambda p: str(p.relative_to(SKILLS)))
def test_skill_python_examples(path, monkeypatch, capsys):
    monkeypatch.setattr(eptr2, "EPTR2", ExampleClient)
    # A missed mock must fail before contacting any endpoint.
    def no_network(*args, **kwargs):
        raise AssertionError("Skill example attempted network access")
    monkeypatch.setattr("urllib3.PoolManager.request", no_network)
    namespace = {}
    for block in re.findall(r"```python\n(.*?)```", path.read_text(), re.S):
        exec(compile(block, str(path), "exec"), namespace)

    if path.parent.name == "eptr2-generation-tracking" and path.name == "examples.md":
        raw = pd.DataFrame(RESPONSES["rt-gen"]["items"])
        output = namespace["df"]
        pd.testing.assert_series_equal(output["total"], raw["total"])
        expected = (raw.wind + raw.sun + raw.river + raw.dammedHydro + raw.geothermal + raw.biomass) / raw.total * 100
        pd.testing.assert_series_equal(output.renewable_share_pct, expected, check_names=False)

    if path.parent.name == "eptr2-imbalance-costs" and path.name == "examples.md":
        assert len(namespace["rows"]) == 2
        assert all(abs(row["positive_difference"]) <= .01 and abs(row["negative_difference"]) <= .01 for row in namespace["rows"])

    if path.parent.name == "eptr2-consumption-data" and path.name == "examples.md":
        assert namespace["df"].consumption_source.eq("settlement").all()
        assert namespace["valid"].all()


def test_skill_references_are_resolvable():
    for path in SKILLS.rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if not target.startswith(("https:", "http:", "#")):
                assert (path.parent / target).is_file(), (path, target)
