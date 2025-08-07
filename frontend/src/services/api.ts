// API base URL
const API_BASE_URL = 'http://localhost:8000';

// Helper function for making API requests
async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;

  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // Add auth token if it exists
  const token = localStorage.getItem('token');
  if (token && defaultOptions.headers) {
    (defaultOptions.headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, defaultOptions);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `HTTP error! status: ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

// Task types
export interface Task {
  id: number;
  title: string;
  description?: string;
  due_at: string;
  user_email: string;
  reminded: boolean;
  created: string;
}

export interface CreateTaskData {
  title: string;
  description?: string;
  due_at: string;
  user_email: string;
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  due_at?: string;
  reminded?: boolean;
}

// Task API functions
export const taskAPI = {
  // Get all tasks
  getTasks: async (): Promise<Task[]> => {
    return await apiRequest('/tasks/');
  },

  // Create a new task
  createTask: async (task: CreateTaskData): Promise<Task> => {
    return await apiRequest('/tasks/', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  },

  // Get a specific task
  getTask: async (id: number): Promise<Task> => {
    return await apiRequest(`/tasks/${id}`);
  },

  // Update a task
  updateTask: async (id: number, updates: UpdateTaskData): Promise<Task> => {
    return await apiRequest(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  },

  // Delete a task
  deleteTask: async (id: number): Promise<void> => {
    await apiRequest(`/tasks/${id}`, {
      method: 'DELETE',
    });
  },

  // Get upcoming tasks
  getUpcomingTasks: async (hours: number = 24): Promise<Task[]> => {
    return await apiRequest(`/tasks/upcoming?hours=${hours}`);
  },

  // Get overdue tasks
  getOverdueTasks: async (): Promise<Task[]> => {
    return await apiRequest('/tasks/overdue');
  },

  // Get task statistics
  getTaskStats: async (): Promise<{
    total_tasks: number;
    overdue_tasks: number;
    upcoming_tasks: number;
  }> => {
    return await apiRequest('/tasks/stats');
  },
};

// Notification types
export interface Notification {
  id: number;
  task_id: number;
  message: string;
  created_at: string;
}

export const notificationAPI = {
  // Get all notifications
  getNotifications: async (): Promise<Notification[]> => {
    return await apiRequest('/notifications/');
  },

  // Get unread count
  getUnreadCount: async (): Promise<{ unread_count: number }> => {
    return await apiRequest('/notifications/unread/count');
  },

  // Delete a notification
  deleteNotification: async (id: number): Promise<void> => {
    await apiRequest(`/notifications/${id}`, {
      method: 'DELETE',
    });
  },
};

// User API functions
export const userAPI = {
  // Get current user profile
  getProfile: async () => {
    return await apiRequest('/users/me');
  },

  // Update profile
  updateProfile: async (updates: any) => {
    return await apiRequest('/users/me', {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  },
};

// Legacy api object for compatibility
export const api = {
  get: (endpoint: string) => apiRequest(endpoint, { method: 'GET' }),
  post: (endpoint: string, data?: any) => apiRequest(endpoint, {
    method: 'POST',
    body: data ? JSON.stringify(data) : undefined,
  }),
  put: (endpoint: string, data?: any) => apiRequest(endpoint, {
    method: 'PUT',
    body: data ? JSON.stringify(data) : undefined,
  }),
  delete: (endpoint: string) => apiRequest(endpoint, { method: 'DELETE' }),
};