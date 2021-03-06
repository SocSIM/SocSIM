from SOC.models import Manna
import numpy as np
import pytest

def test_boundary_shape():
    sim = Manna(L=10)
    assert sim.values.shape == (12, 12)
    assert sim.L_with_boundary == 12

def test_run_abel():
    sim = Manna(L=20)
    sim.run(5)

def test_run_nonabel():
    sim = Manna(L=20, abelian = False)
    sim.run(5)

def test_driving_does_not_pollute_boundary():
    sim = Manna(L=10)
    for i in range(1000):
        sim.drive()

def test_toppling_reduces_middle_to_max_one():
    sim = Manna(L=10)
    sim.values[1:-1, 1:-1] = 6
    sim.AvalancheLoop()
    assert (0 <= sim.values[1:-1, 1:-1]).all()
    assert (sim.values[1:-1, 1:-1] <= 1).all()

@pytest.mark.skip
def test_whiteboard_case_1():
    sim = Manna(L=3)
    sim.values[2, 2] = 2
    results = sim.AvalancheLoop()
    assert int(results['AvalancheSize']) == 2
    assert int(results['number_of_iterations']) == 1

@pytest.mark.skip
def test_whiteboard_case_2():
    sim = Manna(L=3)
    sim.values[2, 2] = 2
    results = sim.AvalancheLoop()
    assert int(results['AvalancheSize']) == 2
    assert int(results['number_of_iterations']) == 1

def test_resurrect():
    sim = Manna(L=10)
    filename = "test_ressurrect.zarr"
    sim.run(5, filename=filename)
    saved = sim.saved_snapshots[-1].copy()
    save_every_orig = sim.save_every

    sim2 = Manna.from_file(filename)
    np.testing.assert_allclose(sim2.values, saved)
    assert sim2.save_every == save_every_orig

def test_resurrect_default_name():
    sim = Manna(L=10)
    filename = sim.run(50, filename=False)
    saved = sim.saved_snapshots[-1].copy()
    save_every_orig = sim.save_every

    sim2 = Manna.from_file(filename)
    np.testing.assert_allclose(sim2.values, saved)
    assert sim2.save_every == save_every_orig
