from scipy.stats import rv_continuous

from dist_truncate.truncate import truncated

__version__ = "0.1.0"
rv_continuous.truncated = property(truncated)
