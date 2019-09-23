# API Test Commands

## Image search API

```
curl -X POST \
  -F "query_img=@../static/data/keyframes/0a9d430ac04d94e8c148dec1d97076c6f931db35127e6e2e1953dca404f4c195_001.jpg" \
  127.0.0.1:3000/api/v1/search/image
```

## Collections API

```
Index:

curl -X GET 127.0.0.1:5000/api/v1/collection/

Show:

curl -X GET 127.0.0.1:5000/api/v1/collection/1/

Create:

curl -X POST \
  -F "title=My Collection" \
  -F "author=user" \
  127.0.0.1:5000/api/v1/collection/

Update:

curl -X PUT \
  -F "title=My Renamed Collection" \
  -F "author=user" \
  127.0.0.1:5000/api/v1/collection/1/

Destroy:

curl -X DELETE 127.0.0.1:5000/api/v1/collection/1/

Add media to collection:

curl -X PUT \
  -F "media_id=123" \
  -F "author=user" \
  127.0.0.1:5000/api/v1/collection/1/add/

Delete media from collection:

curl -X DELETE 127.0.0.1:5000/api/v1/collection/1/media/123/
```
