# Collection Service

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=THI-CND_collection_service&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=THI-CND_collection_service)

## Übersicht

Der **Collection Service** bietet eine zentrale Verwaltung für Rezept-Sammlungen, die Benutzern die Erstellung, Bearbeitung und Organisation ihrer Sammlungen ermöglicht. Er unterstützt sowohl REST- als auch gRPC-Schnittstellen und integriert RabbitMQ als Message Broker zur Ereignisbenachrichtigung. Eine PostgreSQL-Datenbank dient als Datenspeicher.

## Installation und Start

### Voraussetzungen

Um den Collection Service auszuführen sind folgende Tools erforderlich:

- **Python 3.11**: Zum lokalen Entwickeln und Testen des Codes
- **Docker**: Für Containerisierung.
- **Docker Compose**: Für die Orchestrierung mehrerer Container.

### Manuelle Installation und Start

1. **Repository klonen**  
   Klone das Repository in das gewünschte Verzeichnis und navigiere in den Ordner:

   ```bash
   git clone https://github.com/THI-CND/collection_service.git

   cd collection_service
   ```

2. **Abhängigkeiten installieren**  
   Installiere die benötigten Abhängigkeiten:

   ```bash
   pip install -r requirements.txt
   ```

3. **Django Secret Key generieren**  
   Generiere einen **Django Secret Key**:

   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

   Kopiere den generierten Schlüssel und nutze den folgenden Befehl im Verzeichnis des Projekts, um eine **.env**-Datei im Projektverzeichnis zu erstellen und den generierten Schlüssel hinzuzufügen:

   ```bash
   echo "SECRET_KEY_DJANGO=your-secret-key" > .env
   ```

4. **Migrationen durchführen**  
   Führe die Datenbankmigrationen durch:

   ```bash
   python manage.py migrate
   ```

5. **Standarddaten laden (optional)**  
   Lade Standarddaten, falls erforderlich:

   ```bash
   python manage.py loaddata default_database.json
   ```

6. **Service starten**  
   Starte die Django REST- und gRPC-Server:

   ```bash
   python manage.py startcollectionservice
   ```

### Starten mit Docker

1.  **Repository klonen**  
     Klone das Repository in das gewünschte Verzeichnis und navigiere in den Ordner:

    ```bash
    git clone https://github.com/THI-CND/collection_service.git

    cd collection_service
    ```

