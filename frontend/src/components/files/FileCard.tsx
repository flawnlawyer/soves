import {
  File, Folder, Image, Video, Music, FileText, Code, Archive,
  Download, Share2, Trash2, MoreVertical
} from 'lucide-react'
import { useState, useRef, useEffect } from 'react'
import type { FileItem } from '@/types'
import { formatBytes, getMimeIcon, truncate } from '@/lib/utils'
import { useDeleteFile, useShareFile } from '@/hooks/useFiles'
import api from '@/lib/api'

const ICON_MAP: Record<string, React.ElementType> = {
  image: Image, video: Video, music: Music, 'file-text': FileText,
  code: Code, archive: Archive, file: File,
}

interface Props {
  item: FileItem
  onEnterFolder?: (id: string, name: string) => void
}

export default function FileCard({ item, onEnterFolder }: Props) {
  const [menu, setMenu] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)
  const del = useDeleteFile()
  const share = useShareFile()

  const Icon = item.file_type === 'folder' ? Folder : (ICON_MAP[getMimeIcon(item.mime_type)] ?? File)
  const isFolder = item.file_type === 'folder'

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) setMenu(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const handleDownload = async () => {
    const res = await api.get(`/files/${item.id}/download`, { responseType: 'blob' })
    const url = URL.createObjectURL(res.data)
    const a = document.createElement('a')
    a.href = url
    a.download = item.original_name
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div
      className={`card p-4 group relative cursor-pointer select-none
                  hover:border-slate/40 hover:bg-abyss/80 transition-all duration-150 animate-fade-in`}
      onDoubleClick={() => isFolder && onEnterFolder?.(item.id, item.name)}
    >
      {/* Icon */}
      <div className={`w-10 h-10 rounded-lg flex items-center justify-center mb-3
                       ${isFolder ? 'bg-gold/10 text-gold' : 'bg-slate/20 text-mist'}`}>
        <Icon size={20} />
      </div>

      {/* Name */}
      <p className="text-frost text-sm font-medium leading-tight" title={item.name}>
        {truncate(item.name)}
      </p>

      {/* Meta */}
      <p className="text-mist/60 text-xs mt-1">
        {isFolder ? 'Folder' : formatBytes(item.size_bytes)}
      </p>

      {/* Context menu button */}
      <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity" ref={menuRef}>
        <button
          onClick={(e) => { e.stopPropagation(); setMenu((m) => !m) }}
          className="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-slate/30 text-mist hover:text-frost transition-all"
        >
          <MoreVertical size={14} />
        </button>

        {menu && (
          <div className="absolute right-0 top-8 z-20 w-44 bg-abyss border border-slate/30 rounded-xl shadow-xl overflow-hidden animate-fade-in">
            {!isFolder && (
              <button
                onClick={() => { handleDownload(); setMenu(false) }}
                className="flex items-center gap-2.5 w-full px-4 py-2.5 text-sm text-mist hover:text-frost hover:bg-slate/20 transition-colors"
              >
                <Download size={13} /> Download
              </button>
            )}
            <button
              onClick={() => { share.mutate({ id: item.id }); setMenu(false) }}
              className="flex items-center gap-2.5 w-full px-4 py-2.5 text-sm text-mist hover:text-frost hover:bg-slate/20 transition-colors"
            >
              <Share2 size={13} /> Share
            </button>
            <div className="border-t border-slate/20 mt-1" />
            <button
              onClick={() => { del.mutate(item.id); setMenu(false) }}
              className="flex items-center gap-2.5 w-full px-4 py-2.5 text-sm text-red-400 hover:text-red-300 hover:bg-red-900/20 transition-colors"
            >
              <Trash2 size={13} /> Delete
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
