import { Link, useNavigate, useLocation } from 'react-router-dom'
import { isLoggedIn, removeToken } from '../utils/auth'
import './Navbar.css'

export default function Navbar() {
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    removeToken()
    navigate('/login')
  }

  const hideOnAuthPages = ['/login', '/signup'].includes(location.pathname)

  if (hideOnAuthPages) return null

  return (
    <header className="navbar">
      <div className="navbar-container">
        <Link to="/home" className="logo">Tasklytics</Link>
        <nav>
          <Link to="/home">All Tasks</Link>
          <Link to="/create">Create Task</Link>
          {!isLoggedIn() ? (
            <>
              <Link to="/login">Login</Link>
              <Link to="/signup">Sign Up</Link>
            </>
          ) : (
            <button onClick={handleLogout}>Logout</button>
          )}
        </nav>
      </div>
    </header>
  )
}
