import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchTasks } from '../api'
import type { Task } from '../types'
import './TaskList.css'

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([])

  useEffect(() => {
    fetchTasks()
      .then(setTasks)
      .catch(() => alert('Failed to fetch tasks'))
  }, [])

  return (
    <section>
      <h2>📋 Your Tasks</h2>
      <ul className="task-list">
        {tasks.map(task => (
          <li key={task.id} className="task-card">
            <Link to={`/tasks/${task.id}`}>
              <h3>{task.title}</h3>
              <p>{task.description}</p>
              <p><strong>Due:</strong> {new Date(task.due_at).toLocaleString()}</p>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
