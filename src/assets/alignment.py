import time
from dagster import (
    asset,
    AssetIn,
    AssetExecutionContext,
    MetadataValue,
    get_dagster_logger,
)
from ..constants import *
from .ios_segment_teeth import ios_segmentation
from .cbct_nerve_channels import cbct_nerve_key
from .cbct_gum_region import cbct_gum_key
from .cbct_segment_teeth import cbct_teeth_key


logger = get_dagster_logger()

class AlignedModel:
    """
    Represents an aligned 3D model created from multiple segmentation results.
    """
    def __init__(self, name, source_segmentations):
        self.name = name
        self.source_segmentations = source_segmentations
        self.aligned = True

    def __repr__(self):
        return f"AlignedModel(name={self.name}, aligned={self.aligned})"

@asset(
    ins={
        "ios_seg": AssetIn(key=ios_segmentation.key),
        "teeth_seg": AssetIn(key=cbct_teeth_key),
        "gum_det": AssetIn(key=cbct_gum_key),
        "nerve_det": AssetIn(key=cbct_nerve_key)
    },
    group_name=GROUP_OUTPUT,
    metadata={
        "processing_time": f"{ALIGNMENT_TIME}s",
        "description": "Aligns IOS and CBCT segmentations into a unified model",
    }
)
def aligned_model(
    context: AssetExecutionContext,
    ios_seg,
    teeth_seg,
    gum_det,
    nerve_det
):
    """
    Align the results from IOS and CBCT segmentations to create a single detailed file.
    """
    logger.info("Aligning segmentation results...")
    time.sleep(ALIGNMENT_TIME)

    # In a real implementation, this would combine the segmentation results
    # into a single coherent 3D model

    # Create the aligned model using the class defined at module level
    aligned = AlignedModel("patient_aligned_model", {
        "ios": ios_seg,
        "teeth": teeth_seg,
        "gums": gum_det,
        "nerves": nerve_det
    })

    # Convert Python boolean to standard Python int for metadata
    aligned_bool = 1 if aligned.aligned else 0
    seg_count = len(aligned.source_segmentations)

    context.add_output_metadata({
        "aligned": MetadataValue.bool(aligned.aligned),
        "source_segmentations": MetadataValue.int(seg_count),
        "output_file": f"patient_aligned_model{OUTPUT_FILE_EXTENSION}"
    })

    return aligned