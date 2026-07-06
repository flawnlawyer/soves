import { NavLink } from 'react-router-dom'
import { HardDrive, Share2, Settings, LogOut, Folder } from 'lucide-react'
import { useLogout } from '@/hooks/useAuth'
import { useAuthStore } from '@/store/auth'
import StorageBar from './StorageBar'

const nav = [
  { to: '/drive', icon: HardDrive, label: 'My Drive' },
  { to: '/shared', icon: Share2, label: 'Shared' },
  { to: '/settings', icon: Settings, label: 'Settings' },
]

export default function Sidebar() {
  const logout = useLogout()
  const user = useAuthStore((s) => s.user)

  return (
    <aside className="w-56 bg-abyss border-r border-slate/20 flex flex-col h-screen sticky top-0">
      {/* Brand */}
      <div className="px-5 py-6 border-b border-slate/20">
        <h1 className="font-display text-2xl text-gold tracking-widest">SŌVĒS</h1>
        <p className="text-mist/60 text-xs mt-0.5 tracking-wider">LET DATA FLY</p>
      </div>

      {/* Nav */}
      <nav className="flex-1 p-3 space-y-0.5">
        {nav.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-150
               ${isActive
                ? 'bg-slate/30 text-gold font-medium'
                : 'text-mist hover:text-frost hover:bg-slate/10'
              }`
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* User + storage */}
      <div>
        <StorageBar />
        <div className="px-4 py-3 flex items-center justify-between border-t border-slate/20">
          <div className="flex items-center gap-2 min-w-0">
            <div className="w-7 h-7 rounded-full bg-slate/40 flex items-center justify-center flex-shrink-0">
              <span className="text-gold text-xs font-semibold uppercase">
                {user?.username?.[0] ?? '?'}
              </span>
            </div>
            <span className="text-frost text-xs truncate">{user?.username}</span>
          </div>
          <button
            onClick={logout}
            className="text-mist hover:text-frost transition-colors p-1 rounded"
            title="Sign out"
          >
            <LogOut size={14} />
          </button>
        </div>
      </div>
    </aside>
  )
}
