import numpy as np
from dagster import (
    get_dagster_logger,
)

logger = get_dagster_logger()

def safe_float(value):
    """
    Safely convert a value (including numpy types) to a Python float.

    Args:
        value: Any value that can be converted to float

    Returns:
        float: The value as a standard Python float
    """
    try:
        # Convert numpy types to standard Python types
        if hasattr(value, 'item'):  # numpy scalars have .item() method
            return float(value.item())
        return float(value)
    except (TypeError, ValueError):
        logger.warning(f"Could not convert {value} of type {type(value)} to float, using 0.0")
        return 0.0

def safe_dict(data):
    """
    Recursively convert a dictionary that might contain numpy values to use only Python standard types.

    Args:
        data: Dictionary possibly containing numpy values

    Returns:
        dict: Dictionary with only standard Python types
    """
    result = {}
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = safe_dict(value)
        elif isinstance(value, (list, tuple)):
            result[key] = [safe_float(x) if isinstance(x, (int, float, np.number)) else x for x in value]
        elif isinstance(value, np.number):
            result[key] = safe_float(value)
        elif isinstance(value, np.ndarray):
            if value.size == 1:
                result[key] = safe_float(value.item())
            else:
                result[key] = value.tolist()  # Convert arrays to lists
        else:
            result[key] = value
    return result