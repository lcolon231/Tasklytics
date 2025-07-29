import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './TaskForm.css'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://api.tasklytics.dev'

interface TaskFormData {
  title: string
  description: string
  dueAtLocal: string
  userEmail: string
}

export const TaskForm: React.FC = () => {
  const [form, setForm] = useState<TaskFormData>({
    title: '',
    description: '',
    dueAtLocal: '',
    userEmail: '',
  })
  const navigate = useNavigate()

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const due_at = new Date(form.dueAtLocal).toISOString()

    try {
      const res = await fetch(`${BASE_URL}/tasks/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: form.title,
          description: form.description,
          due_at,
          user_email: form.userEmail,
        }),
      })
      if (!res.ok) throw new Error(await res.text())
      navigate('/')
    } catch (err) {
      console.error(err)
      alert('Error creating task')
    }
  }

  return (
    <div className="task-form-card">
      <h2 className="form-title">✏️ Create New Task</h2>
      <form onSubmit={handleSubmit} className="task-form">
        <div className="form-field">
          <label htmlFor="title">Title</label>
          <input
            id="title"
            name="title"
            value={form.title}
            onChange={handleChange}
            placeholder="Brief task title"
            required
          />
        </div>

        <div className="form-field">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={form.description}
            onChange={handleChange}
            placeholder="Optional details…"
            rows={4}
          />
        </div>

        <div className="form-row">
          <div className="form-field">
            <label htmlFor="dueAtLocal">Due date &amp; time</label>
            <input
              id="dueAtLocal"
              type="datetime-local"
              name="dueAtLocal"
              value={form.dueAtLocal}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-field">
            <label htmlFor="userEmail">Your Email</label>
            <input
              id="userEmail"
              type="email"
              name="userEmail"
              value={form.userEmail}
              onChange={handleChange}
              placeholder="you@example.com"
              required
            />
          </div>
        </div>

        <button type="submit" className="btn submit-btn">
          ➕ Add Task
        </button>
      </form>
    </div>
  )
}
