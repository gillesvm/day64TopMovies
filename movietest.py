import requests

TMDB_API_KEY = "9fc352f9178876b5fab87008d9b86d3b"
TMDB_API_READER = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZmMzNTJmOTE3ODg3NmI1ZmFiODcwMDhkOWI4NmQzYiIsIm5iZiI6MTc0MjU3MDk0NS4xMiwic3ViIjoiNjdkZDg1YzE0YWE5NjZjZThjNjk4NDI5Iiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.OXKfQAZMgUdB7HnjMnIb3_m6_wEwBT-jv3tY9PB3QCY"
TMDB_API_ENDPOINT = "https://api.themoviedb.org/3"

url = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1&query='the matrix'"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZmMzNTJmOTE3ODg3NmI1ZmFiODcwMDhkOWI4NmQzYiIsIm5iZiI6MTc0MjU3MDk0NS4xMiwic3ViIjoiNjdkZDg1YzE0YWE5NjZjZThjNjk4NDI5Iiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.OXKfQAZMgUdB7HnjMnIb3_m6_wEwBT-jv3tY9PB3QCY",
}

response = requests.get(url, headers=headers)
data = response.json()
for result in data["results"]:
    print(f"{result['title']} - {result['release_date']}")
