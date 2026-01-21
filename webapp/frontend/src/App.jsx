import React, { useState } from 'react';
import UploadPage from './components/UploadPage';
import ResultsPage from './components/ResultsPage';

function App() {
  const [scoreData, setScoreData] = useState(null);

  const handleScoreCalculated = (data) => {
    setScoreData(data);
  };

  const handleReset = () => {
    setScoreData(null);
  };

  return (
    <div className="min-h-screen">
      {!scoreData ? (
        <UploadPage onScoreCalculated={handleScoreCalculated} />
      ) : (
        <ResultsPage scoreData={scoreData} onReset={handleReset} />
      )}
    </div>
  );
}

export default App;
