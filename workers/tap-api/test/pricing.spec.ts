import { describe, it, expect } from "vitest";
import {
  ambasadaPricing,
  beerStreetPricing,
  extractTrailingVolume,
  halfLiterFrom,
} from "../src/pricing";

describe("halfLiterFrom", () => {
  it("converts 0,4 l price to 0,5 l equivalent", () => {
    expect(halfLiterFrom(100, 0.4)).toBe(125);
  });

  it("converts 0,3 l price to 0,5 l equivalent", () => {
    expect(halfLiterFrom(60, 0.3)).toBe(100);
  });

  it("returns same value for 0,5 l input", () => {
    expect(halfLiterFrom(55, 0.5)).toBe(55);
  });
});

describe("beerStreetPricing", () => {
  it("prefers cena04 when both are present", () => {
    expect(beerStreetPricing("100", "70")).toEqual({
      halfLiterCzk: 125,
      reference: { priceCzk: 100, volumeLiters: 0.4 },
      secondary: null,
    });
  });

  it("falls back to cena03 when cena04 is empty", () => {
    expect(beerStreetPricing("", "45")).toEqual({
      halfLiterCzk: 75,
      reference: { priceCzk: 45, volumeLiters: 0.3 },
      secondary: null,
    });
  });

  it("returns null when neither price is available", () => {
    expect(beerStreetPricing("", "")).toBeNull();
    expect(beerStreetPricing(null, undefined)).toBeNull();
    expect(beerStreetPricing("0", "0")).toBeNull();
  });

  it("accepts numeric inputs", () => {
    expect(beerStreetPricing(100, 0)).toEqual({
      halfLiterCzk: 125,
      reference: { priceCzk: 100, volumeLiters: 0.4 },
      secondary: null,
    });
  });
});

describe("ambasadaPricing", () => {
  it("parses pipe-separated 0,5 l | 0,3 l prices", () => {
    expect(ambasadaPricing("120|80", "Any description")).toEqual({
      halfLiterCzk: 120,
      reference: null,
      secondary: { priceCzk: 80, volumeLiters: 0.3 },
    });
  });

  it("rejects pipe format when one side is invalid", () => {
    expect(ambasadaPricing("120|abc", "d")).toBeNull();
  });

  it("converts single price using trailing volume in description", () => {
    expect(
      ambasadaPricing("60", "5,0% alc. piv. X, Stout 0,3 l"),
    ).toEqual({
      halfLiterCzk: 100,
      reference: { priceCzk: 60, volumeLiters: 0.3 },
      secondary: null,
    });
  });

  it("returns single price as half-liter when no volume in description", () => {
    expect(ambasadaPricing("55", "no volume info")).toEqual({
      halfLiterCzk: 55,
      reference: null,
      secondary: null,
    });
  });

  it("returns null for unparseable price", () => {
    expect(ambasadaPricing("", "")).toBeNull();
    expect(ambasadaPricing(null, "x")).toBeNull();
    expect(ambasadaPricing("abc", "x")).toBeNull();
    expect(ambasadaPricing("0", "x")).toBeNull();
  });
});

describe("extractTrailingVolume", () => {
  it("matches comma decimal", () => {
    expect(extractTrailingVolume("foo 0,3 l")).toBe(0.3);
  });

  it("matches dot decimal", () => {
    expect(extractTrailingVolume("foo 0.5 l")).toBe(0.5);
  });

  it("returns null when no trailing volume", () => {
    expect(extractTrailingVolume("no volume")).toBeNull();
    expect(extractTrailingVolume(null)).toBeNull();
  });
});
