
if __name__ == "__main__":
    from assets_pipeline.cloud_service import CloudStorageService
    from assets_pipeline.asset_metadata_handler import MetaDataHandler
   
    def run_pipeline():
        ASSETS_PATH = "/home/adhi/Desktop/arity_assets/disciplines"
        # ASSETS_PATH = "/home/adhi/Desktop/demo_arity_assets"
        meta_handler = MetaDataHandler(assets_path= ASSETS_PATH)
        meta_handler.create_assets_meta()
        c_storage = CloudStorageService(assetPath= ASSETS_PATH)
        c_storage.traverse_upload_asset_get_urls_and_save_assets_meta()

    run_pipeline()
