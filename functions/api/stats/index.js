export async function onRequestGet({ env }) {
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
