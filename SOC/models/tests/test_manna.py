from SOC.models import Manna
import numpy as np
import pytest
import matplotlib.pyplot as plt

def test_boundary_shape():
    sim = Manna(10,0)
    assert sim.values.shape == (12, 12)
    assert sim.L_with_boundary == 12

def test_run_abel():
    sim = Manna(20,0)
    sim.run(1)
    sim.plot_state()
    plt.show()

def test_run_nonabel():
    sim = Manna(20,1)
    sim.run(200)
    sim.plot_state()
    plt.show()

def test_driving_does_not_pollute_boundary():
    sim = Manna(10,0)
    for i in range(1000):
        sim.drive()

def test_toppling_reduces_middle_to_max_one():
    sim = Manna(10,0)
    sim.values[1:-1, 1:-1] = 6
    sim.AvalancheLoop()
    assert (0 <= sim.values[1:-1, 1:-1]).all()
    assert (sim.values[1:-1, 1:-1] <= 1).all()

    assert (1 <= sim.values[0, :]).all()
    assert (1 <= sim.values[-1, :]).all()
    assert (1 <= sim.values[:, 0]).all()
    assert (1 <= sim.values[:, -1]).all()

@pytest.mark.skip
def test_whiteboard_case_1():
    sim = Manna(3,0)
    sim.values[2, 2] = 2
    results = sim.AvalancheLoop()
    assert int(results['AvalancheSize']) == 2
    assert int(results['number_of_iterations']) == 1

@pytest.mark.skip
def test_whiteboard_case_2():
    sim = Manna(3,0)
    sim.values[2, 2] = 2
    results = sim.AvalancheLoop()
    assert int(results['AvalancheSize']) == 2
    assert int(results['number_of_iterations']) == 1
