import pytest
import warnings
from sklearn.exceptions import UndefinedMetricWarning

# Filter out specific warnings
warnings.filterwarnings('ignore', category=UndefinedMetricWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment before each test."""
    # Add any test environment setup here
    pass 