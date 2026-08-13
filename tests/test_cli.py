"""Offline tests for the eptr2 CLI (no credentials needed)."""

import json

import pytest

from eptr2 import cli


def run(capsys, *argv):
    code = cli.main(list(argv))
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def test_no_command_prints_help(capsys):
    code, out, _ = run(capsys, )
    assert code == 2
    assert "usage: eptr2" in out


def test_list_table(capsys):
    code, out, _ = run(capsys, "list")
    assert code == 0
    assert "mcp" in out
    assert "Total:" in out


def test_list_json_has_all_calls(capsys):
    code, out, _ = run(capsys, "list", "--format", "json")
    assert code == 0
    calls = json.loads(out)
    assert len(calls) >= 231
    assert "mcp" in calls


def test_list_unknown_category(capsys):
    code, out, err = run(capsys, "list", "--category", "NOPE")
    assert code == 1
    assert out == ""
    assert "No category" in err


def test_categories(capsys):
    code, out, _ = run(capsys, "categories", "--format", "json")
    assert code == 0
    cats = json.loads(out)
    assert "GÖP" in cats


def test_search(capsys):
    code, out, _ = run(capsys, "search", "imbalance", "--format", "json")
    assert code == 0
    assert "imb" in out


def test_search_no_match(capsys):
    code, _, err = run(capsys, "search", "zzz-no-such-thing")
    assert code == 1
    assert "No endpoints" in err


def test_describe_text(capsys):
    code, out, _ = run(capsys, "describe", "mcp")
    assert code == 0
    assert "Market Clearing Price" in out
    assert "start_date" in out
    assert "eptr2 call mcp" in out


def test_describe_json_alias(capsys):
    code, out, _ = run(capsys, "describe", "ptf", "--format", "json")
    assert code == 0
    d = json.loads(out)
    assert d["key"] == "mcp"
    assert d["alias_of"]["alias"] == "ptf"


def test_describe_unknown(capsys):
    code, _, err = run(capsys, "describe", "nope-nope")
    assert code == 1
    assert "Unknown call key" in err


def test_schema_stdout(capsys):
    code, out, _ = run(capsys, "schema", "--stdout")
    assert code == 0
    s = json.loads(out)
    assert s["endpoint_count"] == len(s["endpoints"])


def test_schema_check_passes_on_synced_repo(capsys, monkeypatch):
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(repo_root)
    code, _, err = run(capsys, "schema", "--check")
    assert code == 0, err
    assert "up to date" in err


def test_schema_output_file(capsys, tmp_path):
    target = tmp_path / "schema.json"
    code, _, err = run(capsys, "schema", "--output", str(target))
    assert code == 0
    assert json.loads(target.read_text(encoding="utf-8"))["endpoints"]


def test_install_skills_list(capsys):
    code, out, _ = run(capsys, "install-skills", "--list")
    assert code == 0
    assert "eptr2-api-discovery" in out.splitlines()


def test_install_skills_to_path(capsys, tmp_path):
    code, _, err = run(capsys, "install-skills", "--dest", str(tmp_path))
    assert code == 0
    assert "Installed 7 skill(s)" in err
    assert (tmp_path / "eptr2-price-analysis" / "SKILL.md").exists()


def test_mcp_config_generic_and_vscode(capsys):
    code, out, _ = run(capsys, "mcp-config")
    assert code == 0
    config = json.loads(out)
    assert config["mcpServers"]["eptr2"]["command"] == "eptr2-mcp-server"
    assert "EPTR_USERNAME" in config["mcpServers"]["eptr2"]["env"]

    code, out, _ = run(capsys, "mcp-config", "--client", "vscode")
    assert code == 0
    config = json.loads(out)
    assert config["servers"]["eptr2"]["type"] == "stdio"


def test_version(capsys):
    import eptr2

    code, out, _ = run(capsys, "version")
    assert code == 0
    assert out.strip() == eptr2.__version__


class FakeEPTR2:
    last_call = None

    def __init__(self, **kwargs):
        FakeEPTR2.last_init = kwargs

    def call(self, key, **params):
        FakeEPTR2.last_call = (key, params)
        return [
            {"date": "2025-01-01T00:00:00+03:00", "price": 100.5},
            {"date": "2025-01-01T01:00:00+03:00", "price": 99.0},
        ]


@pytest.fixture
def fake_client(monkeypatch):
    import eptr2 as eptr2_pkg

    monkeypatch.setattr(eptr2_pkg, "EPTR2", FakeEPTR2)
    return FakeEPTR2


def test_call_json(capsys, fake_client):
    code, out, _ = run(
        capsys, "call", "mcp", "--start-date", "2025-01-01", "--end-date", "2025-01-01"
    )
    assert code == 0
    records = json.loads(out)
    assert len(records) == 2
    assert fake_client.last_call == (
        "mcp",
        {"start_date": "2025-01-01", "end_date": "2025-01-01"},
    )


def test_call_csv_and_params(capsys, fake_client):
    code, out, _ = run(
        capsys, "call", "mcp", "-p", "org_id=123", "--format", "csv"
    )
    assert code == 0
    lines = out.strip().splitlines()
    assert lines[0] == "date,price"
    assert len(lines) == 3
    assert fake_client.last_call == ("mcp", {"org_id": "123"})


def test_call_bad_param(capsys, fake_client):
    code, _, err = run(capsys, "call", "mcp", "-p", "not-a-pair")
    assert code == 2
    assert "key=value" in err


def test_call_output_file(capsys, fake_client, tmp_path):
    target = tmp_path / "out.json"
    code, out, err = run(capsys, "call", "mcp", "--output", str(target))
    assert code == 0
    assert out == ""
    assert str(target) in err
    assert len(json.loads(target.read_text(encoding="utf-8"))) == 2


def test_plugin_path(capsys):
    from pathlib import Path

    code, out, _ = run(capsys, "plugin-path")
    assert code == 0
    root = Path(out.strip())
    assert (root / "plugin.json").is_file()


def test_install_plugin_cli(capsys, tmp_path):
    dest = tmp_path / "plugin"
    code, _, err = run(capsys, "install-plugin", "--dest", str(dest))
    assert code == 0
    assert (dest / "plugin.json").is_file()

    code, _, err = run(capsys, "install-plugin", "--dest", str(dest))
    assert code == 1
    assert "already exists" in err

    code, _, _ = run(capsys, "install-plugin", "--dest", str(dest), "--force")
    assert code == 0
