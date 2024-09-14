import { z } from "zod";

/* New Chat */
export const NewChatSchema = z.object({
    email: z.string().email({ message: "Email inválido" })
})

export type NewChatData = z.infer<typeof NewChatSchema>