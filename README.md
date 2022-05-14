# dist-truncate
[![PyPI - Version](https://img.shields.io/pypi/v/dist-truncate)](https://pypi.org/project/dist-truncate/)
[![PyPI - License](https://img.shields.io/pypi/l/dist-truncate)](https://github.com/schoennenbeck/dist-truncate/blob/main/LICENSE)
[![Coverage Status](https://coveralls.io/repos/github/schoennenbeck/dist-truncate/badge.svg)](https://coveralls.io/github/schoennenbeck/dist-truncate)

A small python package for truncating (continuous) scipy distributions.

## Installation

### From pypi

To install this package from pypi simply run

```
pip install dist-truncate
```

### From source

To install from source clone this repository and install via pip:

```
git clone https://github.com/schoennenbeck/dist-truncate.git
cd dist-truncate
pip install .
```

## Usage
### Introduction
After installation simply import the package
```
import dist_truncate
```
This adds a property `truncated` to all distributions of type `scipy.stats.rv_continuous`. The property
is itself of type `scipy.stats.rv_continuous` and works the same way as the distribution that was 
started with but with two additional shape-arguments `trunc_min` and `trunc_max` that can be used
to truncated the support of the distribution to the interval `trunc_min <= x <= trunc_max`.

Note that some distributions (e.g. the normal distribution) already have an explicit truncated version 
implemented. In this case the explicit version should be used since it is most likely numerically more
stable than this generic implementation.

### Example

Let us truncate the standard normal distribution to the interval `-0.5 <= x <= 2.0`. As noted above
the truncated normal is already implemented so we can compare the results and make sure that this
generic version actually computes the right outputs.
```
import dist_truncate
from scipy import stats
import numpy as np
```
Comparing the cummulative density functions at multiple points:
```
stats.truncnorm.cdf(np.arange(-3, 3, 0.5), -0.5, 2.0)
# Output: array([0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.28631514, 0.57263027, 0.79676594, 0.93411656,
       1.        , 1.        ])
stats.norm.truncated.cdf(np.arange(-3, 3, 0.5), -0.5, 2.0)
# Output: array([0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.28631514, 0.57263027, 0.79676594, 0.93411656,
       1.        , 1.        ])
```

Comparing the inverse of the cdf:
```
stats.truncnorm.ppf(np.arange(0, 1, 0.2), -0.5, 2.0)
# Output: array([-0.5       , -0.14519108,  0.19172827,  0.55269814,  1.00897798])
stats.norm.truncated.ppf(np.arange(0, 1, 0.2), -0.5, 2.0)
# Output: array([-0.5       , -0.14519108,  0.19172827,  0.55269814,  1.00897798])
```

The minimum and maximum for the truncation can also be called as keyword-arguments:
```
stats.loguniform.truncated.support(1, 100, trunc_max=80, trunc_min=20)
# Output: (20, 80)
```

Broadcasting of shapes works the same as for all other arguments:
```
stats.loguniform.truncated.support([1, 50], [50, 100], trunc_min=20, trunc_max=[[30, 40], [60, 100]])
# Output: (array([[20, 50], [20, 50]]), array([[ 30,  40], [ 50, 100]]))
```