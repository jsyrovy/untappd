const ALLOWED_ORIGINS = ["https://pivo.jsyrovy.cz"];
const ALLOWED_TARGETS = ["beerstreet.cz", "pivniambasada.cz"];

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Preflight (OPTIONS)
    if (request.method === "OPTIONS") {
      return handlePreflight(request);
    }

    if (request.method !== "GET") {
      return new Response("Method not allowed", { status: 405 });
    }

    // Origin check
    const origin = request.headers.get("Origin") || "";
    if (!ALLOWED_ORIGINS.includes(origin)) {
      return new Response("Forbidden", { status: 403 });
    }

    // Parse target URL
    const { searchParams } = new URL(request.url);
    const targetUrl = searchParams.get("url");
    if (!targetUrl) {
      return new Response("Missing ?url= parameter", { status: 400 });
    }

    // Validate target domain
    let parsed: URL;
    try {
      parsed = new URL(targetUrl);
    } catch {
      return new Response("Invalid URL", { status: 400 });
    }
    if (!ALLOWED_TARGETS.some((d) => parsed.hostname === d || parsed.hostname.endsWith("." + d))) {
      return new Response("Target domain not allowed", { status: 403 });
    }

    // Proxy the request
    const response = await fetch(targetUrl, {
      headers: { "User-Agent": "tap-api/1.0" },
    });

    // Return with CORS headers
    const headers = new Headers(response.headers);
    headers.set("Access-Control-Allow-Origin", origin);
    headers.set("Access-Control-Allow-Methods", "GET, OPTIONS");
    headers.set("Access-Control-Allow-Headers", "Content-Type");

    return new Response(response.body, {
      status: response.status,
      headers,
    });
  },
};

function handlePreflight(request: Request): Response {
  const origin = request.headers.get("Origin") || "";
  if (!ALLOWED_ORIGINS.includes(origin)) {
    return new Response("Forbidden", { status: 403 });
  }
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": origin,
      "Access-Control-Allow-Methods": "GET, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Max-Age": "86400",
    },
  });
}
