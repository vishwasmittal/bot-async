FROM python:3.6.5

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code

WORKDIR /code

# ENV AIO_APP_PATH="app/"
# ENV AIO_STATIC_PATH="static/"

# this is the key used to encrypt cookies. Keep it safe!
# you can generate a new key with `base64.urlsafe_b64encode(os.urandom(32))`
# ENV APP_COOKIE_SECRET="2Cn_jUseVJuX61ka3qtv9tWZ4NDtXYwe4GgR2c3UvZk="

# ENV DP_SERVER_HOST='0.0.0.0'
# ENV DP_SERVER_PORT='4000'
# ENV DP_MONGO_SERVER_HOST='127.0.0.1'
# ENV DP_MONGO_SERVER_PORT='27017'
# ENV DP_MONGO_SERVER_DATABASE='test_database'
# ENV DP_GOOGLE_STORAGE_SA_AUTH_JSON="/Users/vishwas/Downloads/Suryodya-924ec8a4816a.json"
# ENV DP_GOOGLE_PROJECT_ID="suryodyad"
# ENV DP_GOOGLE_STORAGE_BUCKET="suryodyad.appspot.com"


CMD [ "python", "server.py" ]
# CMD [ "adev", "runserver", "--host", "0.0.0.0", "--port", "4000", "--no-livereload" ]