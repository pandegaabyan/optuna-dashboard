import sys
from unittest.mock import patch

import numpy as np
import pytest
import torch


if sys.version_info >= (3, 8):
    from optuna_dashboard.preferential.samplers.gp import _one_side_trunc_norm_sampling
    from optuna_dashboard.preferential.samplers.gp import _orthants_MVN_Gibbs_sampling
else:
    pytest.skip("BoTorch dropped Python3.7 support", allow_module_level=True)


def test_orthants_MVN_Gibbs_sampling() -> None:
    cov_inv = torch.Tensor([[0.1, 0.3], [0.4, 0.2]])
    initial_sample = torch.Tensor([0.5, 0.6])
    ret = _orthants_MVN_Gibbs_sampling(cov_inv, 2, initial_sample)
    assert ret.shape == (3, 2)


def test_one_side_trunc_norm_sampling() -> None:
    for lower in np.linspace(-10, 10, 100):
        assert _one_side_trunc_norm_sampling(torch.Tensor([lower])) >= lower

    with patch.object(torch, "rand", return_value=torch.Tensor([0.4])):
        assert np.allclose(
            _one_side_trunc_norm_sampling(torch.Tensor([0.1])).numpy(), 0.899967154837563
        )
    with patch.object(torch, "rand", return_value=torch.Tensor([0.8])):
        assert np.allclose(
            _one_side_trunc_norm_sampling(torch.Tensor([-2.3])).numpy(), -0.8113606739551955
        )
    with patch.object(torch, "rand", return_value=torch.Tensor([0.1])):
        assert np.allclose(
            _one_side_trunc_norm_sampling(torch.Tensor([5])).numpy(), 5.426934003050024
        )
