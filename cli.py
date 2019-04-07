#!/usr/bin/env python
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
@click.option('--display', '-d', is_flag=True, help="Display camera video.")
def analyse_body_keypoints(**kwargs):
    click.echo("Initializing pose system")    
    sys = PoseSystem()

    click.echo("Analysing body keypoints ")
    loader = SampleLoader(kwargs["filename"])
    sys.analyse(loader.getVideoFile(), loader.getDir()+"body_points.npy", kwargs['display'])

@greet.command()
@click.argument("filename")
@click.option('--display', '-d', is_flag=True, help="Display camera video.")
def analyse_head_keypoints(**kwargs):
    click.echo("Initializing pose system")
    from src.headpose import HeadPoseEstimator
    sys = HeadPoseEstimator()

    click.echo("Analysing body keypoints ")
    loader = SampleLoader(kwargs["filename"])
    sys.analyse(loader.getVideoFile(), loader.getDir()+"head_points.npy", kwargs['display'])


@greet.command()
@click.argument("filename")
@click.option('--display', '-d', is_flag=True, help="Display camera video.")
def view_body_keypoints(**kwargs):
    click.echo("Initializing pose system")
    from src.openpose import KeyPointVisualizer
    sys = KeyPointVisualizer()
    
    #loader = SampleLoader(kwargs["filename"])
    sys.viewKeypointsOnSample(kwargs["filename"])

@greet.command()
@click.argument("filename")
@click.option('--display', '-d', is_flag=True, help="Display camera video.")
def view_head_keypoints(**kwargs):
    click.echo("Initializing pose system")
    from src.headpose import HeadPoseVisualizer
    sys = HeadPoseVisualizer()
    
    #loader = SampleLoader(kwargs["filename"])
    sys.viewKeypointsOnSample(kwargs["filename"])

@greet.command()
@click.argument("fname")
def analyse_fer(**arg):
    #print("Analysing facial expressions")
    #print("Recording is in "+arg["fname"])
    from FER.ferAnalysis import FaceSystem
    video_file_name = arg["fname"] + "/test.avi"
    ##load your class
    system = FaceSystem()
    system.analyse(video_file_name)
    ## run analysis

@greet.command()
@click.argument('command', default="")
@click.option('--brightness', "-b", default="70", type=click.IntRange(0, 255))
@click.option('--contrast', "-c", default="50", type=click.IntRange(0, 255))
@click.option('--hue', "-H", default="50", type=int)
@click.option('--saturation', "-s", default="50", type=click.IntRange(0, 255))
@click.option('--width', "-w", default="640", type=int)
@click.option('--height', "-h", default="480", type=int)
@click.option('--gain', "-G", default="50", type=int)
def webcam(**args):
    from src.device import Webcam
    click.echo("Webcam module")
    command = args["command"]
    if  command == "test":
        wc = Webcam()
        wc.setResolution(args["width"], args["height"])
        wc.setLight(args["brightness"],
                    args["contrast"],
                    args["saturation"],
                    args["hue"],
                    args["gain"]
        )
        wc.test_run()
        
        
    

#@click.command()
def greeter(**kwargs):
    click.echo("MEM command line execution script. ")
    click.echo("  Please type --help flag for more information")

if __name__ == '__main__':
    greet()
    #video()
