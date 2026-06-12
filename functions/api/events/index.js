export async function onRequestGet({ env }) {
  const { results } = await env.DB.prepare("SELECT * FROM events ORDER BY id ASC").all();
  return Response.json(results, {
    headers: {
      "Cache-Control": "public, max-age=60"
    }
  });
}
