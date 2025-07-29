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

export interface RegisterData {
  email: string
  password: string
}

// ✅ Base URL for production
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://api.tasklytics.dev'

// 🆕 Register user
export async function registerUser(data: RegisterData): Promise<any> {
  const res = await fetch(`${BASE_URL}/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

// Fetch all tasks
export async function fetchTasks(): Promise<Task[]> {
  const res = await fetch(`${BASE_URL}/tasks/`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

// Fetch a single task by ID
export async function getTask(id: number): Promise<Task> {
  const res = await fetch(`${BASE_URL}/tasks/${id}`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

// Delete a task by ID
export async function deleteTask(id: number): Promise<DeleteResponse> {
  const res = await fetch(`${BASE_URL}/tasks/${id}`, {
    method: 'DELETE',
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}
