from dagster import define_asset_job

materialize_all_job = define_asset_job("materialize_all", selection="*")
# cron_design_job = define_asset_job(name="crown_design_job", selection="*crown_design")
starting_job = define_asset_job("starting_job", selection=["ios_scan_data","cbct_scan_data"])