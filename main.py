import re
import os
import csv
import requests
from requests import Response
from concurrent.futures.thread import ThreadPoolExecutor as Executor


def request_top_250_movies_imdb(imdb_top_movies_url: str) -> Response:
    """Request the 250 top movies IMDb page.

    Args:
        imdb_top_movies_url (str): link of the page

    Returns:
        Response: response of the page
    """
    return requests.get(imdb_top_movies_url)


def get_top_250_movies_imdb_ids(res: Response) -> list[str]:
    """Get the ids of the 250 movies page response.

    Args:
        res (Response): response of the 250 top movies imdb page

    Returns:
        list[str]: list with IMDb movie ids
    """
    all_imdb_ids_raw = re.findall('tt\d+', res.text)
    all_ids_movies = []
    [all_ids_movies.append(
        id_movie) for id_movie in all_imdb_ids_raw if id_movie not in all_ids_movies]
    return all_ids_movies


def get_movies_informations_response(all_ids_movies: list[str]) -> list[Response]:
    """Get all responses with movie's information

    Args:
        all_ids_movies (list[str]): list with IMDb movie ids


    Returns:
        list[Response]: list with the responses with movie information
    """
    with Executor() as executor:
        result = executor.map(request_movie_information, all_ids_movies)
    return list(result)


def request_movie_information(imdb_id_movie: str) -> Response:
    """Request OMDb Api with a IMDb id to get informations about the movie

    Args:
        imdb_id_movie (str): IMDb id

    Returns:
        Response: response of the movie request info
    """
    params = {
        'i': imdb_id_movie,
        'apikey': os.environ['API_KEY']
    }
    url = 'http://www.omdbapi.com/'
    return requests.get(url, params=params)


def parse_all_movie_data(res_list: list[Response]) -> list[dict[str, str]]:
    """Receive all responses and extract informations

    Args:
        res_list (list[Response]): all response movie requests

    Returns:
        list[dict[str, str]]: all movies data sorte by movie rating
    """
    all_movie_data = []
    for res in res_list:
        all_movie_data.append(
            parse_movie_information(res)
        )
    return sorted(all_movie_data, key=lambda d: d['imdbRating'], reverse=True)


def parse_movie_information(res: Response) -> dict[str, str]:
    """Treat the response data 

    Args:
        res (Response): response movie request

    Returns:
        dict[str, str]: movie information
    """
    return {
        'imdbID': res.json()['imdbID'],
        'title': res.json()['Title'],
        'year': res.json()['Year'],
        'released': res.json()['Released'],
        'runtime': res.json()['Runtime'],
        'genre': res.json()['Genre'],
        'imdbRating': res.json()['imdbRating'],
    }


def save_csv_file(data_to_save: list[dict[str, str]]) -> None:
    """Save csv file

    Args:
        data_to_save (list[dict[str, str]]): data to be saved
    """
    with open('movie_data.csv', 'w', encoding='utf8', newline='') as csv_file:
        fieldnames = data_to_save[0].keys()
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for data in data_to_save:
            csv_writer.writerow(data)


if __name__ == '__main__':
    imdb_top_movies_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    response = request_top_250_movies_imdb(imdb_top_movies_url)
    all_ids_movies = get_top_250_movies_imdb_ids(response)
    res_list = get_movies_informations_response(all_ids_movies)
    data_to_save = parse_all_movie_data(res_list)
    save_csv_file(data_to_save)
