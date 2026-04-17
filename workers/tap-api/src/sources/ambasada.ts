import type { MenuResponse } from "../schema";
import { parseAmbasadaHtml } from "../parsers/ambasada";

const UPSTREAM_URL = "https://pivniambasada.cz/";

export async function fetchAmbasadaMenu(): Promise<MenuResponse> {
  const response = await fetch(UPSTREAM_URL, {
    headers: { "User-Agent": "tap-api/1.0" },
  });
  if (!response.ok) {
    throw new Error(`Ambasada upstream returned ${response.status}`);
  }
  return {
    source: "ambasada",
    fetchedAt: new Date().toISOString(),
    beers: await parseAmbasadaHtml(response),
  };
}
