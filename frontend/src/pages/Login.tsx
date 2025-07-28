import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { saveToken } from '../utils/auth'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const form = new URLSearchParams()
    form.append('username', email)
    form.append('password', password)

    try {
      const res = await fetch('http://localhost:8000/auth/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: form.toString(),
      })

      if (!res.ok) throw new Error('Login failed')

      const data = await res.json()
      saveToken(data.access_token)
      navigate('/home')
    } catch (err) {
      alert('Invalid login credentials')
    }
  }

  return (
    <div className="form-card">
      <h2>Login</h2>
      <form className="task-form" onSubmit={handleSubmit}>
        <label>Email
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </label>

        <label>Password
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </label>

        <button type="submit">Log In</button>

        <div style={{ marginTop: '1rem', textAlign: 'center' }}>
          <Link to="/forgot-password">Forgot your password?</Link>
        </div>
      </form>
    </div>
  )
}
