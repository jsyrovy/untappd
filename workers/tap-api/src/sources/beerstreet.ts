import type { MenuResponse } from "../schema";
import { parseBeerStreetJson } from "../parsers/beerstreet";

const UPSTREAM_URL = "https://beerstreet.cz/data/beers.json";

export async function fetchBeerStreetMenu(): Promise<MenuResponse> {
  const response = await fetch(UPSTREAM_URL, {
    headers: { "User-Agent": "tap-api/1.0" },
  });
  if (!response.ok) {
    throw new Error(`Beer Street upstream returned ${response.status}`);
  }
  const payload = await response.json();
  return {
    source: "beerstreet",
    fetchedAt: new Date().toISOString(),
    beers: parseBeerStreetJson(payload),
  };
}
