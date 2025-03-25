import numpy as np
from dagster import (
    get_dagster_logger,
)

logger = get_dagster_logger()

class SegmentationResult:
    """
    A simple class to represent segmentation results.
    """
    def __init__(self, name, source_scan, segmented_data=None):
        """
        Initialize a segmentation result.

        Args:
            name (str): Name/identifier of the segmentation
            source_scan: The source dental scan that was segmented
            segmented_data (ndarray, optional): Pre-computed segmentation mask
        """
        self.name = name
        self.source_scan = source_scan

        # Handle the case where source_scan might not be a DentalScan
        try:
            if hasattr(source_scan, 'data') and isinstance(source_scan.data, np.ndarray):
                source_shape = source_scan.data.shape
                logger.debug(f"Using source scan shape {source_shape} for segmentation")
            else:
                # Fallback if source_scan doesn't have expected data attribute
                logger.warning(f"Source scan doesn't have expected 'data' attribute or is not ndarray")
                source_shape = (100, 100, 100)  # Default shape
        except Exception as e:
            logger.warning(f"Error accessing source scan data: {str(e)}")
            source_shape = (100, 100, 100)  # Default shape

        # Create the segmentation data
        if segmented_data is None:
            try:
                # Try to get shape from source scan
                if hasattr(source_scan, 'data') and isinstance(source_scan.data, np.ndarray):
                    # Simulate segmentation with a boolean mask
                    self.data = np.random.choice(
                        [True, False],
                        size=source_scan.data.shape,
                        p=[0.3, 0.7]  # 30% of voxels are segmented
                    )
                else:
                    # Fallback to default shape
                    self.data = np.random.choice(
                        [True, False],
                        size=source_shape,
                        p=[0.3, 0.7]
                    )
                logger.debug(f"Created segmentation mask with shape {self.data.shape}")
            except Exception as e:
                logger.error(f"Error creating segmentation mask: {str(e)}")
                # Create a small default array as fallback
                self.data = np.random.choice([True, False], size=(10, 10, 10), p=[0.3, 0.7])
        else:
            self.data = segmented_data

    def get_source_name(self):
        """Get the name of the source scan, with error handling"""
        try:
            if hasattr(self.source_scan, 'name'):
                return self.source_scan.name
            return "unknown_source"
        except:
            return "unknown_source"

    def __repr__(self):
        """String representation of the segmentation result"""
        source_name = self.get_source_name()
        return f"SegmentationResult(name='{self.name}', source='{source_name}')"