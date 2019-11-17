from src.utils import MovieController
from src.youtube import YouTubeModule
import pytube

m = MovieController()
files = m.read_files()
metadata = m.readMetadata()
youtube_module = YouTubeModule()

for key in metadata:
    if key not in files:
        print("Movie file not '%s' missing..." % key)
        youtube_url = metadata[key]["youtube"]
        if  youtube_url != "":
            print("Youtube link found")            
            youtube_module.download_video(key, youtube_url)
            print("Download complete")
    else:
        print("Movie \"%s\" found" % key)