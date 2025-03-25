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
from .constants import CBCT_TEETH_SEGMENTATION_TIME, GROUP_SEGMENTATION
from .safe_data import safe_float
from .segmentation_result import SegmentationResult
from .cbct_scan import cbct_scan_data

logger = get_dagster_logger()

cbct_teeth_key = AssetKey("cbct_teeth_segmentation")

@asset(
    ins={
        "cbct_data": AssetIn(key=cbct_scan_data.key),
    },
    key=cbct_teeth_key,
    group_name=GROUP_SEGMENTATION,
    metadata={
        "processing_time": f"{CBCT_TEETH_SEGMENTATION_TIME}s",
        "description": "Segmented teeth from CBCT scan",
    }
)
def cbct_teeth_segmentation(context: AssetExecutionContext, cbct_data):
    """
    Perform teeth segmentation on CBCT scan data.

    This is the first step in the CBCT segmentation pipeline.
    """
    upper_jaw = cbct_data["upper_jaw"]
    lower_jaw = cbct_data["lower_jaw"]

    # Step 1: Teeth segmentation
    logger.info("Segmenting teeth from CBCT...")
    time.sleep(CBCT_TEETH_SEGMENTATION_TIME)

    teeth_upper = SegmentationResult("upper_teeth", upper_jaw)
    teeth_lower = SegmentationResult("lower_teeth", lower_jaw)
    teeth_result = {
        "upper_jaw": teeth_upper,
        "lower_jaw": teeth_lower
    }

    context.add_output_metadata({
        "upper_segmented": MetadataValue.float(safe_float(np.mean(teeth_upper.data) * 100)),
        "lower_segmented": MetadataValue.float(safe_float(np.mean(teeth_lower.data) * 100))
    })

    logger.info("CBCT teeth segmentation complete - crown design can begin")
    return teeth_result