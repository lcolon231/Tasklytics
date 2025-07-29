import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { registerUser } from '../api'

export default function Signup() {
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [age, setAge] = useState<number | ''>('')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (password !== confirmPassword) {
      alert("Passwords do not match")
      return
    }

    const payload = {
      first_name: firstName,
      last_name: lastName,
      email,
      password,
      age: Number(age),
    }

    try {
      await registerUser(payload)
      alert('Account created! You can now log in.')
      navigate('/login')
    } catch (err: any) {
      alert('Signup failed: ' + err.message)
      console.error(err)
    }
  }

  return (
    <div className="form-card">
      <h2>Sign Up</h2>
      <form className="task-form" onSubmit={handleSubmit}>
        <label>First Name
          <input type="text" value={firstName} onChange={e => setFirstName(e.target.value)} required />
        </label>

        <label>Last Name
          <input type="text" value={lastName} onChange={e => setLastName(e.target.value)} required />
        </label>

        <label>Email
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        </label>

        <label>Password
          <div style={{ position: 'relative' }}>
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword(prev => !prev)}
              style={{
                position: 'absolute',
                right: '10px',
                top: '50%',
                transform: 'translateY(-50%)',
                background: 'none',
                border: 'none',
                color: '#4f46e5',
                cursor: 'pointer',
                fontSize: '0.875rem',
              }}
            >
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>
        </label>

        <label>Confirm Password
          <div style={{ position: 'relative' }}>
            <input
              type={showConfirm ? 'text' : 'password'}
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              required
            />
            <button
              type="button"
              onClick={() => setShowConfirm(prev => !prev)}
              style={{
                position: 'absolute',
                right: '10px',
                top: '50%',
                transform: 'translateY(-50%)',
                background: 'none',
                border: 'none',
                color: '#4f46e5',
                cursor: 'pointer',
                fontSize: '0.875rem',
              }}
            >
              {showConfirm ? 'Hide' : 'Show'}
            </button>
          </div>
        </label>

        <label>Age
          <input
            type="number"
            value={age}
            onChange={e => setAge(e.target.value === '' ? '' : Number(e.target.value))}
            required
          />
        </label>

        <button type="submit">Create Account</button>
      </form>
    </div>
  )
}
