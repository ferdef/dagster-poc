import time
from dagster import (
    asset,
    AssetExecutionContext,
    MetadataValue,
    get_dagster_logger
)
from ..constants import GROUP_INPUT, CBCT_LOAD_TIME
from ..safe_data import safe_float
from ..dental_scan import DentalScan

logger = get_dagster_logger()

@asset(
    group_name=GROUP_INPUT,
    metadata={
        "file_type": "DICOM",
        "description": "CBCT scan data for upper and lower jaw",
    }
)
def cbct_scan_data(context: AssetExecutionContext):
    """
    Load CBCT (Cone Beam Computed Tomography) scan data from file system.
    """
    logger.info("Loading CBCT scan data...")
    time.sleep(CBCT_LOAD_TIME)  # Simulate loading time

    # Create simulated scan objects for upper and lower jaw
    upper_jaw = DentalScan("upper_jaw", "CBCT", dimensions=(300, 300, 150))
    lower_jaw = DentalScan("lower_jaw", "CBCT", dimensions=(300, 300, 150))

    # Log some information about the loaded data
    total_size_mb = (upper_jaw.data.nbytes + lower_jaw.data.nbytes) / 1024 / 1024
    # Convert to standard Python float
    total_size_mb = safe_float(total_size_mb)

    context.add_output_metadata({
        "upper_jaw_dimensions": MetadataValue.json(tuple(map(int, upper_jaw.dimensions))),
        "lower_jaw_dimensions": MetadataValue.json(tuple(map(int, lower_jaw.dimensions))),
        "file_size_mb": MetadataValue.float(total_size_mb),
        "scan_type": "CBCT"
    })

    return {
        "upper_jaw": upper_jaw,
        "lower_jaw": lower_jaw
    }