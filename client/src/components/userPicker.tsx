import { getAllUsers } from "@/api/user";
import User from "@/interface/systemData/User";
import UserCard from "./cards/userCard";
import NavButton from "./buttons/navButton";

export default async function UserPicker() {
    const users: User[] = await getAllUsers();
    return (
        <article>
            {users.map((user, idx) => (
                <UserCard key={idx} user={user} useCookie />
            ))}
            <NavButton path="/user/new">
                <p>Add User</p>
            </NavButton>
        </article>
    )
}