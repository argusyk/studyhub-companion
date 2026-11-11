import { describe, expect, it } from "vitest";
import { API_URL } from "./api";

describe("api", () => {
  it("uses the /api/v1 prefix by default", () => {
    expect(API_URL.endsWith("/api/v1")).toBe(true);
  });
});
