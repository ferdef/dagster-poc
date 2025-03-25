import numpy as np
from dagster import (
    get_dagster_logger
)

logger = get_dagster_logger()

class DentalScan:
    """
    A simple class to simulate dental scan data.
    """
    def __init__(self, name, scan_type, dimensions=(100, 100, 100)):
        """
        Initialize a dental scan with simulated data.

        Args:
            name (str): The name/identifier of the scan
            scan_type (str): The type of scan (e.g., "IOS", "CBCT")
            dimensions (tuple): 3D dimensions of the scan data
        """
        self.name = name
        self.scan_type = scan_type
        self.dimensions = dimensions

        # Ensure dimensions is a tuple of 3 integers
        if not (isinstance(dimensions, tuple) and len(dimensions) == 3):
            raise ValueError(f"Dimensions must be a tuple of 3 integers, got {dimensions}")

        # Simulate voxel data with a random array
        try:
            self.data = np.random.rand(*dimensions)
            logger.debug(f"Created random data array with shape {self.data.shape}")
        except Exception as e:
            logger.error(f"Error creating random data array: {str(e)}")
            # Create a small default array as fallback
            self.data = np.random.rand(10, 10, 10)

    def __repr__(self):
        """String representation of the dental scan"""
        return f"DentalScan(name='{self.name}', type='{self.scan_type}', dims={self.dimensions})"