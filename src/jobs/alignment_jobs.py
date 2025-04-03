from dagster import define_asset_job

alignment_job = define_asset_job(name="alignment_job", selection="aligned_model")