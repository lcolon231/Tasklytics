import { useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://api.tasklytics.dev'

export default function ResetPassword() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')

  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [message, setMessage] = useState<string | null>(null)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!token) {
      setMessage('Missing reset token.')
      return
    }

    if (newPassword !== confirmPassword) {
      setMessage("Passwords don't match.")
      return
    }

    try {
      const res = await fetch(`${BASE_URL}/auth/reset-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, new_password: newPassword }),
      })

      if (!res.ok) throw new Error(await res.text())
      setMessage('✅ Password reset successful! Redirecting to login…')
      setTimeout(() => navigate('/login'), 3000)
    } catch (err: any) {
      setMessage('❌ Reset failed: ' + err.message)
    }
  }

  return (
    <div className="form-card">
      <h2>Reset Your Password</h2>
      <form className="task-form" onSubmit={handleSubmit}>
        <label>New Password
          <input
            type="password"
            value={newPassword}
            onChange={e => setNewPassword(e.target.value)}
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

        <button type="submit">Reset Password</button>
      </form>
      {message && <p style={{ marginTop: '1rem', textAlign: 'center' }}>{message}</p>}
    </div>
  )
}
