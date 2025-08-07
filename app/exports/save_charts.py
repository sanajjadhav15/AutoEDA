import zipfile
import os
from tempfile import TemporaryDirectory

def zip_chart_images(file_paths, zip_name="charts_bundle.zip"):
    """
    Zips a list of file paths into a single .zip file and returns the path.
    """
    tmpdir = TemporaryDirectory()
    zip_path = os.path.join(tmpdir.name, zip_name)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_path in file_paths:
            arcname = os.path.basename(file_path)
            zipf.write(file_path, arcname=arcname)

    return zip_path, tmpdir  # Return both path and the tempdir object (to prevent early deletion)
