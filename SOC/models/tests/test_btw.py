from SOC.models import BTW
import numpy as np
import pytest

def test_boundary_shape():
    sim = BTW(10)
    assert sim.values.shape == (12, 12)
    assert sim.L_with_boundary == 12

def test_run():
    sim = BTW(10)
    sim.run(1000)