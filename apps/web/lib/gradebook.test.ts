import { describe, expect, it } from "vitest";
import { average, formatScore, lateBadge } from "@studyhub/shared";

describe("gradebook (характеризаційні тести перенесеного JS)", () => {
  it("average keeps legacy denominator including nulls", () => {
    expect(average([80, null, 100])).toBe(60);
    expect(average([])).toBe(0);
  });
  it("lateBadge", () => {
    expect(lateBadge(0)).toBe("");
    expect(lateBadge(2)).toBe("Запізно на 2 д.");
    expect(lateBadge(6)).toBe("Не приймається");
  });
  it("formatScore", () => {
    expect(formatScore(null)).toBe("–");
    expect(formatScore(76)).toBe("76");
  });
});
