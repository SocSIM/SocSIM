from SOC.models import Manna
from SOC.models.manna import Toppling
import numpy as np

def test_boundary_shape():
    sim = Manna(10)
    assert sim.values.shape == (12, 12)
    assert sim.L_with_boundary == 12

def test_run():
    sim = Manna(10)
    sim.run(1000)

def test_driving_does_not_pollute_boundary():
    sim = Manna(10)
    for i in range(1000):
        sim.Driving()

def test_toppling_reduces_middle_to_max_one():
    sim = Manna(10)
    sim.values[1:-1, 1:-1] = 6
    sim.AvalancheLoop()
    assert (0 <= sim.values[1:-1, 1:-1]).all()
    assert (sim.values[1:-1, 1:-1] <= 1).all()

    assert (1 <= sim.values[0, :]).all()
    assert (1 <= sim.values[-1, :]).all()
    assert (1 <= sim.values[:, 0]).all()
    assert (1 <= sim.values[:, -1]).all()


