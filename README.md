# Flask Superheroes API

A RESTful API for tracking superheroes and their superpowers.

**Author:** [Your Name]

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python seed.py
python app.py
```

The API runs on `http://localhost:5555`

## Endpoints

### GET /heroes
Returns all heroes.

```json
[
  {
    "id": 1,
    "name": "Kamala Khan",
    "super_name": "Ms. Marvel"
  }
]
```

### GET /heroes/:id
Returns a hero with their powers or 404 error.

```json
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "hero_powers": [
    {
      "hero_id": 1,
      "id": 1,
      "power": {
        "description": "gives the wielder the ability to fly through the skies at supersonic speed",
        "id": 2,
        "name": "flight"
      },
      "power_id": 2,
      "strength": "Strong"
    }
  ]
}
```

### GET /powers
Returns all powers.

```json
[
  {
    "description": "gives the wielder super-human strengths",
    "id": 1,
    "name": "super strength"
  }
]
```

### GET /powers/:id
Returns a power or 404 error.

### PATCH /powers/:id
Updates a power's description. Returns updated power or error.

Request:
```json
{
  "description": "Updated description with at least 20 characters"
}
```

### POST /hero_powers
Creates a hero-power association.

Request:
```json
{
  "strength": "Average",
  "power_id": 1,
  "hero_id": 3
}
```

Response:
```json
{
  "id": 11,
  "hero_id": 3,
  "power_id": 1,
  "strength": "Average",
  "hero": {
    "id": 3,
    "name": "Gwen Stacy",
    "super_name": "Spider-Gwen"
  },
  "power": {
    "description": "gives the wielder super-human strengths",
    "id": 1,
    "name": "super strength"
  }
}
```

## Validations

- Power description must be at least 20 characters
- HeroPower strength must be 'Strong', 'Weak', or 'Average'

## Testing

Import `challenge-2-superheroes.postman_collection.json` into Postman.

## Structure

```
superheroes-api/
├── app.py
├── models.py
├── seed.py
├── requirements.txt
└── README.md
```