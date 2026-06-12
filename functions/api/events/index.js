import { EVENTS } from "../../_data.js";

export async function onRequestGet({ env }) {
  if (!env.DB) {
    return Response.json(EVENTS, {
      headers: {
        "Cache-Control": "public, max-age=60"
      }
    });
  }

  const { results } = await env.DB.prepare("SELECT * FROM events ORDER BY id ASC").all();
  return Response.json(results, {
    headers: {
      "Cache-Control": "public, max-age=60"
    }
  });
}
