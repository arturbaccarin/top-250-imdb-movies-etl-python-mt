# Top 250 IMDB Movies - ETL Multithread

> Get informations about top 250 movies list by IMDb and save in a CSV file.

### Requirements
* Docker;
* Open Movie Database (OMDb) Api Key.

### Setup
1. Generate a OMDb Api Key in here: https://www.omdbapi.com/apikey.aspx;
2. Add your Api Key in Dockerfile in `ENV API_KEY your_omdb_api_key_goes_here`;
3. Build an image: `docker build -t movie-app .`;

### How to execute
1. Run the container: `docker run -v $(PWD):/app movie-app`
    * You can remove the container after its execution with the flag `--rm`: `docker run -v $(PWD):/app --rm movie-app`
    * Maybe you'll need to put in `$(PWD)` your folder's absolute path.

### Result
It'll create a csv file named `movie_data.csv` in root folder of the project.

### Attention
You only have 1.000 requests with a Free OMDb Api Key and this project uses 250 per running.

### What is used in this project
* Python (requests);
* API;
* JSON;
* Multihreading;
* CSV;
* Docker;
* Docker Volumes.