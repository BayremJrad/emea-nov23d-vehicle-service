# Vehicle Service API — Python implementation

A Flask implementation of the Vehicle Service API, built from the
**Vehicle Service - API Contract** spec and the **Vehicle Service Collection**
in `postman/`.

## Endpoints

| Method | Path | Description | Success | Errors |
|--------|------|-------------|---------|--------|
| `POST` | `/vehicles` | Create a vehicle | `201` | `400`, `409`, `500` |
| `GET` | `/vehicles` | List all vehicles | `200` | `500` |
| `GET` | `/vehicles/<id>` | Retrieve a vehicle | `200` | `404`, `500` |
| `PATCH` | `/vehicles/<id>` | Update a vehicle | `200` | `400`, `404`, `500` |
| `DELETE` | `/vehicles/<id>` | Delete a vehicle | `204` | `404`, `500` |

## Vehicle schema

```json
{
  "id": 1,
  "nickName": "The Lisa Marie",
  "vin": "4M2DV11W4RDJ53329",
  "make": "Mercury",
  "model": "Villager",
  "year": "1994",
  "miles": 159864
}
```

## Authentication

Every request (except `/health`) must send an API key in the `X-API-Key`
header, matching the collection's API Key auth. The key is read from the
`API_KEY` environment variable and defaults to `local-dev-key` for local
development. **Do not commit real keys** — in Postman the key is stored in the
Vault (`vault:apiKey`).

## Run it

```bash
pip install -r requirements.txt
API_KEY=local-dev-key PORT=3000 python -m app.main
```

Point the Postman `baseUrl` environment variable at `http://localhost:3000`
and set the vault `apiKey` to `local-dev-key` to run the collection against it.

## Test it

```bash
pytest -q
```

The tests in `tests/test_vehicles.py` mirror the collection's contract tests.

> **Note:** vehicles are stored in memory, so data resets on restart. Swap the
> `VehicleStore` in `app/models.py` for a real database when you need
> persistence.
