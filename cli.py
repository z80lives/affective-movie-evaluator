#!/usr/bin/python3
import click
import os
from src.youtube import YouTubeModule
from src.playback import RecordSystem, VLCPlayer
from src.openpose import PoseSystem
from src.utils import SampleLoader

@click.group()
@click.version_option(version='1.0.0')
def greet():
    pass

def askRequiredField(required_fields, args):
    for k in required_fields:
        if len(args[required_fields[k]]) == 0:
            args[required_fields[k]] = click.prompt("Please enter "+k, type=str)

    return args


@greet.command()
@click.argument('video_file')
@click.option('--name', default="", help="Name of the Movie")
@click.option('--year', default="", help="Year movie war released.")
@click.option('--genre', default="", help="Genre of the movie.")
@click.option('--tags', default="", help="Extra tags for analytic purpose.")
@click.option('--person', default="", help="Viewer name.")
@click.option('--display', '-d', is_flag=True, help="Display camera video.")
def record(**kwargs):
    required_fields = {
        "Movie Name": "name",
        "Movie Year": "year",
        "Person Name": "person"        
    }
    other_fields = {
        "Tags": "tags",
        "Genre": "genre"
    }
    file_name = kwargs["video_file"]
    kwargs = askRequiredField(required_fields, kwargs)
    args = kwargs
    all_fields = {**required_fields, **other_fields}

    data = {}
    for k in all_fields:
        click.echo(k +": " + args[all_fields[k]])
        data[k] = args[all_fields[k]]

    print("Playing")
    player = VLCPlayer(file_name)
    #player.play_movie()
    
    print("Recording")
    sys = RecordSystem()
    filename = sys.createSampleDir()
    sys.saveMetaData(filename, data)
    sys.start_recording("test", player, False, filename)


@greet.command()
@click.argument('url')
@click.argument('file_name')
def download_youtube(**kwargs):
    print("Downloading youtube video from url: "+kwargs['url'] )
    yt_module = YouTubeModule()
    yt_module.download_video(kwargs['file_name'], kwargs['url'])
    click.echo("Done")

@greet.command()
@click.argument("filename")
def start_recording(**kwargs):
    sys = RecordSystem()
    print("Starting video capture")
    sys.start_recording(kwargs["filename"])


@greet.command()
@click.argument("filename")
def analyse_body_keypoints(**kwargs):
    click.echo("Initializing pose system")    
    sys = PoseSystem()

    click.echo("Analysing body keypoints ")
    loader = SampleLoader(kwargs["filename"])
    sys.analyse(loader.getVideoFile(), loader.getDir()+"body_points.npy")



#@click.command()
def greeter(**kwargs):
    click.echo("MEM command line execution script. ")
    click.echo("  Please type --help flag for more information")

if __name__ == '__main__':
    greet()
    #video()
