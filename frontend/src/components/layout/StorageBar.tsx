import { useStorageStats } from '@/hooks/useFiles'
import { formatBytes } from '@/lib/utils'

export default function StorageBar() {
  const { data } = useStorageStats()

  if (!data) return null

  const pct = Math.min(data.used_percent, 100)
  const color = pct > 90 ? 'bg-red-500' : pct > 70 ? 'bg-amber-400' : 'bg-gold'

  return (
    <div className="px-4 py-3 border-t border-slate/20">
      <div className="flex justify-between text-xs text-mist mb-1.5">
        <span>{formatBytes(data.used_bytes)} used</span>
        <span>{formatBytes(data.limit_bytes)}</span>
      </div>
      <div className="h-1.5 bg-void rounded-full overflow-hidden">
        <div
          className={`h-full ${color} rounded-full transition-all duration-500`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <p className="text-xs text-mist/60 mt-1.5">
        {data.file_count} files · {data.folder_count} folders
      </p>
    </div>
  )
}
