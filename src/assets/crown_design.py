import time
from dagster import (
    asset,
    AssetIn,
    AssetExecutionContext,
    MetadataValue,
    get_dagster_logger,

)
from ..constants import CROWN_DESIGN_TIME, OUTPUT_FILE_EXTENSION, GROUP_OUTPUT
from .ios_segment_teeth import ios_segmentation
from .cbct_segment_teeth import cbct_teeth_key

logger = get_dagster_logger()

class CrownDesign:
    """
    Represents a dental crown design based on segmentation data.
    """
    def __init__(self, name, tooth_number, segmentations):
        self.name = name
        self.tooth_number = tooth_number
        self.segmentations = segmentations
        self.design_complete = True

    def __repr__(self):
        return f"CrownDesign(name={self.name}, tooth={self.tooth_number})"

@asset(
    ins={
        "ios_seg": AssetIn(key=ios_segmentation.key),
        "teeth_seg": AssetIn(key=cbct_teeth_key)
    },
    group_name=GROUP_OUTPUT,
    metadata={
        "processing_time": f"{CROWN_DESIGN_TIME}s",
        "description": "Designs a dental crown based on segmentation results",
    }
)
def crown_design(
    context: AssetExecutionContext,
    ios_seg,
    teeth_seg
):
    """
    Design a crown using IOS segmentation and CBCT teeth segmentation.
    """
    logger.info("Designing crown...")
    time.sleep(CROWN_DESIGN_TIME)

    # In a real implementation, this would use the segmentation results
    # to design a crown that fits the patient's teeth

    # Create the crown design using the class defined at module level
    crown = CrownDesign("patient_crown_design", 14, {
        "ios": ios_seg,
        "teeth": teeth_seg
    })

    # Make sure we're using standard Python types in metadata
    tooth_num = int(crown.tooth_number)
    design_complete = bool(crown.design_complete)

    context.add_output_metadata({
        "design_complete": MetadataValue.bool(design_complete),
        "tooth_number": MetadataValue.int(tooth_num),
        "output_file": f"patient_crown_tooth{tooth_num}{OUTPUT_FILE_EXTENSION}"
    })

    return crown