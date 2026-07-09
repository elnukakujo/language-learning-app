import UserForm from "@/components/user/userForm"

export default function NewUserPage() {
    return (
        <main className="flex flex-col gap-4">
            <h1>New User</h1>
            <UserForm />
        </main>
    );
}