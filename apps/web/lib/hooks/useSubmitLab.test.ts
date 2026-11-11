import { describe, expect, it } from "vitest";
import { validateFile } from "./useSubmitLab";

describe("validateFile", () => {
  it("rejects missing and empty files", () => {
    expect(validateFile(null)).not.toBeNull();
    expect(validateFile(new File([], "a.pdf"))).not.toBeNull();
  });
  it("accepts a small file", () => {
    expect(validateFile(new File(["x"], "a.pdf"))).toBeNull();
  });
});
