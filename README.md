# Collection Service

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=THI-CND_collection_service&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=THI-CND_collection_service)

## Übersicht

Der Collection Service verwaltet Sammlungen von Rezepten für Benutzer.

---

## Schnittstellen

### REST API

#### GET /api/v1/collections

Ruft alle Sammlungen ab.

**Request:**

- Methode: GET
- URL: `/api/v1/collections`

**Response:**

- Status: 200 OK
- Body: Eine Liste von Sammlungen.

**Beispiel:**
GET "http://localhost:8000/api/v1/collections"

#### GET /collections/{id}

Ruft eine bestimmte Sammlung ab.

**Request:**

- Methode: GET
- URL: `/api/v1/collections/{id}`

**Response:**

- Status: 200 OK
- Body: Die angeforderte Sammlung.

**Beispiel:**
GET "http://localhost:8000/api/v1/collections/1"

#### POST /collections

Erstellt eine neue Sammlung.

**Request:**

- Methode: POST
- URL: `/api/v1/collections`
- Body: JSON-Objekt mit den Daten der neuen Sammlung.

**Response:**

- Status: 201 OK
- Body: Die erstellte Sammlung.

**Beispiel:**
POST "http://localhost:8000/api/v1/collections"

```json
{
  "name": "Neue Sammlung",
  "author": "testuser",
  "description": "Beschreibung der Sammlung",
  "recipes": [1, 2]
}
```

#### PUT /api/v1/collections/{id}

Aktualisiert eine bestehende Sammlung.

**Request:**

- Methode: PUT
- URL: `/api/v1/collections/{id}`
- Body: JSON-Objekt mit den aktualisierten Daten der Sammlung.

**Response:**

- Status: 200 OK
- Body: Die aktualisierte Sammlung.

**Beispiel:**
PUT "http://localhost:8000/api/v1/collections/1"

```json
{
  "name": "Aktualisierte Sammlung",
  "author": "testuser",
  "description": "Aktualisierte Beschreibung",
  "recipes": [1, 2]
}
```

#### DELETE /api/v1/collections/{id}

Löscht eine bestehende Sammlung.

**Request:**

- Methode: DELETE
- URL: `/api/v1/collections/{id}`
- Body: JSON-Objekt mit den Daten des Autors.

**Response:**

- Status: 200 OK
- Body: Bestätigung der Löschung.

**Beispiel:**
DELETE "http://localhost:8000/api/v1/collections/1"

```json
{
  "author": "testuser"
}
```

#### POST /api/v2/collections/{id}/recipe

Fügt ein Rezept zu einer Sammlung hinzu.

**Request:**

- Methode: POST
- URL: `/api/v2/collections/{id}/recipe`
- Body: JSON-Objekt mit der ID des Rezepts.

**Response:**

- Status: 200 OK
- Body: Die aktualisierte Sammlung.

**Beispiel:**
POST "http://localhost:8000/api/v2/collections/1/recipe"

```json
{
  "recipe_id": 1
}
```

#### DELETE /api/v2/collections/{id}/recipe

Entfernt ein Rezept aus einer Sammlung.

**Request:**

- Methode: DELETE
- URL: `/api/v2/collections/{id}/recipe`
- Body: JSON-Objekt mit der ID des Rezepts.

**Response:**

- Status: 200 OK
- Body: Die aktualisierte Sammlung.

**Beispiel:**
DELETE "http://localhost:8000/api/v2/collections/1/recipe"

```json
{
  "recipe_id": 1
}
```

---

### gRPC API

```java
syntax = "proto3";

package collection_service;

service CollectionService {
    rpc GetCollections (Empty) returns (ListCollectionResponse);
    rpc GetCollectionById (CollectionRequest) returns (CollectionResponse);
    rpc CreateCollection (CreateCollectionRequest) returns (CollectionResponse);
    rpc UpdateCollection (UpdateCollectionRequest) returns (CollectionResponse);
    rpc DeleteCollection (DeleteCollectionRequest) returns (DeleteCollectionResponse);
    rpc AddRecipeToCollection (ModifyRecipeRequest) returns (ModifyRecipeResponse);
    rpc RemoveRecipeFromCollection (ModifyRecipeRequest) returns (ModifyRecipeResponse);
}

message Empty {}

message CollectionRequest {
    int32 id = 1;
}

message CreateCollectionRequest {
    string name = 1;
    string author = 2;
    string description = 3;
    repeated int32 recipes = 4;
}

message UpdateCollectionRequest {
    int32 id = 1;
    string author = 2;
    string name = 3;
    string description = 4;
    repeated int32 recipes = 5;
}

message DeleteCollectionRequest {
    int32 id = 1;
    string author = 2;
}

message ModifyRecipeRequest {
    int32 id = 1;
    int32 recipe_id = 2;
}

message CollectionResponse {
    int32 id = 1;
    string name = 2;
    string author = 3;
    string description = 4;
    repeated int32 recipes = 5;
}

message ListCollectionResponse {
    repeated CollectionResponse collections = 1;
}

message DeleteCollectionResponse {
    string status = 1;
}

message ModifyRecipeResponse {
    string status = 1;
}
```

### RabbitMQ Sender

Der Collection Service sendet Nachrichten über erstellte, aktualisierte und gelöschte Sammlungen.

#### Exchange: `collection_service_exchange`

**Methoden:**

- `publishEvent(method, body)`: Sendet eine Nachricht an den angegebenen Routing-Key.

**Parameter:**

- `method` (str): Der Routing-Key der Nachricht (`collection.created`, `collection.updated`, `collection.deleted`).
- `body` (dict): Der Inhalt der Nachricht.

**Beispiel:**

```python
publishEvent('collection.created', {
    "id": 1,
    "user": "Testuser",
    "title": "Neue Sammlung erstellt",
    "message": "Eine neue Sammlung wurde erstellt."
})
```

### Datenbank

Der Collection Service verwendet eine Datenbank zur Speicherung der Sammlungen und Rezepte.

#### Tabellen

##### collections

Speichert Informationen über die Sammlungen.

**Spalten:**

- `id` (int, Primary Key): Eindeutige ID der Sammlung.
- `name` (str): Name der Sammlung.
- `author` (str): Autor der Sammlung.
- `description` (str): Beschreibung der Sammlung.
- `recipes` (Array): Beinhaltete Rezepte.


