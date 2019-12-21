from SOC.models import OFC
import numpy as np
import pytest

def test_run():
    sim = OFC(1.,0.2, L=20)
    sim.run(5)
