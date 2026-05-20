import { getUserById } from "@/api/user";
import AvailableLanguages from "@/components/availableLanguages";
import NavButton from "@/components/buttons/navButton";
import SwitchUserButton from "@/components/buttons/switchUserButton";
import UserPicker from "@/components/userPicker";
import User from "@/interface/systemData/User";
import { getCurrentUserId } from "@/utils/user_cookie";

export default async function Home() {
    const userId = await getCurrentUserId()

    // No cookie → show user picker
    if (!userId) {
      return (
        <main>
          <h1>Language Learning App</h1>
          <p>Who is learning today?</p>
          <UserPicker />
        </main>
      )
    }

    const user: User = await getUserById(userId);
    return (
        <main className="flex flex-col gap-8">
            <header className="flex flex-col gap-4">
                <h1>Language Learning App</h1>
                <h2>Hey {user.username}! What do you want to learn today?</h2>
                <nav className="flex flex-row gap-2">
                    <SwitchUserButton/>
                    <NavButton path={`/user/${userId}/update`}>
                        <p>Modify User</p>
                    </NavButton>
                    <NavButton path="/tags">
                        <p>View All Tags</p>
                    </NavButton>
                    <NavButton path="/sources">
                        <p>View All Sources</p>
                    </NavButton>
                </nav>
            </header>
            <AvailableLanguages />
            <NavButton path="/languages/new">
                <p>Create New Language</p>
            </NavButton>
        </main>
    );
}
