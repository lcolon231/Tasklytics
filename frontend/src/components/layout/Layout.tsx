import { Outlet, NavLink } from 'react-router-dom'
import { LayoutDashboard } from 'lucide-react'

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-3">
          <LayoutDashboard />
          <span className="font-semibold">Tasklytics</span>
          <div className="ml-auto flex gap-4">
            <NavLink to="/" className={({isActive}) => isActive ? 'text-blue-600' : 'text-gray-600'}>Home</NavLink>
          </div>
        </div>
      </nav>
      <main className="max-w-6xl mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}
