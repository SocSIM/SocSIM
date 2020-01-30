from SOC.models import BTW
import numpy as np
import pytest

def test_boundary_shape():
    sim = BTW(10)
    assert sim.values.shape == (12, 12)
    assert sim.L_with_boundary == 12

def test_run():
    sim = BTW(10)
    sim.run(10)

def test_deterministic_result():
    b = BTW(5, save_every = 1)

    b.values[...] = 3
    b.values[3, 3] += 1

    b.topple_dissipate()
    output = [[3, 4, 4, 4, 4, 4, 3],
              [4, 1, 3, 3, 3, 1, 4],
              [4, 3, 1, 3, 1, 3, 4],
              [4, 3, 3, 0, 3, 3, 4],
              [4, 3, 1, 3, 1, 3, 4],
              [4, 1, 3, 3, 3, 1, 4],
              [3, 4, 4, 4, 4, 4, 3],]
    np.testing.assert_allclose(b.values, output)

