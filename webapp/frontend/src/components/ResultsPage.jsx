import React from 'react';
import { CheckCircle, XCircle, MinusCircle, RefreshCw, Trophy, Target } from 'lucide-react';

const ResultsPage = ({ scoreData, onReset }) => {
  const { student_info, scores, section_details, question_details } = scoreData;

  const getSectionIcon = (sectionName) => {
    if (sectionName.includes('NAT')) return '🔢';
    if (sectionName.includes('MSQ')) return '☑️';
    if (sectionName.includes('MCQ')) return '✓';
    return '📝';
  };

  const getScoreColor = (score, maxScore) => {
    const percentage = (score / maxScore) * 100;
    if (percentage >= 70) return 'text-green-600';
    if (percentage >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="min-h-screen p-4 py-8">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header Card */}
        <div className="bg-white rounded-2xl shadow-2xl p-6 md:p-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <Trophy className="h-8 w-8 text-yellow-500" />
              <h1 className="text-2xl md:text-3xl font-bold text-gray-900">
                Your Score Report
              </h1>
            </div>
            <button
              onClick={onReset}
              className="flex items-center space-x-2 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg transition-colors"
            >
              <RefreshCw className="h-4 w-4" />
              <span className="hidden sm:inline">New Calculation</span>
            </button>
          </div>

          {/* Student Info */}
          <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-4 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Candidate Name</p>
                <p className="text-lg font-semibold text-gray-900">{student_info.name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Application Number</p>
                <p className="text-lg font-semibold text-gray-900">{student_info.student_id}</p>
              </div>
            </div>
          </div>

          {/* Total Score */}
          <div className="text-center py-6 border-y-2 border-gray-200">
            <p className="text-gray-600 text-sm uppercase tracking-wide mb-2">Total Score</p>
            <div className="flex items-center justify-center space-x-2">
              <span className={`text-5xl md:text-6xl font-bold ${getScoreColor(scores.total_score, 150)}`}>
                {scores.total_score}
              </span>
              <span className="text-3xl md:text-4xl text-gray-400 font-light">/ 150</span>
            </div>
            <div className="mt-4">
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-gradient-to-r from-primary to-secondary h-3 rounded-full transition-all"
                  style={{ width: `${(scores.total_score / 150) * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Section-wise Breakdown */}
        <div className="bg-white rounded-2xl shadow-2xl p-6 md:p-8">
          <h2 className="text-xl md:text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <Target className="h-6 w-6 mr-2 text-primary" />
            Section-wise Breakdown
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            {Object.entries(section_details).map(([section, details]) => (
              <div key={section} className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl p-4 border border-purple-100">
                <div className="flex items-center space-x-2 mb-3">
                  <span className="text-2xl">{getSectionIcon(section)}</span>
                  <h3 className="font-bold text-gray-900">{section}</h3>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Score:</span>
                    <span className="font-bold text-gray-900">
                      {details.score} / {details.max_score}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-green-600 flex items-center">
                      <CheckCircle className="h-3 w-3 mr-1" />
                      Correct:
                    </span>
                    <span className="font-semibold">{details.correct}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-red-600 flex items-center">
                      <XCircle className="h-3 w-3 mr-1" />
                      Wrong:
                    </span>
                    <span className="font-semibold">{details.wrong}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500 flex items-center">
                      <MinusCircle className="h-3 w-3 mr-1" />
                      Unattempted:
                    </span>
                    <span className="font-semibold">{details.unattempted}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Question Details */}
        <div className="bg-white rounded-2xl shadow-2xl p-6 md:p-8">
          <h2 className="text-xl md:text-2xl font-bold text-gray-900 mb-6">
            Question-wise Analysis
          </h2>
          
          <div className="space-y-4">
            {Object.entries(question_details).map(([qNum, details]) => {
              const isCorrect = details.score > 0;
              const isWrong = details.score < 0;
              const isPartial = details.score > 0 && details.score < (details.type === 'NAT' ? 4 : details.type === 'MSQ' ? 4 : 3);
              
              return (
                <div
                  key={qNum}
                  className={`border-l-4 rounded-lg p-4 transition-all ${
                    isCorrect
                      ? 'bg-green-50 border-green-500'
                      : isWrong
                      ? 'bg-red-50 border-red-500'
                      : 'bg-gray-50 border-gray-300'
                  }`}
                >
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                    <div className="flex items-center space-x-3">
                      {isCorrect && <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0" />}
                      {isWrong && <XCircle className="h-5 w-5 text-red-600 flex-shrink-0" />}
                      {!isCorrect && !isWrong && <MinusCircle className="h-5 w-5 text-gray-400 flex-shrink-0" />}
                      
                      <div className="min-w-0">
                        <span className="font-semibold text-gray-900">{qNum}</span>
                        <span className="ml-2 text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded">
                          {details.type}
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-4 text-sm pl-8 sm:pl-0">
                      <div>
                        <span className="text-gray-600">Your Answer: </span>
                        <span className="font-mono font-semibold text-gray-900">
                          {details.student_answer || 'Not Attempted'}
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-600">Correct: </span>
                        <span className="font-mono font-semibold text-green-700">
                          {Array.isArray(details.correct_answer) 
                            ? details.correct_answer.join(', ') 
                            : details.correct_answer}
                        </span>
                      </div>
                      <div className={`font-bold ${
                        isCorrect ? 'text-green-600' : isWrong ? 'text-red-600' : 'text-gray-600'
                      }`}>
                        {details.score > 0 ? '+' : ''}{details.score}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-white text-sm py-4">
          <p>© 2026 CEED Score Calculator | Results are for reference only</p>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
