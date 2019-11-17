from pytube import YouTube

class YouTubeModule:
    def show_progress_bar(self,stream, chunk, file_handle, bytes_remaining):
        print('Remaining [%d]\r'%bytes_remaining, end="")
        return

    def download_video(self, movie_name, url):        
        yt = YouTube(url)
        yt.register_on_progress_callback(self.show_progress_bar)
        movie_name = movie_name.split(".")        
        if len(movie_name) > 1:
            movie_name = movie_name[0]
        yt.streams.filter(file_extension='mp4').first().download("./movies/", movie_name)
