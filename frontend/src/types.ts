// src/types.ts

export interface Task {
   id: number;
  title: string;
  description: string;
  due_at: string; // Add this
  user_email: string; // Add this
  reminded: boolean;
  created: string;
}

export interface DeleteResponse {
  detail: string
}
