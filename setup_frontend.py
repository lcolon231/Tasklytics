#!/usr/bin/env python3
"""
Quick Frontend Setup for Tasklytics (ASCII-only)
- React + Vite + TS + Tailwind
- Router + Layout + Pages
- Axios service w/ baseURL from VITE_API_URL
- TanStack Query (@tanstack/react-query)
- ESLint + Prettier (optional but added)
"""

import json
from pathlib import Path

ROOT = Path("frontend")

def write(path: Path, content: str, binary=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "wb" if binary else "w"
    with open(path, mode, encoding="utf-8" if not binary else None) as f:
        f.write(content if binary else content.rstrip() + "\n")
    print(f"Created: {path.as_posix()}")

def create_frontend_structure():
    directories = [
        ROOT / "src/components/layout",
        ROOT / "src/contexts",
        ROOT / "src/pages",
        ROOT / "src/services",
        ROOT / "public",
    ]
    for d in directories:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Created: {d.as_posix()}")

    package_json = {
        "name": "tasklytics-frontend",
        "private": True,
        "version": "1.0.0",
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "tsc -b && vite build",
            "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
            "preview": "vite preview"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.25.1",
            "axios": "^1.7.2",
            "@tanstack/react-query": "^5.51.1",
            "date-fns": "^2.30.0",
            "react-hot-toast": "^2.4.1",
            "lucide-react": "^0.441.0",
            "clsx": "^2.1.1",
            "tailwind-merge": "^2.5.2"
        },
        "devDependencies": {
            "@types/react": "^18.2.66",
            "@types/react-dom": "^18.2.22",
            "@typescript-eslint/eslint-plugin": "^7.17.0",
            "@typescript-eslint/parser": "^7.17.0",
            "@vitejs/plugin-react": "^4.3.1",
            "autoprefixer": "^10.4.19",
            "eslint": "^9.7.0",
            "eslint-plugin-react-hooks": "^5.1.0",
            "eslint-plugin-react-refresh": "^0.4.7",
            "postcss": "^8.4.40",
            "prettier": "^3.3.3",
            "tailwindcss": "^3.4.9",
            "typescript": "^5.5.4",
            "vite": "^5.3.4"
        }
    }
    write(ROOT / "package.json", json.dumps(package_json, indent=2))

    index_html = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Tasklytics - Smart Task Management</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  </head>
  <body class="bg-gray-50">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>"""
    write(ROOT / "index.html", index_html)

    main_tsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './index.css'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Layout from '@/components/layout/Layout'
import Home from '@/pages/Home'
import NotFound from '@/pages/NotFound'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: '*', element: <NotFound /> },
    ],
  },
])

const qc = new QueryClient()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={qc}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>,
)
"""
    write(ROOT / "src/main.tsx", main_tsx)

    index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    font-family: 'Inter', system-ui, sans-serif;
  }
}"""
    write(ROOT / "src/index.css", index_css)

    layout_tsx = """import { Outlet, NavLink } from 'react-router-dom'
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
"""
    write(ROOT / "src/components/layout/Layout.tsx", layout_tsx)

    home_tsx = """import { useQuery } from '@tanstack/react-query'
import api from '@/services/api'

export default function Home() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const res = await api.get('/health')
      return res.data
    },
  })

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm">
      <h1 className="text-2xl font-bold mb-2">Tasklytics Frontend</h1>
      <p className="text-gray-600 mb-6">Your frontend is set up and ready to go.</p>

      <ul className="list-disc pl-6 space-y-1 mb-6">
        <li>Install deps: <code>npm install</code></li>
        <li>Run dev: <code>npm run dev</code></li>
        <li>Backend expected at <code>VITE_API_URL</code> (proxy /api -> localhost:8000)</li>
      </ul>

      <div className="mt-4">
        <h2 className="font-semibold mb-2">Backend Health (demo)</h2>
        {isLoading && <p>Checking...</p>}
        {error && <p className="text-red-600">Failed to reach backend. Start it or set VITE_API_URL.</p>}
        {data && <pre className="bg-gray-50 p-3 rounded border text-sm overflow-auto">{JSON.stringify(data, null, 2)}</pre>}
      </div>
    </div>
  )
}
"""
    write(ROOT / "src/pages/Home.tsx", home_tsx)

    notfound_tsx = """export default function NotFound() {
  return (
    <div className="text-center text-gray-600">
      <h1 className="text-3xl font-bold mb-2">404</h1>
      <p>Page not found.</p>
    </div>
  )
}
"""
    write(ROOT / "src/pages/NotFound.tsx", notfound_tsx)

    api_ts = """import axios from 'axios'

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL,
  withCredentials: true,
})

api.interceptors.response.use(
  (r) => r,
  (err) => {
    return Promise.reject(err)
  }
)

export default api
"""
    write(ROOT / "src/services/api.ts", api_ts)

    auth_ctx = """import { createContext, useContext, useState } from 'react'

type User = { id: string; email: string } | null

type AuthCtx = {
  user: User
  setUser: (u: User) => void
}

const Ctx = createContext<AuthCtx | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User>(null)
  return <Ctx.Provider value={{ user, setUser }}>{children}</Ctx.Provider>
}

export function useAuth() {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
"""
    write(ROOT / "src/contexts/AuthContext.tsx", auth_ctx)

    vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (p) => p.replace(/^\\/api/, ''),
      }
    }
  }
})
"""
    write(ROOT / "vite.config.ts", vite_config)

    tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        }
      }
    },
  },
  plugins: [],
}
"""
    write(ROOT / "tailwind.config.js", tailwind_config)

    postcss_config = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
    write(ROOT / "postcss.config.js", postcss_config)

    tsconfig = """{
  "compilerOptions": {
    "target": "ES2022",
    "useDefineForClassFields": true,
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
"""
    write(ROOT / "tsconfig.json", tsconfig)

    tsconfig_node = """{
  "compilerOptions": {
    "composite": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
"""
    write(ROOT / "tsconfig.node.json", tsconfig_node)

    env_content = """VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Tasklytics
VITE_APP_VERSION=1.0.0
"""
    write(ROOT / ".env", env_content)

    gitignore = """# Node
node_modules
dist
dist-ssr
*.local

# Env
.env
.env.*
!.env.example

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Editor
.vscode
.idea
.DS_Store
"""
    write(ROOT / ".gitignore", gitignore)

    eslint = """{
  "root": true,
  "env": { "browser": true, "es2022": true, "node": true },
  "parser": "@typescript-eslint/parser",
  "parserOptions": { "ecmaVersion": "latest", "sourceType": "module" },
  "plugins": ["@typescript-eslint", "react-refresh"],
  "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
  "ignorePatterns": ["dist/", "node_modules/"],
  "rules": {
    "react-refresh/only-export-components": ["warn", { "allowConstantExport": true }]
  }
}
"""
    write(ROOT / ".eslintrc.json", eslint)

    prettier = """{}"""
    write(ROOT / ".prettierrc", prettier)

    write(ROOT / "public/robots.txt", "User-agent: *\nDisallow:\n")
    write(ROOT / "public/favicon.ico", b"", binary=True)

def main():
    print("Setting up Tasklytics Frontend Structure...")
    print("=" * 60)
    create_frontend_structure()
    print("=" * 60)
    print("Frontend structure created!\n")
    print("Next Steps:")
    print("1) cd frontend")
    print("2) npm install")
    print("3) npm run dev -> http://localhost:5173")
    print("\nBackend tips:")
    print(" - Start FastAPI at http://localhost:8000 with a /health endpoint.")
    print(" - Or point VITE_API_URL to your deployed API.")

if __name__ == "__main__":
    main()
