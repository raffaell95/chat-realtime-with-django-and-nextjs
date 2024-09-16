import { Chat } from "@/types/Chat"
import { Message } from "postcss"
import { create } from "zustand"

export type ChatState = {
    showNewChat: boolean,
    chats: Chat[] | null,
    chat: Chat | null,
    chatMessages: Message[] | null,
    loading: boolean,
    showChatsList: boolean
}

export type ChatActions = {
    setShowNewChat: (show: boolean) => void,
    setShowChatsList: (show: boolean) => void,
    setChat: (chat: Chat | null) => void,
    setChatMessages: (messages: Message[] | null) => void,
    setChats: (chats: Chat[] | null) => void,
    setLoading: (loading: boolean) => void
}

export type ChatStore = ChatState & ChatActions

export const useChatStore = create<ChatStore>((set, get) => ({
    showNewChat: false,
    chats: null,
    chat: null,
    chatMessages: null,
    loading: false,
    showChatsList: false,
    setShowNewChat: (show) => set({showNewChat: show}),
}))