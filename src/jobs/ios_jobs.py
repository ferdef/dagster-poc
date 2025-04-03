from dagster import define_asset_job

ios_scan_job = define_asset_job(name="ios_scan_job", selection="ios_scan_data")
ios_seg_job = define_asset_job(name="ios_seg_job", selection="ios_segmentation")