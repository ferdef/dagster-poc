from .assets import *
from .sensors import *
from .jobs import *
from dagster import Definitions


# Define Dagster definitions with explicitly listed assets
defs = Definitions(
    assets=[
        ios_scan_data,
        cbct_scan_data,
        ios_segmentation,
        cbct_teeth_segmentation,
        cbct_gum_detection,
        cbct_nerve_detection,
        aligned_model,
        crown_design
    ],
    sensors=[
      cbct_scan_data_sensor,
      cbct_teeth_seg_sensor,
      cbct_gum_seg_sensor,
      ios_scan_data_sensor,
      alignment_sensor,
      crown_design_sensor
    ],
    jobs=[
      materialize_all_job,
      starting_job,
      cbct_scan_job,
      cbct_teeth_seg_job,
      cbct_gum_seg_job,
      cbct_nerve_seg_job,
      ios_scan_job,
      ios_seg_job,
      alignment_job,
      crown_design_job
    ]
)