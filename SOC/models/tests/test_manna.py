from SOC.models import Manna
import numpy as np
import pytest

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
        sim.drive()

def test_toppling_reduces_middle_to_max_one():
    sim = Manna(10)
    sim.values[1:-1, 1:-1] = 6
    sim.AvalancheLoop()
    assert (0 <= sim.values[1:-1, 1:-1]).all()
    assert (sim.values[1:-1, 1:-1] <= 1).all()

@pytest.mark.skip
def test_whiteboard_case_1():
    sim = Manna(3)
    sim.values[2, 2] = 2
    results = sim.AvalancheLoop()
    assert int(results['AvalancheSize']) == 2
    assert int(results['number_of_iterations']) == 1

@pytest.mark.skip
def test_whiteboard_case_2():
    sim = Manna(3)
    sim.values[2, 2] = 2
    results = sim.AvalancheLoop()
    assert int(results['AvalancheSize']) == 2
    assert int(results['number_of_iterations']) == 1
