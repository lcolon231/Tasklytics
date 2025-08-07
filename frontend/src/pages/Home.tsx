import React, { useEffect, useState } from "react";

export default function BackendStatus() {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch("http://localhost:8000/health");
        if (!res.ok) throw new Error("Backend not healthy");
        const result = await res.json();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    checkHealth();
  }, []);

  return (
    <div className="mt-4">
      <h2 className="font-semibold mb-2">Backend Health</h2>

      {isLoading && <p>Checking backend status...</p>}

      {error && (
        <p className="text-red-600 font-medium">
          Could not reach backend. Make sure it's running.
        </p>
      )}

      {data && (
        <div className="flex items-center gap-2 p-3 bg-gray-50 rounded border">
          <span
            className={`h-3 w-3 rounded-full ${
              data.status === "healthy" ? "bg-green-500" : "bg-red-500"
            }`}
          ></span>
          <span>
            {data.service} is{" "}
            <strong
              className={
                data.status === "healthy" ? "text-green-600" : "text-red-600"
              }
            >
              {data.status}
            </strong>
          </span>
        </div>
      )}
    </div>
  );
}
