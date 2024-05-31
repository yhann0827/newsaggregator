# News Aggregator

- Develop, implement, and deploy a RESTful web API for a news agency using Django.
- Host the API on [pythonanywhere.com](https://www.pythonanywhere.com/).
- Write a news aggregator to collect news from APIs adhering to provided specifications.
- Test the aggregator by collecting news from peers' deployed APIs.

### Create a News Agency
- Maintain tables for authors and news stories.

### Develop a RESTful Web Interface
- **Log In:**
  - POST `/api/login` with `username` and `password`.
  - Response: `200 OK` with welcome message or appropriate error code.
- **Log Out:**
  - POST `/api/logout` with no payload.
  - Response: `200 OK` with goodbye message or appropriate error code.
- **Post a Story:**
  - POST `/api/stories` with story details.
  - Response: `201 CREATED` or appropriate error code.
- **Get Stories:**
  - GET `/api/stories` with filters for category, region, and date.
  - Response: `200 OK` with list of stories or appropriate error code.
- **Delete Story:**
  - DELETE `/api/stories/key` to delete a story.
  - Response: `200 OK` or appropriate error code.


## Client Application
- Command line interface to interact with APIs.
- Display list of news agencies and aggregate news stories.
- Supported commands:
  - `login`, `logout`, `post`, `news`, `list`, `delete`.
