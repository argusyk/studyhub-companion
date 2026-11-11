import type { ReactNode } from "react";
import "../styles/tokens.css";

export const metadata = { title: "StudyHub" };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="uk">
      <body style={{ padding: "var(--sh-space-3)" }}>{children}</body>
    </html>
  );
}
