import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { useSearchParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { taskAPI, CreateTaskData, Task } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import {
  Plus,
  Search,
  Filter,
  Calendar,
  Clock,
  AlertTriangle,
  CheckSquare,
  Edit,
  Trash2,
  X
} from 'lucide-react';
import { format, isPast, isToday, isTomorrow } from 'date-fns';
import toast from 'react-hot-toast';

interface TaskFormData {
  title: string;
  description: string;
  due_at: string;
}

const Tasks = () => {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [searchParams] = useSearchParams();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(searchParams.get('action') === 'create');
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  const { data: tasks = [], isLoading } = useQuery('tasks', taskAPI.getTasks);

  const createTaskMutation = useMutation(taskAPI.createTask, {
    onSuccess: () => {
      queryClient.invalidateQueries('tasks');
      queryClient.invalidateQueries('taskStats');
      toast.success('Task created successfully!');
      setIsCreateModalOpen(false);
      reset();
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create task');
    },
  });

  const updateTaskMutation = useMutation(
    ({ id, data }: { id: number; data: any }) => taskAPI.updateTask(id, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('tasks');
        queryClient.invalidateQueries('taskStats');
        toast.success('Task updated successfully!');
        setEditingTask(null);
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.detail || 'Failed to update task');
      },
    }
  );

  const deleteTaskMutation = useMutation(taskAPI.deleteTask, {
    onSuccess: () => {
      queryClient.invalidateQueries('tasks');
      queryClient.invalidateQueries('taskStats');
      toast.success('Task deleted successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to delete task');
    },
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
  } = useForm<TaskFormData>();

  const onSubmit = (data: TaskFormData) => {
    const taskData: CreateTaskData = {
      title: data.title,
      description: data.description || undefined,
      due_at: new Date(data.due_at).toISOString(),
      user_email: user?.email || '',
    };

    if (editingTask) {
      updateTaskMutation.mutate({ id: editingTask.id, data: taskData });
    } else {
      createTaskMutation.mutate(taskData);
    }
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setValue('title', task.title);
    setValue('description', task.description || '');
    setValue('due_at', format(new Date(task.due_at), "yyyy-MM-dd'T'HH:mm"));
    setIsCreateModalOpen(true);
  };

  const handleDelete = (task: Task) => {
    if (window.confirm(`Are you sure you want to delete "${task.title}"?`)) {
      deleteTaskMutation.mutate(task.id);
    }
  };

  const getTaskDateLabel = (dateString: string) => {
    const date = new Date(dateString);
    if (isToday(date)) return 'Today';
    if (isTomorrow(date)) return 'Tomorrow';
    return format(date, 'MMM dd, yyyy');
  };

  const getTaskDateColor = (dateString: string) => {
    const date = new Date(dateString);
    if (isPast(date)) return 'text-red-600 bg-red-100';
    if (isToday(date)) return 'text-orange-600 bg-orange-100';
    if (isTomorrow(date)) return 'text-yellow-600 bg-yellow-100';
    return 'text-green-600 bg-green-100';
  };

  const filteredTasks = tasks.filter((task) => {
    // Search filter
    const matchesSearch = task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         task.description?.toLowerCase().includes(searchTerm.toLowerCase());

    // Type filter
    const matchesFilter = (() => {
      switch (filterType) {
        case 'overdue':
          return isPast(new Date(task.due_at));
        case 'today':
          return isToday(new Date(task.due_at));
        case 'upcoming':
          return !isPast(new Date(task.due_at)) && !isToday(new Date(task.due_at));
        default:
          return true;
      }
    })();

    return matchesSearch && matchesFilter;
  });

  const closeModal = () => {
    setIsCreateModalOpen(false);
    setEditingTask(null);
    reset();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-300 rounded w-1/4 mb-8"></div>
            <div className="space-y-4">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="h-24 bg-gray-300 rounded-lg"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
            <button
              onClick={() => setIsCreateModalOpen(true)}
              className="btn-primary"
            >
              <Plus className="h-4 w-4 mr-2" />
              Add Task
            </button>
          </div>

          {/* Filters */}
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1 relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search tasks..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="form-input pl-10"
              />
            </div>
            <div className="relative">
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="form-input pr-10 appearance-none"
              >
                <option value="all">All Tasks</option>
                <option value="overdue">Overdue</option>
                <option value="today">Due Today</option>
                <option value="upcoming">Upcoming</option>
              </select>
              <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <Filter className="h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>
        </div>

        {/* Tasks List */}
        <div className="space-y-4">
          {filteredTasks.length > 0 ? (
            filteredTasks.map((task) => (
              <div key={task.id} className="card">
                <div className="card-body">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-lg font-medium text-gray-900">{task.title}</h3>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getTaskDateColor(task.due_at)}`}>
                          <Clock className="h-3 w-3 mr-1" />
                          {getTaskDateLabel(task.due_at)}
                        </span>
                        {isPast(new Date(task.due_at)) && (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-red-600 bg-red-100">
                            <AlertTriangle className="h-3 w-3 mr-1" />
                            Overdue
                          </span>
                        )}
                      </div>
                      {task.description && (
                        <p className="text-gray-600 mb-3">{task.description}</p>
                      )}
                      <div className="flex items-center text-sm text-gray-500 space-x-4">
                        <div className="flex items-center">
                          <Calendar className="h-4 w-4 mr-1" />
                          Due: {format(new Date(task.due_at), 'MMM dd, yyyy HH:mm')}
                        </div>
                        <div className="flex items-center">
                          <CheckSquare className="h-4 w-4 mr-1" />
                          Created: {format(new Date(task.created), 'MMM dd, yyyy')}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2 ml-4">
                      <button
                        onClick={() => handleEdit(task)}
                        className="p-2 text-gray-400 hover:text-primary-600 transition-colors"
                        title="Edit task"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(task)}
                        className="p-2 text-gray-400 hover:text-red-600 transition-colors"
                        title="Delete task"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-12">
              <CheckSquare className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                {searchTerm || filterType !== 'all' ? 'No tasks found' : 'No tasks yet'}
              </h3>
              <p className="text-gray-500 mb-6">
                {searchTerm || filterType !== 'all'
                  ? 'Try adjusting your search or filter criteria.'
                  : 'Get started by creating your first task.'
                }
              </p>
              {!searchTerm && filterType === 'all' && (
                <button
                  onClick={() => setIsCreateModalOpen(true)}
                  className="btn-primary"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Create your first task
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Create/Edit Task Modal */}
      {isCreateModalOpen && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-lg w-full">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-gray-900">
                  {editingTask ? 'Edit Task' : 'Create New Task'}
                </h2>
                <button
                  onClick={closeModal}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>

              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <div>
                  <label htmlFor="title" className="form-label">
                    Task Title *
                  </label>
                  <input
                    {...register('title', { required: 'Title is required' })}
                    type="text"
                    className="form-input"
                    placeholder="Enter task title"
                  />
                  {errors.title && (
                    <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
                  )}
                </div>

                <div>
                  <label htmlFor="description" className="form-label">
                    Description
                  </label>
                  <textarea
                    {...register('description')}
                    rows={3}
                    className="form-input"
                    placeholder="Enter task description (optional)"
                  />
                </div>

                <div>
                  <label htmlFor="due_at" className="form-label">
                    Due Date & Time *
                  </label>
                  <input
                    {...register('due_at', { required: 'Due date is required' })}
                    type="datetime-local"
                    className="form-input"
                  />
                  {errors.due_at && (
                    <p className="mt-1 text-sm text-red-600">{errors.due_at.message}</p>
                  )}
                </div>

                <div className="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={closeModal}
                    className="btn-outline"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={createTaskMutation.isLoading || updateTaskMutation.isLoading}
                    className="btn-primary disabled:opacity-50"
                  >
                    {createTaskMutation.isLoading || updateTaskMutation.isLoading ? (
                      <div className="flex items-center">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        {editingTask ? 'Updating...' : 'Creating...'}
                      </div>
                    ) : (
                      editingTask ? 'Update Task' : 'Create Task'
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Tasks;