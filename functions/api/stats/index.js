import { PLACES, categories } from "../../_data.js";

export async function onRequestGet({ env }) {
  if (!env.DB) {
    const average = PLACES.reduce((sum, place) => sum + place.rating, 0) / PLACES.length;
    return Response.json({
      totalPlaces: PLACES.length,
      averageRating: Math.round(average * 10) / 10,
      categories: categories()
    }, {
      headers: {
        "Cache-Control": "public, max-age=60"
      }
    });
  }

  const { results: categories } = await env.DB.prepare(`
    SELECT category, COUNT(*) AS count
    FROM places
    GROUP BY category
    ORDER BY category
  `).all();

  const total = await env.DB.prepare("SELECT COUNT(*) AS count FROM places").first();
  const average = await env.DB.prepare("SELECT ROUND(AVG(rating), 1) AS rating FROM places").first();

  return Response.json({
    totalPlaces: total.count,
    averageRating: average.rating,
    categories
  }, {
    headers: {
      "Cache-Control": "public, max-age=60"
    }
  });
}
