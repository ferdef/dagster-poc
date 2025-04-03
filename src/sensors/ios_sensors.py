from dagster import asset_sensor, DefaultSensorStatus, AssetKey, RunRequest

@asset_sensor(
  asset_key=AssetKey("ios_scan_data"),
  job_name="ios_seg_job",
  default_status=DefaultSensorStatus.RUNNING,
)
def ios_scan_data_sensor():
  return RunRequest()