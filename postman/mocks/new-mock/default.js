pm.mockRequest(async (req, res) => {
  const vehicles = pm.state.get('vehicles') || {};
  const nextId = pm.state.get('nextId') || 1;

  const method = req.method;
  const pathParts = req.path.split('/').filter(Boolean);
  const vehicleId = pathParts[1] ? parseInt(pathParts[1]) : null;

  // @endpoint POST /vehicles
  if (method === 'POST' && !vehicleId) {
    const body = JSON.parse(req.body.raw);
    const newVehicle = { id: nextId, ...body };
    vehicles[nextId] = newVehicle;
    pm.state.set('vehicles', vehicles);
    pm.state.set('nextId', nextId + 1);
    res.status = 201;
    res.headers.set('Content-Type', 'application/json');
    res.body = JSON.stringify(newVehicle);

  // @endpoint GET /vehicles
  } else if (method === 'GET' && !vehicleId) {
    res.status = 200;
    res.headers.set('Content-Type', 'application/json');
    res.body = JSON.stringify(Object.values(vehicles));

  // @endpoint GET /vehicles/:id
  } else if (method === 'GET' && vehicleId) {
    const vehicle = vehicles[vehicleId];
    if (vehicle) {
      res.status = 200;
      res.headers.set('Content-Type', 'application/json');
      res.body = JSON.stringify(vehicle);
    } else {
      res.status = 404;
      res.headers.set('Content-Type', 'application/json');
      res.body = JSON.stringify({ error: 'Vehicle not found', id: vehicleId });
    }

  // @endpoint PATCH /vehicles/:id
  } else if (method === 'PATCH' && vehicleId) {
    const vehicle = vehicles[vehicleId];
    if (vehicle) {
      const body = JSON.parse(req.body.raw);
      const updated = { ...vehicle, ...body, id: vehicleId };
      vehicles[vehicleId] = updated;
      pm.state.set('vehicles', vehicles);
      res.status = 200;
      res.headers.set('Content-Type', 'application/json');
      res.body = JSON.stringify(updated);
    } else {
      res.status = 404;
      res.headers.set('Content-Type', 'application/json');
      res.body = JSON.stringify({ error: 'Vehicle not found', id: vehicleId });
    }

  // @endpoint DELETE /vehicles/:id
  } else if (method === 'DELETE' && vehicleId) {
    const vehicle = vehicles[vehicleId];
    if (vehicle) {
      delete vehicles[vehicleId];
      pm.state.set('vehicles', vehicles);
      res.status = 204;
      res.body = '';
    } else {
      res.status = 404;
      res.headers.set('Content-Type', 'application/json');
      res.body = JSON.stringify({ error: 'Vehicle not found', id: vehicleId });
    }

  } else {
    res.status = 405;
    res.headers.set('Content-Type', 'application/json');
    res.body = JSON.stringify({ error: 'Method not allowed' });
  }
});