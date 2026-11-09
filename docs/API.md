# API Reference

## Authentication
- **Method:** POST
- **Endpoint:** `/api/auth`
- **Request Body:** `{"username": "string", "password": "string"}`
- **Response (200 OK):** `{"token": "string"}`

## Endpoints
### [METHOD] /api/anagrams
- **Description:** Returns a list of anagrams for a given word
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:** `{"word": "string"}`
- **Response (200 OK):** `{"anagrams": ["string"]}`
- **Error Responses:**
  - **400 Bad Request:** `{"error": "Invalid request"}`

### [METHOD] /api/submit
- **Description:** Submits a word for anagram generation
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:** `{"word": "string"}`
- **Response (200 OK):** `{"anagrams": ["string"]}`
- **Error Responses:**
  - **400 Bad Request:** `{"error": "Invalid request"}`

### [METHOD] /api/export
- **Description:** Exports anagrams data to JSON
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:** `{"word": "string"}`
- **Response (200 OK):** `{"anagrams": ["string"]}`
- **Error Responses:**
  - **400 Bad Request:** `{"error": "Invalid request"}`

## Error Handling
- **400 Bad Request:** `{"error": "Invalid request"}`
- **401 Unauthorized:** `{"error": "Unauthorized"}`
- **500 Internal Server Error:** `{"error": "Internal server error"}`