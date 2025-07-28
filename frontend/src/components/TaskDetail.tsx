import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getTask, deleteTask } from '../api'
import type { Task } from '../types'
import './TaskDetail.css'

export function TaskDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [task, setTask] = useState<Task | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    getTask(Number(id))
      .then(setTask)
      .catch(() => setError('Failed to load task.'))
  }, [id])

  const handleDelete = async () => {
    if (!task) return
    const confirmed = window.confirm('Are you sure you want to delete this task?')
    if (!confirmed) return

    try {
      await deleteTask(task.id)
      navigate('/')
    } catch (err) {
      console.error('Failed to delete task:', err)
      alert('Task could not be deleted. It may have already been removed.')
    }
  }

  if (error) return <p className="task-error">{error}</p>
  if (!task) return <p>Loading...</p>

  return (
    <section className="task-detail">
      <h2>{task.title}</h2>
      <p>{task.description}</p>
      <p><strong>Due:</strong> {new Date(task.due_at).toLocaleString()}</p>
      <p><strong>Email:</strong> {task.user_email}</p>
      <button onClick={handleDelete}>Delete Task</button>
    </section>
  )
}
