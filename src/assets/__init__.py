"""
Dagster repository definition for phase 3.
Updated to be compatible with Dagster 1.8.5
"""
from dagster import Definitions, define_asset_job

# Import assets directly from the module
from .ios_scan import ios_scan_data
from .cbct_scan import cbct_scan_data
from .ios_segment_teeth import ios_segmentation
from .cbct_segment_teeth import cbct_teeth_segmentation
from .cbct_gum_region import cbct_gum_detection
from .cbct_nerve_channels import cbct_nerve_detection
from .alignment import aligned_model
from .crown_design import crown_design