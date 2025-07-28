import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './TaskForm.css'

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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const due_at = new Date(form.dueAtLocal).toISOString()

    try {
      const res = await fetch('http://127.0.0.1:8000/tasks/', {
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
    <section className="form-card">
      <h2>Create a New Task</h2>
      <form onSubmit={handleSubmit} className="task-form">
        <label>
          Title
          <input type="text" name="title" value={form.title} onChange={handleChange} required />
        </label>

        <label>
          Description
          <textarea name="description" value={form.description} onChange={handleChange} />
        </label>

        <label>
          Due Date & Time
          <input type="datetime-local" name="dueAtLocal" value={form.dueAtLocal} onChange={handleChange} required />
        </label>

        <label>
          Email
          <input type="email" name="userEmail" value={form.userEmail} onChange={handleChange} required />
        </label>

        <button type="submit">Add Task</button>
      </form>
    </section>
  )
}
