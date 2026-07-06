export type FileType = 'file' | 'folder'
export type StorageProvider = 'local' | 's3' | 'r2' | 'minio'

export interface User {
  id: string
  email: string
  username: string
  is_active: boolean
  storage_used_bytes: number
  storage_limit_bytes: number
  created_at: string
}

export interface FileItem {
  id: string
  name: string
  original_name: string
  path: string
  mime_type: string | null
  size_bytes: number
  file_type: FileType
  storage_provider: StorageProvider
  is_public: boolean
  share_token: string | null
  share_expires_at: string | null
  parent_id: string | null
  created_at: string
  updated_at: string
}

export interface StorageStats {
  used_bytes: number
  limit_bytes: number
  used_percent: number
  file_count: number
  folder_count: number
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface ShareLinkOut {
  share_token: string
  share_url: string
  expires_at: string | null
}
