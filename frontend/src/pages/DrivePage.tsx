import { useState } from 'react'
import { ChevronRight, FolderPlus, Home } from 'lucide-react'
import { useFiles, useCreateFolder } from '@/hooks/useFiles'
import FileCard from '@/components/files/FileCard'
import Dropzone from '@/components/files/Dropzone'

interface BreadcrumbItem {
  id: string | null
  name: string
}

export default function DrivePage() {
  const [breadcrumbs, setBreadcrumbs] = useState<BreadcrumbItem[]>([{ id: null, name: 'My Drive' }])
  const [newFolderMode, setNewFolderMode] = useState(false)
  const [newFolderName, setNewFolderName] = useState('')

  const currentFolder = breadcrumbs[breadcrumbs.length - 1]
  const { data: files, isLoading } = useFiles(currentFolder.id)
  const createFolder = useCreateFolder()

  const enterFolder = (id: string, name: string) => {
    setBreadcrumbs((b) => [...b, { id, name }])
  }

  const navigateTo = (index: number) => {
    setBreadcrumbs((b) => b.slice(0, index + 1))
  }

  const submitNewFolder = (e: React.FormEvent) => {
    e.preventDefault()
    if (!newFolderName.trim()) return
    createFolder.mutate({ name: newFolderName.trim(), parentId: currentFolder.id ?? undefined })
    setNewFolderName('')
    setNewFolderMode(false)
  }

  return (
    <div className="flex-1 min-h-screen p-6 max-w-5xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          {/* Breadcrumb */}
          <nav className="flex items-center gap-1 text-sm mb-1">
            {breadcrumbs.map((crumb, i) => (
              <span key={i} className="flex items-center gap-1">
                {i > 0 && <ChevronRight size={12} className="text-mist/40" />}
                <button
                  onClick={() => navigateTo(i)}
                  className={`transition-colors ${
                    i === breadcrumbs.length - 1
                      ? 'text-frost font-medium cursor-default'
                      : 'text-mist hover:text-gold'
                  }`}
                >
                  {i === 0 ? <Home size={14} className="inline" /> : crumb.name}
                </button>
              </span>
            ))}
          </nav>
          <h1 className="text-2xl font-semibold text-frost">{currentFolder.name}</h1>
        </div>

        <button
          onClick={() => setNewFolderMode(true)}
          className="btn-ghost flex items-center gap-2 text-sm"
        >
          <FolderPlus size={16} />
          New folder
        </button>
      </div>

      {/* New folder input */}
      {newFolderMode && (
        <form onSubmit={submitNewFolder} className="mb-4 flex gap-2 animate-slide-up">
          <input
            className="input max-w-xs"
            placeholder="Folder name"
            value={newFolderName}
            onChange={(e) => setNewFolderName(e.target.value)}
            autoFocus
          />
          <button type="submit" className="btn-primary text-sm px-4">Create</button>
          <button
            type="button"
            className="btn-ghost text-sm"
            onClick={() => { setNewFolderMode(false); setNewFolderName('') }}
          >
            Cancel
          </button>
        </form>
      )}

      {/* Upload zone */}
      <div className="mb-6">
        <Dropzone parentId={currentFolder.id ?? undefined} />
      </div>

      {/* File grid */}
      {isLoading ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="card p-4 h-28 animate-pulse" />
          ))}
        </div>
      ) : !files?.length ? (
        <div className="text-center py-16">
          <p className="text-mist text-sm">This folder is empty</p>
          <p className="text-mist/50 text-xs mt-1">Drop files above to upload</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
          {files.map((item) => (
            <FileCard key={item.id} item={item} onEnterFolder={enterFolder} />
          ))}
        </div>
      )}
    </div>
  )
}
