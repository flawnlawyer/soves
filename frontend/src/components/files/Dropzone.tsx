import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload } from 'lucide-react'
import { useUploadFile } from '@/hooks/useFiles'
import { clsx } from 'clsx'

interface Props {
  parentId?: string
}

export default function Dropzone({ parentId }: Props) {
  const upload = useUploadFile()

  const onDrop = useCallback(
    (accepted: File[]) => {
      accepted.forEach((file) => upload.mutate({ file, parentId }))
    },
    [upload, parentId]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: true,
  })

  return (
    <div
      {...getRootProps()}
      className={clsx(
        'border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200',
        isDragActive
          ? 'border-gold bg-gold/5 scale-[1.01]'
          : 'border-slate/30 hover:border-slate/50 hover:bg-slate/5'
      )}
    >
      <input {...getInputProps()} />
      <Upload
        size={28}
        className={clsx('mx-auto mb-3 transition-colors', isDragActive ? 'text-gold' : 'text-mist')}
      />
      <p className="text-frost text-sm font-medium">
        {isDragActive ? 'Drop to upload' : 'Drop files here'}
      </p>
      <p className="text-mist/60 text-xs mt-1">or click to browse</p>

      {upload.isPending && (
        <div className="mt-4 flex items-center justify-center gap-2 text-gold text-sm">
          <span className="animate-spin inline-block w-4 h-4 border-2 border-gold border-t-transparent rounded-full" />
          Uploading…
        </div>
      )}
    </div>
  )
}
