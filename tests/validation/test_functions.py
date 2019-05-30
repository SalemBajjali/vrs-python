import os

import pytest
import yaml

from ga4gh.vr import ga4gh_digest


validation_fn = os.path.join(os.path.dirname(__file__), "data", "functions.yaml")
validation_tests = yaml.load(open(validation_fn), Loader=yaml.SafeLoader)


@pytest.mark.parametrize("test", validation_tests["ga4gh_digest"])
def test_digest(test):
    assert test["out"]["digest"] == ga4gh_digest(blob=test["in"]["blob"].encode())
