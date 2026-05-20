import BackButton from "@/components/buttons/backButton";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <main>
        <header>
            <BackButton />
        </header>
        {children}
    </main>
  );
}