import { handleSignOut } from "@/lib/server/auth"
import { userAuthStore } from "@/stores/authStore"
import { useChatStore } from "@/stores/chatStore"
import { useTheme } from "next-themes"
import { usePathname } from "next/navigation"
import { toast } from "sonner"

export const Header = () => {
    const { setTheme } = useTheme()
    const { user, clearUser } = userAuthStore()
    const { setChat, showChatsList, setShowChatsList } = useChatStore()
    
    const pathname = usePathname()

    const handleLogOut = () => {
        handleSignOut()
        setChat(null)
        clearUser()
        toast.success('Deslogado com sucesso!', {position: "top-center"})
    }

    return (
        <header className="h-header">

        </header>
    )
}