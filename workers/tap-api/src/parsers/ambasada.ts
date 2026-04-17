import type { Beer } from "../schema";
import { ambasadaPricing } from "../pricing";

interface PendingRow {
  name?: string;
  priceRaw?: string;
  description?: string;
}

export async function parseAmbasadaHtml(response: Response): Promise<Beer[]> {
  const beers: Beer[] = [];
  let tableEnded = false;
  let pending: PendingRow = {};

  let nazevBuf = "";
  let cenaBuf = "";
  let popisBuf = "";
  let inNazev = false;
  let inCena = false;
  let inPopis = false;

  const rewriter = new HTMLRewriter()
    .on("table.listek_tab td.listek_tab_nadpis", {
      element() {
        tableEnded = true;
      },
    })
    .on("table.listek_tab td.listek_tab_nazev", {
      element(el) {
        if (tableEnded) return;
        nazevBuf = "";
        inNazev = true;
        el.onEndTag(() => {
          pending.name = nazevBuf.trim();
          inNazev = false;
        });
      },
      text(t) {
        if (inNazev) nazevBuf += t.text;
      },
    })
    .on("table.listek_tab td.listek_tab_cena", {
      element(el) {
        if (tableEnded) return;
        cenaBuf = "";
        inCena = true;
        el.onEndTag(() => {
          pending.priceRaw = cenaBuf.trim();
          inCena = false;
        });
      },
      text(t) {
        if (inCena) cenaBuf += t.text;
      },
    })
    .on("table.listek_tab td.listek_tab_popis", {
      element(el) {
        if (tableEnded) return;
        popisBuf = "";
        inPopis = true;
        el.onEndTag(() => {
          inPopis = false;
          if (!pending.name) return;
          pending.description = popisBuf.trim();
          const beer = buildBeer(pending, beers.length + 1);
          if (beer) beers.push(beer);
          pending = {};
        });
      },
      text(t) {
        if (inPopis) popisBuf += t.text;
      },
    });

  await rewriter.transform(response).text();
  return beers;
}

function buildBeer(row: PendingRow, order: number): Beer | null {
  const rawName = row.name ?? "";
  if (!rawName) return null;

  const degreeMatch = rawName.match(/^(\d+)°\s*/);
  const degreePlato = degreeMatch ? Number.parseInt(degreeMatch[1], 10) : null;
  const name = degreeMatch ? rawName.slice(degreeMatch[0].length).trim() : rawName;

  const { abv, brewery, style } = parseDescription(row.description ?? "");
  const pricing = ambasadaPricing(row.priceRaw ?? null, row.description ?? null);

  return {
    name,
    brewery,
    style,
    abv,
    degreePlato,
    source: "ambasada",
    order,
    pricing,
  };
}

export function parseDescription(raw: string): {
  abv: number | null;
  brewery: string;
  style: string;
} {
  let desc = raw.trim();
  if (!desc) return { abv: null, brewery: "", style: "" };

  let abv: number | null = null;
  const abvMatch = desc.match(/^([\d,.]+)\s*%\s*alc\.\s*/i);
  if (abvMatch) {
    const n = Number.parseFloat(abvMatch[1].replace(",", "."));
    abv = Number.isFinite(n) ? n : null;
    desc = desc.slice(abvMatch[0].length);
  }

  if (desc.startsWith("piv. ")) desc = desc.slice(5);

  const parts = desc.split(",").map((p) => p.trim()).filter((p) => p.length > 0);
  if (parts.length === 0) return { abv, brewery: "", style: "" };

  const totalLen = desc.length;
  const last = parts[parts.length - 1];

  if (parts.length > 1 && last.length <= 40 && totalLen <= 120) {
    return {
      abv,
      brewery: parts.slice(0, -1).join(", "),
      style: last,
    };
  }
  if (totalLen > 120) {
    return {
      abv,
      brewery: parts.slice(0, 2).join(", "),
      style: "",
    };
  }
  return { abv, brewery: desc, style: "" };
}
