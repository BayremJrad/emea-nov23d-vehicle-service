"""Data models and in-memory store for the Vehicle Service API.

The vehicle schema is derived from the Vehicle Service - API Contract spec
and the Vehicle Service Collection examples:

    id       integer   (server-assigned)
    nickName string
    vin      string    (unique identifier for a vehicle)
    make     string
    model    string
    year     string
    miles    integer
"""

from threading import Lock

# Fields a client may supply when creating/updating a vehicle.
WRITABLE_FIELDS = ("nickName", "vin", "make", "model", "year", "miles")

# Fields that are required when creating a vehicle.
REQUIRED_FIELDS = ("vin", "make", "model", "year")


class VehicleStore:
    """A simple thread-safe, in-memory vehicle store.

    This stands in for a real database so the API can be run and tested
    without external dependencies.
    """

    def __init__(self):
        self._vehicles = {}
        self._next_id = 1
        self._lock = Lock()
        self._seed()

    def _seed(self):
        """Seed one vehicle so GET endpoints return data out of the box."""
        self.create(
            {
                "nickName": "The Lisa Marie",
                "vin": "4M2DV11W4RDJ53329",
                "make": "Mercury",
                "model": "Villager",
                "year": "1994",
                "miles": 159864,
            }
        )

    def list(self):
        with self._lock:
            return [dict(v) for v in self._vehicles.values()]

    def get(self, vehicle_id):
        with self._lock:
            vehicle = self._vehicles.get(vehicle_id)
            return dict(vehicle) if vehicle else None

    def find_by_vin(self, vin):
        with self._lock:
            for vehicle in self._vehicles.values():
                if vehicle.get("vin") == vin:
                    return dict(vehicle)
        return None

    def create(self, data):
        with self._lock:
            vehicle_id = self._next_id
            self._next_id += 1
            vehicle = {"id": vehicle_id}
            for field in WRITABLE_FIELDS:
                if field in data:
                    vehicle[field] = data[field]
            self._vehicles[vehicle_id] = vehicle
            return dict(vehicle)

    def update(self, vehicle_id, data):
        with self._lock:
            vehicle = self._vehicles.get(vehicle_id)
            if not vehicle:
                return None
            for field in WRITABLE_FIELDS:
                if field in data:
                    vehicle[field] = data[field]
            return dict(vehicle)

    def delete(self, vehicle_id):
        with self._lock:
            return self._vehicles.pop(vehicle_id, None) is not None


# Module-level singleton used by the app.
store = VehicleStore()
