import { describe, expect, it } from "vitest";
import { daysLeft, formatDeadline } from "./deadline";

describe("deadline", () => {
  it("formats in Kyiv time (summer, UTC+3)", () => {
    expect(formatDeadline("2026-04-19T20:59:00Z")).toBe("19.04.2026 23:59");
  });
  it("formats in Kyiv time (winter, UTC+2)", () => {
    expect(formatDeadline("2026-02-22T21:59:00Z")).toBe("22.02.2026 23:59");
  });
  it("counts whole days left", () => {
    expect(daysLeft("2026-04-19T20:59:00Z", new Date("2026-04-16T20:59:00Z"))).toBe(3);
    expect(daysLeft("2026-04-19T20:59:00Z", new Date("2026-04-20T20:59:00Z"))).toBe(-1);
  });
});
