from dagster import asset_sensor, DefaultSensorStatus, AssetKey, RunRequest

@asset_sensor(
  asset_key=AssetKey("cbct_scan_data"),
  job_name="cbct_teeth_seg_job",
  default_status=DefaultSensorStatus.RUNNING,
)
def cbct_scan_data_sensor():
  print("Running test_sensor...")
  return RunRequest()

@asset_sensor(
  asset_key=AssetKey("cbct_teeth_segmentation"),
  job_name="cbct_gum_seg_job",
  default_status=DefaultSensorStatus.RUNNING,
)
def cbct_teeth_seg_sensor():
  return RunRequest()

@asset_sensor(
  asset_key=AssetKey("cbct_gum_detection"),
  job_name="cbct_nerve_seg_job",
  default_status=DefaultSensorStatus.RUNNING,
)
def cbct_gum_seg_sensor():
  return RunRequest()