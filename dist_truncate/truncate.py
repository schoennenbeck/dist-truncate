from typing import Tuple, Union

import numpy as np
from scipy.stats import rv_continuous

DistArg = Union[np.float64, np.ndarray, float, int]


def truncated(dist: rv_continuous) -> rv_continuous:
    class _Truncated(rv_continuous):
        def _pdf(self, x: DistArg, *args) -> DistArg:
            *args, min_value, max_value = args
            args = map(np.asarray, args)
            scale = 1 / (dist.cdf(max_value, *args) - dist.cdf(min_value, *args))
            in_intervall = (x >= min_value) & (x <= max_value)
            return dist.pdf(x, *args) * scale * in_intervall

        def _cdf(self, x: DistArg, *args) -> DistArg:
            *args, min_value, max_value = args
            scale = 1 / (dist.cdf(max_value, *args) - dist.cdf(min_value, *args))
            cdf_min = dist.cdf(min_value, *args)
            # For value in the intervall we simply have to rescale and reposition the known cdf
            res = scale * (dist.cdf(x, *args) - cdf_min)
            # For value below the min we set the value to 0
            res = res * (x >= min_value)
            # For values above the max we set the value to 1
            res = np.minimum(res, 1)
            return res

        def _sf(self, x: DistArg, *args) -> DistArg:
            *args, min_value, max_value = args
            scale = 1 / (dist.cdf(max_value, *args) - dist.cdf(min_value, *args))
            sf_max = dist.sf(max_value, *args)
            res = scale * (dist.sf(x, *args) - sf_max)
            res = res * (x <= max_value)
            res = np.minimum(res, 1)
            return res

        def _ppf(self, q: DistArg, *args) -> DistArg:
            *args, min_value, max_value = args
            scale = 1 / (dist.cdf(max_value, *args) - dist.cdf(min_value, *args))
            cdf_min = dist.cdf(min_value, *args)
            return dist.ppf(q / scale + cdf_min, *args)

        def _get_support(self, *args) -> Tuple[DistArg, DistArg]:
            *args, min_value, max_value = args
            args = map(np.asarray, args)
            dist_min, dist_max = dist.support(*args)
            return (np.maximum(dist_min, min_value), np.minimum(dist_max, max_value))

        def _argcheck(self, *args) -> Union[bool, np.ndarray]:
            *args, min_value, max_value = args
            return dist._argcheck(*args) & (max_value > min_value)

        def __repr__(self) -> str:
            return f"Truncated {dist.name} distribution"

    shapes = ", ".join([dist.shapes, "min_value", "max_value"])
    return _Truncated(
        name=f"truncated_{dist.name}",
        shapes=shapes,
        a=dist.a,
        b=dist.b,
        badvalue=dist.badvalue,
        xtol=dist.xtol,
        momtype=dist.moment_type,
    )
