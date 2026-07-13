from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_experiment_config import validate  # noqa: E402


def test_bootstrap_config_is_valid() -> None:
    with (ROOT / "configs" / "experiment.bootstrap.yaml").open(
        "r", encoding="utf-8"
    ) as handle:
        config = yaml.safe_load(handle)
    validate(config, ROOT)


def test_future_comments_are_rejected() -> None:
    with (ROOT / "configs" / "experiment.bootstrap.yaml").open(
        "r", encoding="utf-8"
    ) as handle:
        config = yaml.safe_load(handle)
    config["run"]["input_modalities"].append("target_future_comments")
    try:
        validate(config, ROOT)
    except ValueError as error:
        assert "forbidden" in str(error)
    else:
        raise AssertionError("future comments were not rejected")
