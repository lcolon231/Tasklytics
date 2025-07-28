// src/api.ts

export interface Task {
  id: number
  title: string
  description: string
  due_at: string
  user_email: string
  reminded: boolean
  created: string
}

export interface DeleteResponse {
  detail: string
}

// Fetch all tasks
export async function fetchTasks(): Promise<Task[]> {
  const res = await fetch('http://localhost:8000/tasks/')
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

// Fetch a single task by ID
export async function getTask(id: number): Promise<Task> {
  const res = await fetch(`http://localhost:8000/tasks/${id}`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

// Delete a task by ID
export async function deleteTask(id: number): Promise<DeleteResponse> {
  const res = await fetch(`http://localhost:8000/tasks/${id}`, {
    method: 'DELETE',
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}
