import React, { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'

export default function ResetPassword() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token') || ''
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [message, setMessage] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    if (!token) {
      setMessage('Missing or invalid reset token.')
    }
  }, [token])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (password !== confirmPassword) {
      setMessage("Passwords don't match")
      return
    }

    try {
      const res = await fetch('http://localhost:8000/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, new_password: password }),
      })

      if (!res.ok) throw new Error('Failed to reset password')

      setMessage('✅ Password reset successful! Redirecting to login...')
      setTimeout(() => navigate('/login'), 2500)
    } catch {
      setMessage('❌ Failed to reset password. Try again or request a new link.')
    }
  }

  return (
    <div className="form-card">
      <h2>Reset Password</h2>
      {message && <p style={{ textAlign: 'center', marginBottom: '1rem' }}>{message}</p>}
      {!message?.startsWith('✅') && (
        <form className="task-form" onSubmit={handleSubmit}>
          <label>New Password
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </label>

          <label>Confirm Password
            <input
              type="password"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              required
            />
          </label>

          <button type="submit">Update Password</button>
        </form>
      )}
    </div>
  )
}
