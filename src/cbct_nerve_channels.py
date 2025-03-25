import time
import numpy as np
from dagster import (
    asset,
    AssetIn,
    AssetExecutionContext,
    MetadataValue,
    get_dagster_logger,
    AssetKey
)
from .constants import CBCT_NERVE_DETECTION_TIME, GROUP_SEGMENTATION
from .safe_data import safe_float
from .segmentation_result import SegmentationResult
from .cbct_scan import cbct_scan_data
from .cbct_gum_region import cbct_gum_key


logger = get_dagster_logger()

cbct_nerve_key = AssetKey("cbct_nerve_detection")

@asset(
    ins={
        "cbct_data": AssetIn(key=cbct_scan_data.key),
        "gum_detection": AssetIn(key=cbct_gum_key),
    },
    key=cbct_nerve_key,
    group_name=GROUP_SEGMENTATION,
    metadata={
        "processing_time": f"{CBCT_NERVE_DETECTION_TIME}s",
        "description": "Detected nerve channels from CBCT scan",
    }
)
def cbct_nerve_detection(context: AssetExecutionContext, cbct_data, gum_detection):
    """
    Perform nerve detection on CBCT scan data.

    This is the third step in the CBCT segmentation pipeline, which starts
    after gum detection is complete.
    """
    lower_jaw = cbct_data["lower_jaw"]

    # Step 3: Nerve detection (depends on gum detection being done)
    logger.info("Detecting nerves from CBCT...")
    time.sleep(CBCT_NERVE_DETECTION_TIME)

    # Nerves are typically only in the lower jaw
    nerve_lower = SegmentationResult("lower_nerve", lower_jaw)
    # For nerve detection, we want fewer positive voxels
    nerve_lower.data = np.random.choice(
        [True, False],
        size=lower_jaw.data.shape,
        p=[0.05, 0.95]  # Only 5% of voxels are nerve tissue
    )

    nerve_result = {
        "lower_jaw": nerve_lower
    }

    context.add_output_metadata({
        "nerve_volume_percentage": MetadataValue.float(safe_float(np.mean(nerve_lower.data) * 100))
    })

    logger.info("CBCT nerve detection complete")
    return nerve_result