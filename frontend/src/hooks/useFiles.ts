import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import type { FileItem, StorageStats } from '@/types'
import toast from 'react-hot-toast'

export const useFiles = (parentId?: string | null) =>
  useQuery<FileItem[]>({
    queryKey: ['files', parentId ?? 'root'],
    queryFn: async () => {
      const params = parentId ? { parent_id: parentId } : {}
      const { data } = await api.get('/files/', { params })
      return data
    },
  })

export const useStorageStats = () =>
  useQuery<StorageStats>({
    queryKey: ['storage-stats'],
    queryFn: async () => {
      const { data } = await api.get('/files/stats')
      return data
    },
    refetchInterval: 30_000,
  })

export const useUploadFile = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async ({ file, parentId }: { file: File; parentId?: string }) => {
      const form = new FormData()
      form.append('file', file)
      if (parentId) form.append('parent_id', parentId)
      const { data } = await api.post('/files/upload', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      return data as FileItem
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['files'] })
      qc.invalidateQueries({ queryKey: ['storage-stats'] })
      toast.success('File uploaded')
    },
    onError: (e: any) => {
      toast.error(e.response?.data?.detail || 'Upload failed')
    },
  })
}

export const useCreateFolder = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async ({ name, parentId }: { name: string; parentId?: string }) => {
      const { data } = await api.post('/files/folder', { name, parent_id: parentId })
      return data as FileItem
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['files'] })
      toast.success('Folder created')
    },
    onError: () => toast.error('Failed to create folder'),
  })
}

export const useDeleteFile = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/files/${id}`)
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['files'] })
      qc.invalidateQueries({ queryKey: ['storage-stats'] })
      toast.success('Deleted')
    },
    onError: () => toast.error('Delete failed'),
  })
}

export const useShareFile = () =>
  useMutation({
    mutationFn: async ({ id, expiresInHours }: { id: string; expiresInHours?: number }) => {
      const { data } = await api.post(`/files/${id}/share`, {
        is_public: true,
        expires_in_hours: expiresInHours,
      })
      return data
    },
    onSuccess: (data) => {
      const url = `${window.location.origin}${data.share_url}`
      navigator.clipboard.writeText(url)
      toast.success('Share link copied!')
    },
    onError: () => toast.error('Share failed'),
  })
