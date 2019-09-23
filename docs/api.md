# API Documentation

## POST /api/v1/xyz

...

### Form parameters

- `limit` (default: 30) - Number of results to return.
- `offset` (default: 0) - Starting offset.
- `url` - Image URL to fetch and test.

### Response

Returns a JSON object with the following properties:

- `success` - True or false based on whether the query is successful.
- `error` - If success is false, the error code will be here.
- `match` - True if a match was found.
- `added` - True if no match was found, and the image was added to the database.
- `results` - Array containing the image that matched, if any.
- `timing` - Time in seconds to query the database.

