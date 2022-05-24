import numpy as np
from scipy import stats

import dist_truncate


def test_against_truncated_normal():
    cdf_truncnorm = stats.truncnorm.cdf(np.arange(-10, 10, 0.2), -2, 0.5)
    cdf_truncated_normal = stats.norm.truncated.cdf(
        np.arange(-10, 10, 0.2), trunc_min=-2, trunc_max=0.5
    )
    assert np.allclose(cdf_truncnorm, cdf_truncated_normal)

    pdf_truncnorm = stats.truncnorm.pdf(np.arange(-10, 10, 0.2), -2, 0.5)
    pdf_truncated_normal = stats.norm.truncated.pdf(
        np.arange(-10, 10, 0.2), trunc_min=-2, trunc_max=0.5
    )
    assert np.allclose(pdf_truncnorm, pdf_truncated_normal)

    sf_truncnorm = stats.truncnorm.sf(np.arange(-10, 10, 0.2), -2, 0.5)
    sf_truncated_normal = stats.norm.truncated.sf(
        np.arange(-10, 10, 0.2), trunc_min=-2, trunc_max=0.5
    )
    assert np.allclose(sf_truncnorm, sf_truncated_normal)

    ppf_truncnorm = stats.truncnorm.ppf(np.arange(0, 1, 0.02), -2, 0.5)
    ppf_truncated_normal = stats.norm.truncated.ppf(
        np.arange(0, 1, 0.02), trunc_min=-2, trunc_max=0.5
    )
    assert np.allclose(ppf_truncnorm, ppf_truncated_normal)

    stats_truncnorm = stats.truncnorm.stats(-2, 0.5)
    stats_truncated_normal = stats.norm.truncated.stats(trunc_min=-2, trunc_max=0.5)
    assert np.allclose(stats_truncnorm, stats_truncated_normal)


def test_sampling():
    samples = stats.loguniform.truncated.rvs(
        1, 100, trunc_min=5, trunc_max=80, size=1000
    )
    assert all(5 <= x <= 80 for x in samples)


def test_repr():
    assert str(stats.loguniform.truncated).startswith("Truncated")
