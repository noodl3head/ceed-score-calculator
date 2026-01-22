import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, Dot } from 'recharts';
import axios from 'axios';

const ScoreChart = ({ userScore }) => {
  const [allScores, setAllScores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchScores = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
        const response = await axios.get(`${apiUrl}/api/scores`);
        
        if (response.data.scores && response.data.scores.length > 0) {
          setAllScores(response.data.scores);
        } else {
          // No scores available yet
          setAllScores([]);
        }
        setLoading(false);
      } catch (err) {
        console.error('Error fetching scores:', err);
        // Don't show error, just show empty state
        setAllScores([]);
        setLoading(false);
      }
    };

    fetchScores();
  }, []);

  if (loading) {
    return (
      <div className="bg-white rounded-2xl shadow-2xl p-6 md:p-8">
        <h2 className="text-xl md:text-2xl font-bold text-gray-900 mb-6">
          Score Distribution
        </h2>
        <div className="flex items-center justify-center h-64">
          <div className="animate-pulse text-gray-500">Loading chart...</div>
        </div>
      </div>
    );
  }

  if (error || allScores.length === 0) {
    return (
      <div className="bg-white rounded-2xl shadow-2xl p-6 md:p-8">
        <h2 className="text-xl md:text-2xl font-bold text-gray-900 mb-6">
          Score Distribution
        </h2>
        <div className="flex flex-col items-center justify-center h-64 space-y-4">
          <div className="text-6xl">📊</div>
          <div className="text-gray-600 text-center">
            <p className="font-semibold mb-2">Score comparison not available yet</p>
            <p className="text-sm text-gray-500">
              {error || 'Once more students submit their scores, you\'ll see how you compare!'}
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Prepare data for chart
  const chartData = allScores.map((score, index) => ({
    index: index + 1,
    score: score,
    isUser: Math.abs(score - userScore) < 0.01 // Check if this is user's score
  }));

  // Find user's position
  const userPosition = allScores.findIndex(score => Math.abs(score - userScore) < 0.01) + 1;
  const totalScores = allScores.length;
  const percentile = userPosition ? Math.round((userPosition / totalScores) * 100) : null;

  // Custom dot renderer to highlight user's score
  const CustomDot = (props) => {
    const { cx, cy, payload } = props;
    if (payload.isUser) {
      return (
        <g>
          <circle cx={cx} cy={cy} r={8} fill="#f59e0b" stroke="#fff" strokeWidth={3} />
          <circle cx={cx} cy={cy} r={3} fill="#fff" />
        </g>
      );
    }
    return <circle cx={cx} cy={cy} r={4} fill="#8b5cf6" />;
  };

  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white border border-gray-300 rounded-lg shadow-lg p-3">
          <p className="text-sm font-semibold text-gray-900">
            {data.isUser ? '👤 Your Score' : `Position #${data.index}`}
          </p>
          <p className="text-sm text-gray-700">
            Score: <span className="font-bold text-purple-600">{data.score}</span>
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white rounded-2xl shadow-2xl p-6 md:p-8">
      <div className="mb-6">
        <h2 className="text-xl md:text-2xl font-bold text-gray-900 mb-2">
          Score Distribution
        </h2>
        <p className="text-sm text-gray-600">
          Compare your performance with {totalScores} total submissions
        </p>
        {percentile && (
          <div className="mt-3 inline-flex items-center bg-yellow-50 border border-yellow-200 rounded-lg px-4 py-2">
            <span className="text-2xl mr-2">🎯</span>
            <div>
              <p className="text-sm font-semibold text-yellow-900">
                You're in the top {percentile}%
              </p>
              <p className="text-xs text-yellow-700">
                Position {userPosition} out of {totalScores} students
              </p>
            </div>
          </div>
        )}
      </div>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 30 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="index" 
              label={{ value: 'Student Rank', position: 'insideBottom', offset: -10, fill: '#6b7280' }}
              stroke="#9ca3af"
              tick={{ fill: '#6b7280' }}
            />
            <YAxis 
              label={{ value: 'Total Score', angle: -90, position: 'insideLeft', fill: '#6b7280' }}
              stroke="#9ca3af"
              tick={{ fill: '#6b7280' }}
              domain={[0, 150]}
            />
            <Tooltip content={<CustomTooltip />} />
            <ReferenceLine 
              y={userScore} 
              stroke="#f59e0b" 
              strokeDasharray="5 5" 
              strokeWidth={2}
              label={{ 
                value: 'Your Score', 
                position: 'right',
                fill: '#f59e0b',
                fontSize: 12,
                fontWeight: 'bold'
              }}
            />
            <Line 
              type="monotone" 
              dataKey="score" 
              stroke="#8b5cf6" 
              strokeWidth={2}
              dot={<CustomDot />}
              activeDot={{ r: 8 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 flex items-center justify-center space-x-6 text-xs text-gray-600">
        <div className="flex items-center">
          <div className="w-4 h-4 rounded-full bg-purple-500 mr-2"></div>
          <span>Other Students</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 rounded-full bg-yellow-500 mr-2"></div>
          <span>Your Score</span>
        </div>
      </div>
    </div>
  );
};

export default ScoreChart;
