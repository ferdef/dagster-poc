from dagster import multi_asset_sensor, DefaultSensorStatus, AssetKey, RunRequest

@multi_asset_sensor(
  monitored_assets=[
    AssetKey("cbct_teeth_segmentation"),
    AssetKey("ios_segmentation")
  ],
  job_name="crown_design_job",
  default_status=DefaultSensorStatus.RUNNING,
)
def crown_design_sensor(context):
  asset_events = context.latest_materialization_records_by_key()
  if any(asset_events.values()):
      context.advance_all_cursors()
      return RunRequest(run_key=context.cursor, run_config={})
  return None