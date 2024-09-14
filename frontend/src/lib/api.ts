"use server"

import { APIError } from "@/types/Api"
import axios, {AxiosError } from "axios"
import { cookies } from "next/headers"


type Props = {
    endpoint: string,
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE',
    data?: object,
    withAuth?: boolean,
    withAttachment?: boolean
}

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL + '/api/v1'

export const api = async ({ }) => {
    
}
