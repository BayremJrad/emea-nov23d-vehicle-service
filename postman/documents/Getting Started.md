# Getting Started with the Vehicle Service API

Welcome to the **Vehicle Service Collection**! This guide will walk you through everything you need to know to start sending successful requests — from setting up authorization to making your first API call.

---

## Overview

The Vehicle Service API lets you manage a registry of vehicles. You can create, retrieve, update, and delete vehicle records. All endpoints are organized under a single base URL and secured with an API key.

---

## Prerequisites

Before you begin, make sure you have:

- Access to the **Vehicle Service** Postman workspace
- Your **API key** (provided by your team or API administrator)
- The **base URL** for the environment you are targeting (e.g. development, staging, or production)

---

## Step 1 — Set Up Your Environment

All requests in this collection use a variable called `{{baseUrl}}` to define the server address. You need to set this variable before sending any requests.

1. In Postman, click the **Environments** tab in the left sidebar.
2. Select the environment linked to this workspace, or create a new one.
3. Add a variable named `baseUrl` and set its value to the server URL you want to target, for example:
   ```
   https://api.vehicleservice.example.com
   ```
4. Make sure the environment is selected (active) in the top-right environment dropdown before sending requests.

---

## Step 2 — Configure Authorization

The Vehicle Service API uses an **API key** for authentication. Your API key is stored securely in the **Postman Vault** under the key `vault:apiKey`.

### What is the Postman Vault?

The Postman Vault is a secure, local secret store built into Postman. It keeps sensitive values like API keys off the network and out of shared environments, so your credentials are never accidentally exposed to teammates or version control.

### How to add your API key to the Vault

1. Click the **Vault** icon (🔒) in the Postman footer bar at the bottom of the app.
2. Find the entry named `apiKey`.
3. Enter your API key as the value and save it.

The collection is already configured to read `vault:apiKey` automatically — you do not need to add the key to any request header manually.

---

## Step 3 — Send Your First Request

Once your environment and vault are set up, you are ready to send requests. A great place to start is **Get all vehicles**, which returns a list of all vehicles in the registry.

1. Open the **Vehicle Service Collection** in the left sidebar.
2. Click on **Get all vehicles**.
3. Confirm the correct environment is selected in the top-right dropdown.
4. Click **Send**.

A successful response will return a `200 OK` status with a JSON array of vehicle objects.

---

## Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/vehicles` | Retrieve a list of all vehicles |
| `GET` | `/vehicles/:id` | Retrieve a single vehicle by its ID |
| `POST` | `/vehicles` | Create a new vehicle record |
| `PATCH` | `/vehicles/:id` | Update an existing vehicle record |
| `DELETE` | `/vehicles/:id` | Delete a vehicle record |

---

## Creating a Vehicle

To create a new vehicle, use the **Create a vehicle** request. The request body must be JSON and include the following fields:

```json
{
  "nickName": "The Lisa Marie",
  "vin": "4M2DV11W4RDJ53329",
  "make": "Mercury",
  "model": "Villager",
  "year": "1994",
  "miles": 159864
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `nickName` | string | Yes | A friendly name for the vehicle |
| `vin` | string | Yes | The Vehicle Identification Number (must be unique) |
| `make` | string | Yes | The manufacturer (e.g. Ford, Toyota) |
| `model` | string | Yes | The model name |
| `year` | string | Yes | The model year |
| `miles` | number | Yes | Current mileage on the vehicle |

A successful creation returns a `201 Created` response.

---

## Common Response Codes

| Status Code | Meaning |
|-------------|---------|
| `200 OK` | Request succeeded, data returned |
| `201 Created` | New vehicle successfully created |
| `204 No Content` | Vehicle successfully deleted |
| `400 Bad Request` | Missing or invalid fields in the request body |
| `404 Not Found` | No vehicle found with the given ID |
| `409 Conflict` | A vehicle with that VIN already exists |
| `500 Internal Server Error` | Unexpected server-side error |

---

## Tips for Success

- **Always select an environment** before sending requests. If `{{baseUrl}}` is not resolved, requests will fail.
- **Check your Vault** if you receive `401 Unauthorized` errors — your API key may not be set.
- **Use the saved examples** on each request to preview expected responses before sending live requests. Click on any request and look for the **Examples** section.
- **Use the Mock Server** (`Vehicle Service Mock`) to test requests without hitting a live backend.

---

## Need Help?

If you run into issues, check that:
1. Your `baseUrl` environment variable is set and the correct environment is active.
2. Your `vault:apiKey` value is populated in the Postman Vault.
3. The VIN you are using for `POST /vehicles` is unique (not already in the system).

---