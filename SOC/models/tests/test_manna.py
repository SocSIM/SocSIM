from SOC.models import Manna

def test_boundary_shape():
    sim = Manna(10)
    assert sim.values.shape == (12, 12)
    assert sim.L_with_boundary == 12

def test_run():
    sim = Manna(10)
    sim.run(1000)


