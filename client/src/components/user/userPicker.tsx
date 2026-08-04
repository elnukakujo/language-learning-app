import { getAllUsers } from "@/api/user";
import User from "@/interface/systemData/User";
import UserCard from "@/components/user/userCard";
import NavButton from "@/components/layout/navButton";

export default async function UserPicker() {
    const users: User[] = await getAllUsers();
    return (
        <article className="flex flex-col gap-3">
            <div className="flex flex-row gap-3 flex-wrap">
                {users.map((user, idx) => (
                    <UserCard key={idx} user={user} useCookie />
                ))}
            </div>
            <NavButton path="/user/new">
                <p>Add User</p>
            </NavButton>
        </article>
    )
}