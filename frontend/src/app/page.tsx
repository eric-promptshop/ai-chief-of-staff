import React from 'react'

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">
        AI Chief of Staff
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Task Delegation
          </h2>
          <p className="text-gray-600">
            Delegate tasks to AI agents using natural language commands
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Agent Monitoring
          </h2>
          <p className="text-gray-600">
            Track agent activities and task progress in real-time
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Context Management
          </h2>
          <p className="text-gray-600">
            Upload and manage documents for RAG-based agent context
          </p>
        </div>
      </div>
    </div>
  )
} 