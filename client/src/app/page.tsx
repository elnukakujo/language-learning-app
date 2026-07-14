import { getUserById } from "@/api/user";
import AvailableLanguages from "@/components/language/availableLanguages";
import NavButton from "@/components/layout/navButton";
import UserPicker from "@/components/user/userPicker";
import User from "@/interface/systemData/User";
import { getCurrentUserId } from "@/utils/user_cookie";

export default async function Home() {
  const userId = await getCurrentUserId();

  // No cookie -> show user picker
  if (!userId) {
    return (
      <main className="flex flex-col gap-6">
        <div>
          <h1>Fluence</h1>
          <p className="text-muted">Who is learning today?</p>
        </div>
        <UserPicker />
      </main>
    );
  }

  const user: User | null = await getUserById(userId);

  // If user not found, fallback to picker
  if (!user) {
    return (
      <main className="flex flex-col gap-6">
        <div>
          <h1>Fluence</h1>
          <p className="text-muted">Who is learning today?</p>
        </div>
        <UserPicker />
      </main>
    );
  }

  return (
    <main className="flex flex-col gap-8">
      <header className="flex flex-col gap-4">
        <h1>Fluence</h1>
        <h2>Hey {user.username}! What do you want to study today?</h2>
      </header>
      <AvailableLanguages />
      <NavButton path="/languages/new">
        <p>Create New Language</p>
      </NavButton>
    </main>
  );
}
