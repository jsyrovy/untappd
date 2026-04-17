import json

from untappd_pairing import overrides


def test_load_returns_empty_when_file_missing(tmp_path):
    assert overrides.load(tmp_path / "missing.json") == {}


def test_load_parses_key_to_url_mapping(tmp_path):
    path = tmp_path / "overrides.json"
    path.write_text(
        json.dumps(
            {
                "ambasada::Maisel, Bayreuth, Bavorsko::Maisels Weisse": (
                    "https://untappd.com/b/brauerei-gebr-maisel-maisel-s-weisse-original/35642"
                ),
            },
        ),
    )
    result = overrides.load(path)
    assert result["ambasada::Maisel, Bayreuth, Bavorsko::Maisels Weisse"].endswith("/35642")


def test_load_recovers_from_corrupt_file(tmp_path, caplog):
    path = tmp_path / "overrides.json"
    path.write_text("not json")
    with caplog.at_level("ERROR"):
        assert overrides.load(path) == {}


def test_load_rejects_non_object_payload(tmp_path, caplog):
    path = tmp_path / "overrides.json"
    path.write_text(json.dumps(["a", "b"]))
    with caplog.at_level("ERROR"):
        assert overrides.load(path) == {}
