from SOC.models import OFC
import numpy as np
import pytest

def test_run():
    sim = OFC(20,1.,0.2)
    sim.run(5)
