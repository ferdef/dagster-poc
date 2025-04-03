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
from ..constants import CBCT_GUM_DETECTION_TIME, GROUP_SEGMENTATION
from ..safe_data import safe_float
from ..segmentation_result import SegmentationResult
from .cbct_scan import cbct_scan_data
from .cbct_segment_teeth import cbct_teeth_key

logger = get_dagster_logger()

cbct_gum_key = AssetKey("cbct_gum_detection")

@asset(
    ins={
        "cbct_data": AssetIn(key=cbct_scan_data.key),
        "teeth_segmentation": AssetIn(key=cbct_teeth_key),
    },
    key=cbct_gum_key,
    group_name=GROUP_SEGMENTATION,
    metadata={
        "processing_time": f"{CBCT_GUM_DETECTION_TIME}s",
        "description": "Detected gum regions from CBCT scan",
    }
)
def cbct_gum_detection(context: AssetExecutionContext, cbct_data, teeth_segmentation):
    """
    Perform gum detection on CBCT scan data.

    This is the second step in the CBCT segmentation pipeline, which starts
    after teeth segmentation is complete.
    """
    upper_jaw = cbct_data["upper_jaw"]
    lower_jaw = cbct_data["lower_jaw"]

    # Step 2: Gum detection (depends on teeth segmentation being done)
    logger.info("Detecting gums from CBCT...")
    time.sleep(CBCT_GUM_DETECTION_TIME)

    gum_upper = SegmentationResult("upper_gum", upper_jaw)
    gum_lower = SegmentationResult("lower_gum", lower_jaw)
    gum_result = {
        "upper_jaw": gum_upper,
        "lower_jaw": gum_lower
    }

    context.add_output_metadata({
        "upper_segmented": MetadataValue.float(safe_float(np.mean(gum_upper.data) * 100)),
        "lower_segmented": MetadataValue.float(safe_float(np.mean(gum_lower.data) * 100))
    })

    logger.info("CBCT gum detection complete")
    return gum_result