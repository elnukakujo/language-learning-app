import { getUserById } from "@/api/user";
import ProfileSection from "@/components/user/profileSection";
import PasswordSection from "@/components/user/passwordSection";
import PreferencesSection from "@/components/user/preferencesSection";
import ApiEndpointsSection from "@/components/user/apiEndpointsSection";
import BackupSection from "@/components/user/backupSection";

export default async function UpdateUserPage({ params }: { params: Promise<{ user_id: string }> }) {
    const { user_id } = await params;
    const user = await getUserById(user_id);
    const preferences = user.preferences ?? {};

    return (
        <main className="flex flex-col gap-4 max-w-2xl mx-auto">
            <h1>Settings</h1>
            <ProfileSection user={user} />
            <PasswordSection userId={user.id} />
            <PreferencesSection preferences={preferences} />
            <ApiEndpointsSection
                prefId={preferences.id}
                endpoints={preferences.ai_endpoints ?? []}
            />
            <BackupSection />
        </main>
    );
}
