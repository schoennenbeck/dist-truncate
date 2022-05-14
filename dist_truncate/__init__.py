from scipy.stats import rv_continuous

from dist_truncate.truncate import truncated

__version__ = "0.0.1"
rv_continuous.truncated = property(truncated)
