import { useState } from 'react'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://api.tasklytics.dev'

export default function ForgotPassword() {
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      const res = await fetch(`${BASE_URL}/auth/forgot-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      })

      if (!res.ok) throw new Error('Failed to send reset email')

      setMessage('If that email exists, a reset link has been sent.')
    } catch {
      setMessage('Something went wrong. Try again later.')
    }
  }

  return (
    <div className="form-card">
      <h2>Reset Password</h2>
      <form className="task-form" onSubmit={handleSubmit}>
        <label>Email Address
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </label>
        <button type="submit">Send Reset Link</button>
      </form>
      {message && <p style={{ marginTop: '1rem', textAlign: 'center' }}>{message}</p>}
    </div>
  )
}
