"""Contract checks; examples are hand-authored and are not simulation results."""
import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")
ROOT = Path(__file__).resolve().parents[1]


def load(kind, name):
    folder = "schemas" if kind == "schema" else "examples/handoffs"
    suffix = ".schema.json" if kind == "schema" else ".json"
    return json.loads((ROOT / folder / (name + suffix)).read_text())


@pytest.mark.parametrize("name", ["input", "results", "evaluation"])
def test_examples_match_contract(name):
    schema = load("schema", name)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(load("example", name), schema)


@pytest.mark.parametrize("field,value", [("seed", -1), ("duration_months", 0),
                                         ("start_month", 13), ("purpose", "historical")])
def test_invalid_inputs_fail(field, value):
    example = load("example", "input")
    example[field] = value
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(example, load("schema", "input"))


def test_missing_and_unknown_fields_fail():
    for change in ("missing", "unknown"):
        example = load("example", "input")
        if change == "missing":
            del example["seed"]
        else:
            example["disease_shock"] = True
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(example, load("schema", "input"))


def test_revision_limit():
    for name in ("results", "evaluation"):
        example = load("example", name)
        example["revision_round"] = 4
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(example, load("schema", name))


def test_sample_population_accounting():
    result = load("example", "results")
    assert result["run_id"] == result["config"]["run_id"]
    assert result["seed"] == result["config"]["seed"]
    assert len({a["id"] for a in result["final_animals"]}) == 20
    assert sum(a["sex"] == "female" for a in result["final_animals"]) == 10
    for previous, current in zip(result["history"], result["history"][1:]):
        assert current["population"] == previous["population"] + current["births"] - current["deaths"]
        assert current["population"] == current["females"] + current["males"]
