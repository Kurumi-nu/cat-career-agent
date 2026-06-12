import { PLACES } from "../../_data.js";

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

  if (!env.DB) {
    const filtered = PLACES
      .filter((place) => category === "all" || place.category === category)
      .filter((place) => {
        if (!query) return true;
        const q = query.toLowerCase();
        return [place.name, place.area, place.tag, place.description]
          .some((value) => value.toLowerCase().includes(q));
      })
      .sort((a, b) => b.rating - a.rating || a.name.localeCompare(b.name, "ja"));
    return json(filtered);
  }

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
