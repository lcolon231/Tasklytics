export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center flex-col text-center px-4">
      <h1 className="text-5xl font-bold text-gray-800 mb-4">404</h1>
      <p className="text-gray-600 mb-6">Oops! The page you're looking for doesn't exist.</p>
      <a href="/" className="text-primary-600 hover:underline">
        Go back home
      </a>
    </div>
  );
}
