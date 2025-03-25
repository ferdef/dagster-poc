import time
import numpy as np
from dagster import (
    asset,
    AssetIn,
    AssetExecutionContext,
    MetadataValue,
    get_dagster_logger
)
from .constants import IOS_SEGMENTATION_TIME, GROUP_SEGMENTATION
from .safe_data import safe_float
from .dental_scan import DentalScan
from .segmentation_result import SegmentationResult
from .ios_scan import ios_scan_data

logger = get_dagster_logger()

@asset(
    ins={
        "ios_data": AssetIn(key=ios_scan_data.key)
    },
    group_name=GROUP_SEGMENTATION,
    metadata={
        "processing_time": f"{IOS_SEGMENTATION_TIME}s",
        "description": "Segments teeth and other structures from IOS scan",
    }
)
def ios_segmentation(context: AssetExecutionContext, ios_data):
    """
    Perform segmentation on IOS scan data.

    Args:
        context: The Dagster execution context
        ios_data: The IOS scan data to process, expected to be a DentalScan object

    Returns:
        SegmentationResult: The segmentation result for the IOS scan
    """
    try:
        # Detailed logging for debugging
        logger.info(f"Starting IOS segmentation...")
        logger.info(f"Received ios_data of type: {type(ios_data)}")

        # Input validation
        if not isinstance(ios_data, DentalScan):
            logger.warning(f"Expected DentalScan object, but got {type(ios_data)}. Attempting to continue...")

        # More robust handling - extract name regardless of input type
        scan_name = getattr(ios_data, 'name', 'unknown_scan')
        logger.info(f"Segmenting IOS data from {scan_name}...")

        # Simulate processing time
        time.sleep(IOS_SEGMENTATION_TIME)

        # Create a simulated segmentation result with enhanced error handling
        try:
            result = SegmentationResult("ios_teeth_segmentation", ios_data)

            # Calculate percentage of segmented voxels - with error handling
            try:
                segmented_percent = np.mean(result.data) * 100
                # Convert numpy.float64 to standard Python float
                segmented_percent = safe_float(segmented_percent)
            except Exception as e:
                logger.error(f"Error calculating segmentation percentage: {str(e)}")
                segmented_percent = 30.0  # Default fallback value

            # Add output metadata
            context.add_output_metadata({
                "segmented_percentage": MetadataValue.float(segmented_percent),
                "source_scan": scan_name
            })

            logger.info(f"IOS segmentation completed successfully")
            return result

        except Exception as e:
            logger.error(f"Error during SegmentationResult creation: {str(e)}")
            raise

    except Exception as e:
        logger.error(f"Unexpected error in ios_segmentation: {str(e)}")
        # Re-raise to ensure Dagster knows this step failed
        raise