import requests
import click
import textwrap

FILM_DB_URL = 'http://www.omdbapi.com/'

class Movie(object):

    MOVIE_FORMAT = """
Title:           {title}
Director:        {director}
Actors:          {actors}
Runtime:         {runtime}
Metascore:       {metascore}
IMDB:            {imdb}
Rotten Tomatoes: {rotten_tomatoes}
Released:        {released}
Plot:
----
{plot}
----
"""

    def __init__(self, title, director, actors, runtime, metascore, imdb,
        rotten_tomatoes, released, plot):
        self.title = title
        self.director = director
        self.actors = actors
        self.runtime = runtime
        self.metascore = metascore
        self.imdb = imdb
        self.rotten_tomatoes = rotten_tomatoes
        self.released = released
        self.plot = plot

    def from_title(title):
        params = {'t': title, 'type': 'movie', 'tomatoes': 'true'}
        result = requests.get(FILM_DB_URL, params=params).json()
        return Movie(
            title=result['Title'],
            director=result['Director'],
            actors=result['Actors'],
            runtime=result['Runtime'],
            metascore=result['Metascore'],
            imdb=result['imdbRating'],
            rotten_tomatoes=result['tomatoRating'],
            released=result['Released'],
            plot=result['Plot']
        )

    def __str__(self):
        plot = textwrap.fill(self.plot, 80)
        return Movie.MOVIE_FORMAT.format(
            title=self.title,
            director=self.director,
            actors=self.actors,
            runtime=self.runtime,
            metascore=self.metascore,
            imdb=self.imdb,
            rotten_tomatoes=self.rotten_tomatoes,
            released=self.released,
            plot=plot
        )

@click.group()
def cli():
    pass

@cli.command()
@click.option('--fname', help='File with movie names', required=True)
@click.option('--rating', default='metascore', help='Website to use for ratings')
def rating(fname, rating):
    names = open(fname).readlines()
    movies = [Movie.from_title(name) for name in names]
    highest = max(movies, key= lambda m: float(getattr(m, rating)))
    lowest = min(movies, key=lambda m: float(getattr(m, rating)))
    click.echo('\n\n--Highest--\n\n')
    click.echo(highest)
    click.echo('\n\n--Lowest--\n\n')
    click.echo(lowest)

@cli.command()
@click.option('--title', default='', help='Movie title')
def info(title):
    movie = Movie.from_title(title)
    click.echo(movie)

if __name__ == '__main__':
    cli()
