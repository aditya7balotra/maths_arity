import os

# ASSETS AND ASSETS_METADATA
CORES_FILE_NAME = "cores.json"
CHANNELS_FILE_NAME = "discipline_external_sources.json"
AUTO_GENERATED_METADATA_FILE_NAME = "generated_metadata.json"
VIDEO_REF_FLE_NAME = "v_refs.json"
SYLLABUS_FILE_NAME = "syllabus.pdf"
DISCIPLINE_EXTERNAL_LINKS_FILE_NAME = "discipline_external_sources.json"
SYLLABUS_UNIT_FILE_NAME = "syllabus.json"
ASSETS_METADATA_FOLDER_NAME = "assets_metadata"
URL_FILE_NAME = "urls.json"
COMMUNITY_PLATFORM_FILE_NAME = "community_platforms.json"

#in cloud
ASSETS_BASE_PATH = os.path.join("assets", "disciplines") # in cloud

# local side: pushing to cloud
ASSETS_PATH = os.path.join("/", "home", "adhi" , "Desktop", "arity_assets", "disciplines") # change as per yours