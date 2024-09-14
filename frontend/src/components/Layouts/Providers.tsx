'use client'

import { ThemeProvider } from "next-themes"
import { Toaster } from "@/components/ui/sonner"
import { useEffect } from "react"
import daysjs from "dayjs"
import { io } from "socket.io-client"
import { AppProgressBar as ProgressBar} from "next-nprogress-bar"
import 'dayjs/esm/locale/pt-br'


export const socket = io(process.env.NEXT_PUBLIC_API_BASE_URL as string)

export const Providers = ({children}: {children: React.ReactNode }) => {
    useEffect(() => {
        daysjs.locale('pt-br')
    }, [])

    return (
        <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
        >
            {children}

            <ProgressBar 
                height="4px"
                color="#493cdd"
                shallowRouting
            />

            <Toaster />
        </ThemeProvider>


    )
}