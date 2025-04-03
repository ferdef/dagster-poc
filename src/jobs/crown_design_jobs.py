from dagster import define_asset_job

crown_design_job = define_asset_job(name="crown_design_job", selection="crown_design")