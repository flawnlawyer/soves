import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useRegister } from '@/hooks/useAuth'

export default function RegisterPage() {
  const register = useRegister()
  const [form, setForm] = useState({ email: '', username: '', password: '' })

  const update = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }))

  const submit = (e: React.FormEvent) => {
    e.preventDefault()
    register.mutate(form)
  }

  return (
    <div className="min-h-screen bg-void flex items-center justify-center px-4">
      <div className="w-full max-w-sm animate-fade-in">
        <div className="text-center mb-10">
          <h1 className="font-display text-4xl text-gold tracking-widest">SŌVĒS</h1>
          <p className="text-mist text-sm mt-1 tracking-wider">LET DATA FLY</p>
        </div>

        <div className="card p-8">
          <h2 className="text-frost font-semibold text-xl mb-6">Create account</h2>

          <form onSubmit={submit} className="space-y-4">
            <div>
              <label className="label">Email</label>
              <input
                className="input"
                type="email"
                placeholder="you@example.com"
                value={form.email}
                onChange={update('email')}
                required
                autoFocus
              />
            </div>

            <div>
              <label className="label">Username</label>
              <input
                className="input"
                type="text"
                placeholder="yourname"
                value={form.username}
                onChange={update('username')}
                required
                minLength={3}
                maxLength={32}
              />
            </div>

            <div>
              <label className="label">Password</label>
              <input
                className="input"
                type="password"
                placeholder="min 8 characters"
                value={form.password}
                onChange={update('password')}
                required
                minLength={8}
              />
            </div>

            <button
              type="submit"
              className="btn-primary w-full mt-2"
              disabled={register.isPending}
            >
              {register.isPending ? 'Creating…' : 'Create account'}
            </button>
          </form>

          <p className="text-mist text-sm text-center mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-gold hover:text-gold-light transition-colors">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
