import time
import numpy as np
from dagster import (
    asset,
    AssetExecutionContext,
    MetadataValue,
    get_dagster_logger
)

from ..constants import IOS_LOAD_TIME, GROUP_INPUT
from ..safe_data import safe_float
from ..dental_scan import DentalScan

logger = get_dagster_logger()

@asset(
    group_name=GROUP_INPUT,
    metadata={
        "file_type": "IOS STL",
        "description": "Intraoral scanner data in STL format",
    }
)
def ios_scan_data(context: AssetExecutionContext):
    """
    Load IOS (Intraoral Scanner) data from file system.

    Returns:
        DentalScan: Object containing simulated IOS scan data
    """
    try:
        logger.info("Loading IOS scan data...")

        # Simulate loading time
        time.sleep(IOS_LOAD_TIME)

        # Create a simulated scan object with explicit dimensions
        dimensions = (200, 200, 100)
        logger.info(f"Creating DentalScan with dimensions {dimensions}")

        scan = DentalScan(
            name="patient_ios_scan",
            scan_type="IOS",
            dimensions=dimensions
        )

        # Verify the scan was created correctly
        logger.info(f"Successfully created DentalScan: {scan}")

        # Check that the data attribute exists and has the right shape
        if hasattr(scan, 'data') and isinstance(scan.data, np.ndarray):
            logger.info(f"Scan data shape: {scan.data.shape}")
        else:
            logger.warning("Scan data not properly initialized!")

        # Log some information about the loaded data
        try:
            file_size_mb = scan.data.nbytes / 1024 / 1024
            # Convert to standard Python float
            file_size_mb = safe_float(file_size_mb)

            # Use tuples instead of numpy arrays for dimensions
            dimensions = tuple(map(int, scan.dimensions))

            context.add_output_metadata({
                "dimensions": MetadataValue.json(dimensions),
                "file_size_mb": MetadataValue.float(file_size_mb),
                "scan_type": "IOS"
            })
        except Exception as e:
            logger.error(f"Error adding metadata: {str(e)}")

        logger.info("IOS scan data loaded successfully")
        return scan

    except Exception as e:
        logger.error(f"Error in ios_scan_data: {str(e)}")
        # Re-raise so Dagster knows the step failed
        raise