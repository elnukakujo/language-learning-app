import { getUserById } from "@/api/user";
import UserForm from "@/components/forms/entityForms/userForm"
import User from "@/interface/systemData/User";

export default async function UpdateUserPage({ params }: { params: { user_id: string } }) {
    const { user_id } = await params;
    const user: User = await getUserById(user_id);
    return (
        <main>
            <h1>Update User</h1>
            <UserForm user={user} />
        </main>
    );
}