export function formatBytes(bytes: number, decimals = 1): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(decimals))} ${sizes[i]}`
}

export function getMimeIcon(mimeType: string | null): string {
  if (!mimeType) return 'file'
  if (mimeType.startsWith('image/')) return 'image'
  if (mimeType.startsWith('video/')) return 'video'
  if (mimeType.startsWith('audio/')) return 'music'
  if (mimeType.includes('pdf')) return 'file-text'
  if (mimeType.includes('zip') || mimeType.includes('tar') || mimeType.includes('gz')) return 'archive'
  if (mimeType.includes('text/')) return 'file-text'
  if (mimeType.includes('javascript') || mimeType.includes('json') || mimeType.includes('python')) return 'code'
  return 'file'
}

export function truncate(str: string, n = 28): string {
  return str.length > n ? str.slice(0, n - 1) + '…' : str
}
