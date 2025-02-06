/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_API_BASE_URL: string 
    readonly VITE_CODE_LIFESPAN: number
    readonly VITE_CODE_REQUEST_COOLDOWN: number
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}