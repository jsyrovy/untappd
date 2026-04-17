import type { Beer, MenuResponse, Source } from "./schema";
import { parseBeerStreetJson } from "./parsers/beerstreet";
import { parseAmbasadaHtml } from "./parsers/ambasada";

const USER_AGENT = "tap-api/1.0";

async function fetchMenu(
  source: Source,
  url: string,
  parse: (response: Response) => Promise<Beer[]>,
): Promise<MenuResponse> {
  const response = await fetch(url, { headers: { "User-Agent": USER_AGENT } });
  if (!response.ok) {
    throw new Error(`${source} upstream returned ${response.status}`);
  }
  return {
    source,
    fetchedAt: new Date().toISOString(),
    beers: await parse(response),
  };
}

export const fetchBeerStreetMenu = (): Promise<MenuResponse> =>
  fetchMenu("beerstreet", "https://beerstreet.cz/data/beers.json", async (r) =>
    parseBeerStreetJson(await r.json()),
  );

export const fetchAmbasadaMenu = (): Promise<MenuResponse> =>
  fetchMenu("ambasada", "https://pivniambasada.cz/", parseAmbasadaHtml);
