function json(data, status = 200) {
  return Response.json(data, {
    status,
    headers: {
      "Cache-Control": "public, max-age=60"
    }
  });
}

export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const category = url.searchParams.get("category") || "all";
  const query = (url.searchParams.get("q") || "").trim();

  let sql = "SELECT * FROM places WHERE 1 = 1";
  const params = [];

  if (category !== "all") {
    sql += " AND category = ?";
    params.push(category);
  }

  if (query) {
    sql += " AND (name LIKE ? OR area LIKE ? OR tag LIKE ? OR description LIKE ?)";
    const like = `%${query}%`;
    params.push(like, like, like, like);
  }

  sql += " ORDER BY rating DESC, name ASC";

  const { results } = await env.DB.prepare(sql).bind(...params).all();
  return json(results);
}
