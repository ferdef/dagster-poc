from dagster import define_asset_job

cbct_scan_job = define_asset_job(name="cbct_scan_job", selection="cbct_scan_data")
cbct_teeth_seg_job = define_asset_job(name="cbct_teeth_seg_job", selection="cbct_teeth_segmentation")
cbct_gum_seg_job = define_asset_job(name="cbct_gum_seg_job", selection="cbct_gum_detection")
cbct_nerve_seg_job = define_asset_job(name="cbct_nerve_seg_job", selection="cbct_nerve_detection")