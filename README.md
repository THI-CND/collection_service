# Collection Service

## Übersicht

Der Collection Service verwaltet Sammlungen von Rezepten für Benutzer.

## Schnittstellen

### REST API

#### GET /collections

Ruft alle Sammlungen ab.

**Request:**
- Methode: GET
- URL: `/collections`

**Response:**
- Status: 200 OK
- Body: Eine Liste von Sammlungen.

**Beispiel:**
GET "http://localhost:8000/collections"

#### GET /collections/{id}

Ruft eine bestimmte Sammlung ab.

**Request:**
- Methode: GET
- URL: `/collections/{id}`

**Response:**
- Status: 200 OK
- Body: Die angeforderte Sammlung.

**Beispiel:**
GET "http://localhost:8000/collections/1"

#### POST /collections

Erstellt eine neue Sammlung.

**Request:**
- Methode: POST
- URL: `/collections`
- Body: JSON-Objekt mit den Daten der neuen Sammlung.

**Response:**
- Status: 200 OK
- Body: Die erstellte Sammlung.

**Beispiel:**
POST "http://localhost:8000/collections"
```json
{
    "name": "Neue Sammlung",
    "author": "testuser",
    "description": "Beschreibung der Sammlung",
    "recipes": [1, 2]
}
```

#### PUT /collections/{id}

Aktualisiert eine bestehende Sammlung.

**Request:**
- Methode: PUT
- URL: `/collections/{id}`
- Body: JSON-Objekt mit den aktualisierten Daten der Sammlung.

**Response:**
- Status: 200 OK
- Body: Die aktualisierte Sammlung.

**Beispiel:**
PUT "http://localhost:8000/collections/1"
```json
{
    "name": "Aktualisierte Sammlung",
    "author": "testuser",
    "description": "Aktualisierte Beschreibung",
    "recipes": [1, 2]
}
```

#### DELETE /collections/{id}

Löscht eine bestehende Sammlung.

**Request:**
- Methode: DELETE
- URL: `/collections/{id}`
- Body: JSON-Objekt mit den Daten des Autors.

**Response:**
- Status: 200 OK
- Body: Bestätigung der Löschung.

**Beispiel:**
DELETE "http://localhost:8000/collections/1"
```json
{
    "author": "testuser"
}
```

#### POST /collections/{id}/recipe

Fügt ein Rezept zu einer Sammlung hinzu.

**Request:**
- Methode: POST
- URL: `/collections/{id}/recipe`
- Body: JSON-Objekt mit der ID des Rezepts.

**Response:**
- Status: 200 OK
- Body: Die aktualisierte Sammlung.

**Beispiel:**
POST "http://localhost:8000/collections/1/recipe"
```json
{
    "recipe_id": 1
}
```

#### DELETE /collections/{id}/recipe

Entfernt ein Rezept aus einer Sammlung.

**Request:**
- Methode: DELETE
- URL: `/collections/{id}/recipe`
- Body: JSON-Objekt mit der ID des Rezepts.

**Response:**
- Status: 200 OK
- Body: Die aktualisierte Sammlung.

**Beispiel:**
DELETE "http://localhost:8000/collections/1/recipe"
```json
{
    "recipe_id": 1
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

Der Collection Service verwendet eine relationale Datenbank zur Speicherung der Sammlungen und Rezepte.

#### Tabellen

##### collections

Speichert Informationen über die Sammlungen.

**Spalten:**
- `id` (int, Primary Key): Eindeutige ID der Sammlung.
- `name` (str): Name der Sammlung.
- `author` (str): Autor der Sammlung.
- `description` (str): Beschreibung der Sammlung.

##### recipes

Speichert Informationen über die Rezepte.

**Spalten:**
- `id` (int, Primary Key): Eindeutige ID des Rezepts.
- `title` (str): Titel des Rezepts.
- `ingredients` (str): Zutaten des Rezepts.
- `instructions` (str): Anweisungen zur Zubereitung.

##### collection_recipes

Verknüpft Sammlungen mit Rezepten (Many-to-Many Beziehung).

**Spalten:**
- `collection_id` (int, Foreign Key): ID der Sammlung.
- `recipe_id` (int, Foreign Key): ID des Rezepts.