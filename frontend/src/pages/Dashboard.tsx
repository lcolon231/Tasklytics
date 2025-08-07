import React from 'react';
import { useQuery } from 'react-query';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { taskAPI } from '../services/api';
import {
  CheckSquare,
  Clock,
  AlertTriangle,
  Plus,
  Calendar,
  TrendingUp,
  BarChart3
} from 'lucide-react';
import { format, isToday, isTomorrow, isPast } from 'date-fns';

const Dashboard = () => {
  const { user } = useAuth();

  // Fetch dashboard data
  const { data: stats, isLoading: statsLoading } = useQuery('taskStats', taskAPI.getTaskStats);
  const { data: upcomingTasks, isLoading: upcomingLoading } = useQuery('upcomingTasks', () => taskAPI.getUpcomingTasks(72)); // Next 3 days
  const { data: overdueTasks, isLoading: overdueLoading } = useQuery('overdueTasks', taskAPI.getOverdueTasks);

  const isLoading = statsLoading || upcomingLoading || overdueLoading;

  const getTaskDateLabel = (dateString: string) => {
    const date = new Date(dateString);
    if (isToday(date)) return 'Today';
    if (isTomorrow(date)) return 'Tomorrow';
    return format(date, 'MMM dd');
  };

  const getTaskDateColor = (dateString: string) => {
    const date = new Date(dateString);
    if (isPast(date)) return 'text-red-600 bg-red-100';
    if (isToday(date)) return 'text-orange-600 bg-orange-100';
    if (isTomorrow(date)) return 'text-yellow-600 bg-yellow-100';
    return 'text-green-600 bg-green-100';
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-300 rounded w-1/4 mb-8"></div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-32 bg-gray-300 rounded-lg"></div>
              ))}
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="h-96 bg-gray-300 rounded-lg"></div>
              <div className="h-96 bg-gray-300 rounded-lg"></div>
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.first_name}! 👋
          </h1>
          <p className="text-gray-600">
            Here's what's happening with your tasks today.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <div className="card-body">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                    <CheckSquare className="h-6 w-6 text-primary-600" />
                  </div>
                </div>
                <div className="ml-4 flex-1">
                  <p className="text-sm font-medium text-gray-600">Total Tasks</p>
                  <p className="text-2xl font-bold text-gray-900">{stats?.total_tasks || 0}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-body">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                    <Clock className="h-6 w-6 text-orange-600" />
                  </div>
                </div>
                <div className="ml-4 flex-1">
                  <p className="text-sm font-medium text-gray-600">Due Soon</p>
                  <p className="text-2xl font-bold text-gray-900">{stats?.upcoming_tasks || 0}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-body">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                    <AlertTriangle className="h-6 w-6 text-red-600" />
                  </div>
                </div>
                <div className="ml-4 flex-1">
                  <p className="text-sm font-medium text-gray-600">Overdue</p>
                  <p className="text-2xl font-bold text-gray-900">{stats?.overdue_tasks || 0}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upcoming Tasks */}
          <div className="card">
            <div className="card-header">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900 flex items-center">
                  <Calendar className="h-5 w-5 mr-2 text-gray-500" />
                  Upcoming Tasks
                </h3>
                <Link
                  to="/tasks"
                  className="text-primary-600 hover:text-primary-500 text-sm font-medium"
                >
                  View all
                </Link>
              </div>
            </div>
            <div className="card-body">
              {upcomingTasks?.length > 0 ? (
                <div className="space-y-4">
                  {upcomingTasks.slice(0, 5).map((task) => (
                    <div key={task.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex-1">
                        <h4 className="font-medium text-gray-900 mb-1">{task.title}</h4>
                        {task.description && (
                          <p className="text-sm text-gray-600 mb-2 line-clamp-1">{task.description}</p>
                        )}
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getTaskDateColor(task.due_at)}`}>
                          <Clock className="h-3 w-3 mr-1" />
                          {getTaskDateLabel(task.due_at)}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-6">
                  <Calendar className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">No upcoming tasks</p>
                  <Link
                    to="/tasks"
                    className="mt-2 inline-flex items-center text-primary-600 hover:text-primary-500 font-medium"
                  >
                    <Plus className="h-4 w-4 mr-1" />
                    Create your first task
                  </Link>
                </div>
              )}
            </div>
          </div>

          {/* Overdue Tasks */}
          <div className="card">
            <div className="card-header">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900 flex items-center">
                  <AlertTriangle className="h-5 w-5 mr-2 text-red-500" />
                  Overdue Tasks
                </h3>
                {overdueTasks?.length > 0 && (
                  <Link
                    to="/tasks?filter=overdue"
                    className="text-red-600 hover:text-red-500 text-sm font-medium"
                  >
                    View all
                  </Link>
                )}
              </div>
            </div>
            <div className="card-body">
              {overdueTasks?.length > 0 ? (
                <div className="space-y-4">
                  {overdueTasks.slice(0, 5).map((task) => (
                    <div key={task.id} className="flex items-center justify-between p-3 bg-red-50 rounded-lg border border-red-200">
                      <div className="flex-1">
                        <h4 className="font-medium text-gray-900 mb-1">{task.title}</h4>
                        {task.description && (
                          <p className="text-sm text-gray-600 mb-2 line-clamp-1">{task.description}</p>
                        )}
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-red-600 bg-red-100">
                          <AlertTriangle className="h-3 w-3 mr-1" />
                          {format(new Date(task.due_at), 'MMM dd, yyyy')}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-6">
                  <CheckSquare className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500 mb-2">Great job! No overdue tasks</p>
                  <p className="text-sm text-gray-400">Keep up the excellent work!</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900 flex items-center">
              <TrendingUp className="h-5 w-5 mr-2 text-gray-500" />
              Quick Actions
            </h3>
          </div>
          <div className="card-body">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <Link
                to="/tasks?action=create"
                className="flex items-center p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors group"
              >
                <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center group-hover:bg-primary-700 transition-colors">
                  <Plus className="h-5 w-5 text-white" />
                </div>
                <div className="ml-3">
                  <p className="font-medium text-gray-900">Create Task</p>
                  <p className="text-sm text-gray-600">Add a new task</p>
                </div>
              </Link>

              <Link
                to="/tasks"
                className="flex items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors group"
              >
                <div className="w-10 h-10 bg-gray-600 rounded-lg flex items-center justify-center group-hover:bg-gray-700 transition-colors">
                  <CheckSquare className="h-5 w-5 text-white" />
                </div>
                <div className="ml-3">
                  <p className="font-medium text-gray-900">View All Tasks</p>
                  <p className="text-sm text-gray-600">Manage your tasks</p>
                </div>
              </Link>

              <Link
                to="/profile"
                className="flex items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors group"
              >
                <div className="w-10 h-10 bg-gray-600 rounded-lg flex items-center justify-center group-hover:bg-gray-700 transition-colors">
                  <BarChart3 className="h-5 w-5 text-white" />
                </div>
                <div className="ml-3">
                  <p className="font-medium text-gray-900">View Profile</p>
                  <p className="text-sm text-gray-600">Account settings</p>
                </div>
              </Link>

              <div className="flex items-center p-4 bg-green-50 rounded-lg">
                <div className="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center">
                  <TrendingUp className="h-5 w-5 text-white" />
                </div>
                <div className="ml-3">
                  <p className="font-medium text-gray-900">Productivity</p>
                  <p className="text-sm text-green-600">
                    {stats?.total_tasks ?
                      `${Math.round(((stats.total_tasks - (stats.overdue_tasks || 0)) / stats.total_tasks) * 100)}% on track`
                      : 'No data yet'
                    }
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;