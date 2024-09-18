import { getChats } from "@/lib/requests"
import { userAuthStore } from "@/stores/authStore"
import { useChatStore } from "@/stores/chatStore"
import { Chat, UpdateChatEvent } from "@/types/Chat"
import { useEffect, useState } from "react"
import { toast } from "sonner"
import { socket } from "../Providers"

type Props = {
    variant?: "mobile" | "desktop"
}

export const LeftSide = () => {
    const { chat: currentChat, chats, setChats, setChat, setShowNewChat } = useChatStore()
    const { user } = userAuthStore()

    const [queryInput, setQueryInput] = useState('')
    const [chatsFiltered, setChatsFiltered] = useState<Chat[]>([])

    const handleGetChats = async () => {
        const response = await getChats()

        if(response.data){
            setChats(response.data.chats)
        }
    }

    const handleFilterChats = () => {
        if(!chats) return

        setChatsFiltered(chats.filter(chats => chats.user.name.toLowerCase()
            .includes(queryInput.toLowerCase())))
    }

    useEffect(() => {
        handleGetChats()
    }, [])

    useEffect(() => {
        if(!queryInput && chats) setChatsFiltered(chats)
    }, [chats])

    useEffect(() => {
        const handleUpdateChat = (data: UpdateChatEvent) => {
            if(user && data.query.users.includes(user.id)){
                handleGetChats()
            }

            if(data.type === "delete" && data.query.chat_id === currentChat?.id){
                setChat(null)
                toast.info('A conversa foi deletada', {position: "top-center"})
            }
        }

        socket.on('update_chat', handleUpdateChat)

        return () => {
            socket.off('update_chat', handleUpdateChat)
        }
    }, [currentChat])

    return (
        <div className={`bg-slate-100 dark:bg-slate-900 border-r border-slate-50 dark:border-slate-800 ${variant === "mobile"}`}>
            
        </div>
    )
}