import React from 'react';
import ChatThread from './components/ChatThread';
import AgentSelector from './components/AgentSelector';
import FileUploader from './components/FileUploader';
import AutonomySlider from './components/AutonomySlider';

export default function App() {
  return (
    <div className="p-6">
      <h1 className="text-xl font-bold">AI Chief of Staff</h1>
      <AgentSelector />
      <FileUploader />
      <AutonomySlider />
      <ChatThread />
    </div>
  );
}