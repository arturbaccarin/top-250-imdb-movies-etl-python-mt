from requests import Response
from main import (
    request_top_250_movies_imdb,
    get_top_250_movies_imdb_ids,
    request_movie_information,
    parse_movie_information,
    parse_all_movie_data,
    get_movies_informations_response
)


def test_request_top_250_movies_imdb():
    imdb_top_movies_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    response = request_top_250_movies_imdb(imdb_top_movies_url)
    assert response.status_code == 200
    assert 'IMDb Top 250 Movies' in response.text


def test_get_top_250_movies_imdb_ids():
    imdb_top_movies_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    response = request_top_250_movies_imdb(imdb_top_movies_url)
    all_ids_movies = get_top_250_movies_imdb_ids(response)
    assert isinstance(all_ids_movies, list)
    assert isinstance(all_ids_movies[0], str)
    assert 'tt' in all_ids_movies[0]


def test_request_movie_information():
    imdb_id_movie = 'tt0120737'
    response = request_movie_information(imdb_id_movie)
    assert response.status_code == 200


def test_parse_movie_information():
    imdb_id_movie = 'tt0120737'
    response = request_movie_information(imdb_id_movie)
    result = parse_movie_information(response)
    assert isinstance(result, dict)
    assert 'The Lord of the Rings' in result['title']


def test_parse_all_movie_data():
    imdb_id_movie = 'tt0120737'
    response1 = request_movie_information(imdb_id_movie)
    imdb_id_movie = 'tt0111161'
    response2 = request_movie_information(imdb_id_movie)
    result = parse_all_movie_data([response1, response2])
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], dict)


def test_get_movies_informations_response():
    imdb_id_movie1 = 'tt0120737'
    imdb_id_movie2 = 'tt0111161'
    result = get_movies_informations_response([imdb_id_movie1, imdb_id_movie2])
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], Response)
