import dropbox, cloudinary
from backend.config import *
from dropbox.exceptions import ApiError
import time

cldinary = cloudinary.config( 
        cloud_name = CLOUD_NAME,
        api_key = API_KEY,
        api_secret = API_SECRET
    )

dbx = dropbox.Dropbox(
    app_key=APP_KEY,
    app_secret= APP_SECRET,
    oauth2_refresh_token=REFRESH_TOKEN
)


def dropbox_get_temp_url(discipline: str, core_id: str, unit: str, sem: str):
    def get_dropbox_file_path(discipline, sem, core_id, unit):
        file_path = f"/assets/disciplines/{discipline}/{sem}/{core_id}/notes/{unit}.pdf"
        return file_path
    try:
        temp_url= dbx.files_get_temporary_link(path = get_dropbox_file_path(discipline= discipline, sem = sem, core_id= core_id, unit = unit)).link
        # preview_wrapper = f"https://docs.google.com/viewer?url={temp_url}&embedded=true"
        # return preview_wrapper
        return temp_url
    except ApiError as e:
        return None



def cloudinary_get_temp_url(public_id: str):
    current_timestamp = int(time.time())
    return cloudinary.utils.private_download_url(
            public_id,
            format="pdf",
            resource_type="raw",
            expires_at=current_timestamp + CLOUDINARY_EXPIRY_TIME_SECONDS,
            timestamp=current_timestamp,
            attachment = False
        )