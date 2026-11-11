import type { ReactNode } from "react";

export const metadata = { title: "StudyHub" };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="uk">
      <body style={{ fontFamily: "system-ui, sans-serif", margin: 24 }}>{children}</body>
    </html>
  );
}
