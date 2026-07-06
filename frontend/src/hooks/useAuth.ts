import { useMutation } from '@tanstack/react-query'
import api from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import type { User, TokenResponse } from '@/types'
import toast from 'react-hot-toast'
import { useNavigate } from 'react-router-dom'

export const useLogin = () => {
  const { setAuth } = useAuthStore()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: async ({ email, password }: { email: string; password: string }) => {
      const { data: tokens } = await api.post<TokenResponse>('/auth/login', { email, password })
      return tokens
    },
    onSuccess: async (tokens) => {
      localStorage.setItem('access_token', tokens.access_token)
      const { data: user } = await api.get<User>('/auth/me')
      setAuth(user, tokens.access_token, tokens.refresh_token)
      navigate('/drive')
    },
    onError: (e: any) => {
      toast.error(e.response?.data?.detail || 'Login failed')
    },
  })
}

export const useRegister = () => {
  const navigate = useNavigate()

  return useMutation({
    mutationFn: async (payload: { email: string; username: string; password: string }) => {
      const { data } = await api.post('/auth/register', payload)
      return data
    },
    onSuccess: () => {
      toast.success('Account created — please log in')
      navigate('/login')
    },
    onError: (e: any) => {
      toast.error(e.response?.data?.detail || 'Registration failed')
    },
  })
}

export const useLogout = () => {
  const { logout } = useAuthStore()
  const navigate = useNavigate()

  return () => {
    logout()
    navigate('/login')
    toast.success('Logged out')
  }
}
