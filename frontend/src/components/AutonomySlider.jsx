import React from 'react';

export default function AutonomySlider() {
  return (
    <div className="mt-4">
      <label>Autonomy Level</label>
      <input type="range" min="0" max="10" className="w-full" />
    </div>
  );
}