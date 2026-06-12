function json(data, status = 200) {
  return Response.json(data, {
    status,
    headers: {
      "Cache-Control": "public, max-age=60"
    }
  });
}

export async function onRequestGet({ params, env }) {
  const placeId = Number(params.id);

  if (!Number.isInteger(placeId) || placeId <= 0) {
    return json({ error: "Invalid place id" }, 400);
  }

  const place = await env.DB.prepare("SELECT * FROM places WHERE id = ?")
    .bind(placeId)
    .first();

  if (!place) {
    return json({ error: "Place not found" }, 404);
  }

  const { results: related } = await env.DB.prepare(`
    SELECT id, name, category, area, rating, image
    FROM places
    WHERE id != ? AND (category = ? OR area = ?)
    ORDER BY rating DESC, name ASC
    LIMIT 3
  `).bind(place.id, place.category, place.area).all();

  return json({ place, related });
}
