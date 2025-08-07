import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useAuth } from '../contexts/AuthContext';
import { userAPI } from '../services/api';
import { useMutation, useQueryClient } from 'react-query';
import {
  User,
  Mail,
  Calendar,
  Settings,
  Shield,
  Bell,
  Save,
  Edit
} from 'lucide-react';
import toast from 'react-hot-toast';

interface ProfileFormData {
  first_name: string;
  last_name: string;
  age: number;
}

const Profile = () => {
  const { user, logout } = useAuth();
  const queryClient = useQueryClient();
  const [isEditing, setIsEditing] = useState(false);

  const updateProfileMutation = useMutation(userAPI.updateProfile, {
    onSuccess: () => {
      queryClient.invalidateQueries('user');
      toast.success('Profile updated successfully!');
      setIsEditing(false);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update profile');
    },
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ProfileFormData>({
    defaultValues: {
      first_name: user?.first_name || '',
      last_name: user?.last_name || '',
      age: 25, // Default age since we don't store it in user context
    },
  });

  const onSubmit = (data: ProfileFormData) => {
    updateProfileMutation.mutate(data);
  };

  const handleEditToggle = () => {
    if (isEditing) {
      reset({
        first_name: user?.first_name || '',
        last_name: user?.last_name || '',
        age: 25,
      });
    }
    setIsEditing(!isEditing);
  };

  const handleDeleteAccount = () => {
    if (window.confirm(
      'Are you sure you want to delete your account? This action cannot be undone and will permanently delete all your tasks and data.'
    )) {
      // In a real app, you'd implement account deletion
      toast.error('Account deletion not implemented yet');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Profile Settings</h1>
          <p className="text-gray-600 mt-2">
            Manage your account settings and preferences
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Profile Card */}
          <div className="lg:col-span-2">
            <div className="card">
              <div className="card-header">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-medium text-gray-900 flex items-center">
                    <User className="h-5 w-5 mr-2 text-gray-500" />
                    Personal Information
                  </h2>
                  <button
                    onClick={handleEditToggle}
                    className="btn-outline text-sm"
                  >
                    <Edit className="h-4 w-4 mr-1" />
                    {isEditing ? 'Cancel' : 'Edit'}
                  </button>
                </div>
              </div>
              <div className="card-body">
                {isEditing ? (
                  <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label htmlFor="first_name" className="form-label">
                          First Name
                        </label>
                        <input
                          {...register('first_name', {
                            required: 'First name is required',
                            minLength: {
                              value: 2,
                              message: 'First name must be at least 2 characters',
                            },
                          })}
                          type="text"
                          className="form-input"
                        />
                        {errors.first_name && (
                          <p className="mt-1 text-sm text-red-600">{errors.first_name.message}</p>
                        )}
                      </div>
                      <div>
                        <label htmlFor="last_name" className="form-label">
                          Last Name
                        </label>
                        <input
                          {...register('last_name', {
                            required: 'Last name is required',
                            minLength: {
                              value: 2,
                              message: 'Last name must be at least 2 characters',
                            },
                          })}
                          type="text"
                          className="form-input"
                        />
                        {errors.last_name && (
                          <p className="mt-1 text-sm text-red-600">{errors.last_name.message}</p>
                        )}
                      </div>
                    </div>

                    <div>
                      <label htmlFor="age" className="form-label">
                        Age
                      </label>
                      <input
                        {...register('age', {
                          required: 'Age is required',
                          min: {
                            value: 13,
                            message: 'You must be at least 13 years old',
                          },
                          max: {
                            value: 120,
                            message: 'Please enter a valid age',
                          },
                        })}
                        type="number"
                        className="form-input max-w-xs"
                      />
                      {errors.age && (
                        <p className="mt-1 text-sm text-red-600">{errors.age.message}</p>
                      )}
                    </div>

                    <div className="flex justify-end">
                      <button
                        type="submit"
                        disabled={updateProfileMutation.isLoading}
                        className="btn-primary disabled:opacity-50"
                      >
                        {updateProfileMutation.isLoading ? (
                          <div className="flex items-center">
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                            Saving...
                          </div>
                        ) : (
                          <>
                            <Save className="h-4 w-4 mr-2" />
                            Save Changes
                          </>
                        )}
                      </button>
                    </div>
                  </form>
                ) : (
                  <div className="space-y-6">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-500 mb-1">
                          First Name
                        </label>
                        <p className="text-lg text-gray-900">{user?.first_name}</p>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-500 mb-1">
                          Last Name
                        </label>
                        <p className="text-lg text-gray-900">{user?.last_name}</p>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-500 mb-1">
                        Email Address
                      </label>
                      <div className="flex items-center">
                        <Mail className="h-4 w-4 text-gray-400 mr-2" />
                        <p className="text-lg text-gray-900">{user?.email}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Stats */}
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-medium text-gray-900">Account Overview</h3>
              </div>
              <div className="card-body">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <User className="h-4 w-4 text-gray-400 mr-2" />
                      <span className="text-sm text-gray-600">Account ID</span>
                    </div>
                    <span className="text-sm font-medium text-gray-900">#{user?.id}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <Shield className="h-4 w-4 text-green-400 mr-2" />
                      <span className="text-sm text-gray-600">Status</span>
                    </div>
                    <span className="text-sm font-medium text-green-600">Active</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Settings */}
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-medium text-gray-900 flex items-center">
                  <Settings className="h-5 w-5 mr-2 text-gray-500" />
                  Settings
                </h3>
              </div>
              <div className="card-body">
                <div className="space-y-3">
                  <button className="w-full flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <div className="flex items-center">
                      <Bell className="h-4 w-4 text-gray-400 mr-3" />
                      <span className="text-sm text-gray-700">Notifications</span>
                    </div>
                    <span className="text-xs text-gray-500">Enabled</span>
                  </button>

                  <button className="w-full flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <div className="flex items-center">
                      <Shield className="h-4 w-4 text-gray-400 mr-3" />
                      <span className="text-sm text-gray-700">Privacy</span>
                    </div>
                    <span className="text-xs text-gray-500">Manage</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Danger Zone */}
            <div className="card border-red-200">
              <div className="card-header border-red-200">
                <h3 className="text-lg font-medium text-red-600">Danger Zone</h3>
              </div>
              <div className="card-body">
                <div className="space-y-4">
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Sign out everywhere</h4>
                    <p className="text-sm text-gray-600 mb-3">
                      This will sign you out of all devices and sessions.
                    </p>
                    <button
                      onClick={logout}
                      className="btn-outline text-red-600 border-red-600 hover:bg-red-50"
                    >
                      Sign Out
                    </button>
                  </div>

                  <hr className="border-red-200" />

                  <div>
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Delete account</h4>
                    <p className="text-sm text-gray-600 mb-3">
                      Permanently delete your account and all associated data.
                    </p>
                    <button
                      onClick={handleDeleteAccount}
                      className="btn-outline text-red-600 border-red-600 hover:bg-red-50"
                    >
                      Delete Account
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;