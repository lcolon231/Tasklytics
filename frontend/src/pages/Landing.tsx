import React from 'react';
import { Link } from 'react-router-dom';
import {
  CheckSquare,
  Clock,
  Mail,
  BarChart3,
  Shield,
  Zap,
  ArrowRight,
  Star
} from 'lucide-react';

const Landing = () => {
  const features = [
    {
      icon: CheckSquare,
      title: 'Smart Task Management',
      description: 'Organize your tasks with intuitive categorization, priority levels, and due dates.'
    },
    {
      icon: Clock,
      title: 'Intelligent Reminders',
      description: 'Never miss a deadline with our smart reminder system that adapts to your schedule.'
    },
    {
      icon: Mail,
      title: 'Email Notifications',
      description: 'Stay updated with beautifully designed email notifications for all your important tasks.'
    },
    {
      icon: BarChart3,
      title: 'Productivity Analytics',
      description: 'Track your productivity with detailed insights and performance metrics.'
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your data is encrypted and secure. We respect your privacy and never share your information.'
    },
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'Built with modern technology for blazing-fast performance and seamless user experience.'
    }
  ];

  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'Product Manager',
      content: 'Tasklytics has transformed how I manage my daily workflow. The smart reminders are a game-changer!',
      rating: 5
    },
    {
      name: 'Michael Chen',
      role: 'Software Developer',
      content: 'Clean interface, powerful features, and excellent performance. Everything I need in a task manager.',
      rating: 5
    },
    {
      name: 'Emily Davis',
      role: 'Marketing Director',
      content: 'The analytics dashboard helps me understand my productivity patterns and optimize my schedule.',
      rating: 5
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-r from-primary-600 to-primary-800 overflow-hidden">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-32">
          <div className="text-center">
            <h1 className="text-4xl sm:text-6xl font-bold text-white mb-6">
              Master Your Tasks,
              <br />
              <span className="text-primary-200">Maximize Your Productivity</span>
            </h1>
            <p className="text-xl sm:text-2xl text-primary-100 mb-8 max-w-3xl mx-auto">
              The intelligent task management platform that adapts to your workflow
              and keeps you focused on what matters most.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/register"
                className="bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-primary-50 transition-colors shadow-lg flex items-center justify-center"
              >
                Get Started Free
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link
                to="/login"
                className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-primary-600 transition-colors flex items-center justify-center"
              >
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              Everything you need to stay organized
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Powerful features designed to help you manage tasks efficiently and boost your productivity.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  className="p-8 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors group"
                >
                  <div className="w-12 h-12 bg-primary-600 rounded-lg flex items-center justify-center mb-6 group-hover:bg-primary-700 transition-colors">
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Testimonials Section */}
      <div className="py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              Loved by thousands of users
            </h2>
            <p className="text-xl text-gray-600">
              See what our users are saying about Tasklytics
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div
                key={index}
                className="bg-white p-8 rounded-xl shadow-sm border border-gray-100"
              >
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-600 mb-6 italic">
                  "{testimonial.content}"
                </p>
                <div>
                  <div className="font-semibold text-gray-900">
                    {testimonial.name}
                  </div>
                  <div className="text-sm text-gray-500">
                    {testimonial.role}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-24 bg-primary-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
            Ready to boost your productivity?
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Join thousands of users who have already transformed their workflow with Tasklytics.
          </p>
          <Link
            to="/register"
            className="bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-primary-50 transition-colors shadow-lg inline-flex items-center"
          >
            Start Your Free Trial
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
                <CheckSquare className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold">Tasklytics</span>
            </div>
            <p className="text-gray-400">
              © 2025 Tasklytics. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;