2.  **Django Secret Key generieren**  
    Generiere einen **Django Secret Key**:

    ```bash
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```

    Kopiere den generierten Schlüssel und füge ihn in die Umgebungsvariable `SECRET_KEY_DJANGO` in der [docker-compose.yml](https://github.com/THI-CND/collection_service/blob/next/docker-compose.yml)-Datei ein.

3.  **Docker Compose starten**  
    Stelle sicher, dass Docker installiert und betriebsbereit ist. Navigiere in den Projektordner und starte alle notwendigen Dienste mit dem Befehl:

    ```bash
    docker-compose up
    ```

    Dies startet:

    - **PostgreSQL**: Die Datenbank für den Collection Service.
    - **RabbitMQ**: Für die Nachrichtenvermittlung und Ereignisverarbeitung.
    - **Collection Service**: Der Hauptdienst.

4.  **Überprüfen des Service**  
    Nach dem Start sind die APIs verfügbar unter:
    - **REST API**: Port 8000
    - **gRPC**: Port 50051

### Umgebungsvariablen

Die folgenden Umgebungsvariablen werden zur Konfiguration des Dienstes verwendet:

- `SECRET_KEY_DJANGO`: Der Secret-Key für Django.
- `DJANGO_SETTINGS_MODULE`: Das Einstellungsmodul für Django.
- `DB_NAME`: Der Name der Datenbank.
- `DB_USER`: Der Datenbankbenutzer.
- `DB_PASSWORD`: Das Datenbankpasswort.
- `DB_HOST`: Der Datenbankhost.
- `DB_PORT`: Der Datenbankport.
- `RABBITMQ_USER`: Der RabbitMQ-Benutzer.
- `RABBITMQ_PASSWORD`: Das RabbitMQ-Passwort.
- `RABBITMQ_HOST`: Der RabbitMQ-Host.
- `RABBITMQ_PORT`: Der RabbitMQ-Port.
- `RABBITMQ_EXCHANGE`: Der RabbitMQ-Exchange.
- `RABBITMQ_ROUTING_KEYS_COLLECTION`: Die RabbitMQ-Routing-Keys für Sammlungen.
- `GRPC_HOST_RECIPE_SERVICE`: Der gRPC-Host für den Rezeptdienst (nur für Get-collection-tags-request; wenn der Rezeptdienst nicht verfügbar ist, läuft alles andere weiter (soft fail)).
- `GRPC_PORT_RECIPE_SERVICE`: Der gRPC-Port für den Rezeptdienst.

Für das Modul `DJANGO_SETTINGS_MODULE` können die Parameter `config.settings.development` (Entwicklungsprofil und als Standard hinterlegt), `config.settings.production` (Für Produktionsumgebung) und `config.settings.test` (Für Testausführung mit einer sqlite3-Datenbank) verwendet werden.

## Schnittstellen

### REST API

#### V1

#### GET /api/v1/collections/

Ruft alle Sammlungen ab.

**Request:**

- Methode: GET
- URL: `/api/v1/collections/`

**Response:**

- Status: 200 OK
- Body: Eine Liste von Sammlungen.

**Beispiel:**
GET "http://localhost:8000/api/v1/collections/"

#### GET /api/v1/collections/{id}/

Ruft eine bestimmte Sammlung ab.

**Request:**

- Methode: GET
- URL: `/api/v1/collections/{id}/`

**Response:**

- Status: 200 OK
- Body: Die angeforderte Sammlung.

**Beispiel:**
GET "http://localhost:8000/api/v1/collections/1/"

#### POST /api/v1/collections/

Erstellt eine neue Sammlung.

**Request:**

- Methode: POST
- URL: `/api/v1/collections/`
- Body: JSON-Objekt mit den Daten der neuen Sammlung.

**Response:**

- Status: 201 OK
- Body: Die erstellte Sammlung.

**Beispiel:**
POST "http://localhost:8000/api/v1/collections/"

```json
{
  "name": "Neue Sammlung",
  "author": "testuser",
  "description": "Beschreibung der Sammlung",
  "recipes": ["1", "2"]
}
```

#### PUT /api/v1/collections/{id}/

Aktualisiert eine bestehende Sammlung.

**Request:**

- Methode: PUT
- URL: `/api/v1/collections/{id}/`
- Body: JSON-Objekt mit den aktualisierten Daten der Sammlung.

**Response:**

- Status: 200 OK
- Body: Die aktualisierte Sammlung.

**Beispiel:**
PUT "http://localhost:8000/api/v1/collections/1/"

```json
{
  "name": "Aktualisierte Sammlung",
  "author": "testuser",
  "description": "Aktualisierte Beschreibung",
  "recipes": ["1", "2"]
}
```

#### DELETE /api/v1/collections/{id}/

Löscht eine bestehende Sammlung.

**Request:**

- Methode: DELETE
- URL: `/api/v1/collections/{id}/`
- Body: JSON-Objekt mit den Daten des Autors.

**Response:**

- Status: 200 OK
- Body: Bestätigung der Löschung.

**Beispiel:**
DELETE "http://localhost:8000/api/v1/collections/1/"

```json
{
  "author": "testuser"
}
```

#### V2

#### POST /api/v2/collections/{id}/recipe/

Fügt ein Rezept zu einer Sammlung hinzu.

**Request:**

- Methode: POST
- URL: `/api/v2/collections/{id}/recipe/`
- Body: JSON-Objekt mit der ID des Rezepts.

**Response:**

- Status: 200 OK
- Body: Die aktualisierte Sammlung.

**Beispiel:**
POST "http://localhost:8000/api/v2/collections/1/recipe/"

```json
{
  "recipe_id": "1"
}
```

#### DELETE /api/v2/collections/{id}/recipe/

Entfernt ein Rezept aus einer Sammlung.

**Request:**

- Methode: DELETE
- URL: `/api/v2/collections/{id}/recipe/`
- Body: JSON-Objekt mit der ID des Rezepts.

**Response:**

- Status: 200 OK
- Body: Die aktualisierte Sammlung.

**Beispiel:**
DELETE "http://localhost:8000/api/v2/collections/1/recipe/"

```json
{
  "recipe_id": "1"
}
```

#### GET /api/v2/collections/{id}/tags/

Holt die Tags einer Sammlung.

**Logik:**

`intersection`: Tags, die in allen Rezepten der Sammlung vorkommen.

`union`: Alle Tags, die in mindestens einem Rezept der Sammlung vorkommen.

**Request:**

- Methode: GET
- URL: `/api/v2/collections/{id}/tags/`

**Response:**

- Status: 200 OK
- Body: Die Tags der Sammlung, aufgeteilt in `intersection` und `union`.

**Beispiel:**
GET "http://localhost:8000/api/v2/collections/1/tags/"

```json
{
  "intersection": ["tag1", "tag2"],
  "union": ["tag1", "tag2", "tag3", "tag4"]
}
```

### gRPC API

```python
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
    repeated string recipes = 4;
}

message UpdateCollectionRequest {
    int32 id = 1;
    string author = 2;
    string name = 3;
    string description = 4;
    repeated string recipes = 5;
}

message DeleteCollectionRequest {
    int32 id = 1;
    string author = 2;
}

message ModifyRecipeRequest {
    int32 id = 1;
    string recipe_id = 2;
}

message CollectionResponse {
    int32 id = 1;
    string name = 2;
    string author = 3;
    string description = 4;
    repeated string recipes = 5;
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

## RabbitMQ Events

### `collection.created`

Wird ausgelöst, wenn eine Sammlung erstellt wird.

### `collection.updated`

Wird ausgelöst, wenn eine Sammlung aktualisiert wird.

### `collection.deleted`

Wird ausgelöst, wenn eine Sammlung gelöscht wird.

### Payload für alle Events:

```json
{
  "id": 1,
  "name": "Neue Sammlung",
  "author": "testuser",
  "description": "Beschreibung der Sammlung",
  "recipes": [1, 2]
}
```

## Datenmodell Collections

Zur Speicherung der Sammlungen wird folgendes Modell verwendet:

| Spalte      | Typ   | Beschreibung               |
| ----------- | ----- | -------------------------- |
| id          | int   | Eindeutige ID der Sammlung |
| name        | str   | Name der Sammlung          |
| author      | str   | Autor der Sammlung         |
| description | str   | Beschreibung der Sammlung  |
| recipes     | array | Beinhaltete Rezept-IDs     |
