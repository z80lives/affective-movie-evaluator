#!/usr/bin/python3
import click
from src.youtube import YouTubeModule

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
    kwargs = askRequiredField(required_fields, kwargs)
    args = kwargs
    all_fields = {**required_fields, **other_fields}

    for k in all_fields:
        click.echo(k +": " + args[all_fields[k]])


@greet.command()
@click.argument('url')
@click.argument('file_name')
def download_youtube(**kwargs):
    print("Downloading youtube video from url: "+kwargs['url'] )
    yt_module = YouTubeModule()
    yt_module.download_video(kwargs['file_name'], kwargs['url'])
    click.echo("Done")


#@click.command()
def greeter(**kwargs):
    click.echo("MEM command line execution script. ")
    click.echo("  Please type --help flag for more information")

if __name__ == '__main__':
    greet()
    #video()
