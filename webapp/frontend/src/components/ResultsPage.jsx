import React from 'react';
import { CheckCircle, XCircle, MinusCircle, RefreshCw, Trophy, Target } from 'lucide-react';
import ScoreChart from './ScoreChart';

const ResultsPage = ({ scoreData, onReset }) => {
  const { student_info, scores, section_details, question_details, warning } = scoreData;

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
            <p className="text-xs text-gray-500 mt-3 text-center">
              ⚠️ This is an estimate only. The final score may vary slightly due to potential errors in PDF parsing and calculation.
            </p>
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

        {/* Score Distribution Chart */}
        <ScoreChart userScore={scores.total_score} />

        {/* Warning Section for Many N/As */}
        {warning?.has_many_na && (
          <div className="bg-red-50 border-2 border-red-200 rounded-2xl shadow-2xl p-6 md:p-8">
            <h2 className="text-xl md:text-2xl font-bold text-red-900 mb-4">
              🚨 Do you think the result is incorrect?
            </h2>
            <p className="text-gray-700 mb-4">
              We detected <span className="font-bold text-red-600">{warning.na_count} N/A answers</span> in your response sheet. 
              This usually happens when the PDF doesn't contain proper text data (e.g., it's an image or screenshot).
            </p>
            <p className="text-gray-700 mb-6">
              <span className="font-semibold">Follow this video tutorial</span> to learn how to correctly save your PDF response sheet:
            </p>
            <div className="bg-white rounded-lg p-4 shadow-inner">
              <video 
                className="w-full max-w-2xl mx-auto rounded-lg shadow-lg"
                controls
                preload="metadata"
              >
                <source src="/tutorial.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
              <p className="text-sm text-gray-600 mt-3 text-center">
                💡 <span className="font-semibold">Pro Tip:</span> Use your browser's "Print" function and select "Save as PDF" 
                instead of taking screenshots or using "Download as Image".
              </p>
            </div>
          </div>
        )}

        {/* Question Details */}
        <div className="bg-white rounded-2xl shadow-2xl p-6 md:p-8">
          <h2 className="text-xl md:text-2xl font-bold text-gray-900 mb-6">
            Question-wise Analysis
          </h2>
          
          <div className="space-y-4">
            {Object.entries(question_details)
              .sort(([a], [b]) => {
                // Extract numeric part from question number (e.g., "Q1" -> 1)
                const numA = parseInt(a.replace(/\D/g, ''));
                const numB = parseInt(b.replace(/\D/g, ''));
                return numA - numB;
              })
              .map(([qNum, details]) => {
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

        {/* How Score is Calculated - Detailed Section */}
        <div className="bg-white rounded-2xl shadow-2xl p-6 md:p-8">
          <h2 className="text-xl md:text-2xl font-bold text-gray-900 mb-6">How Your Score Was Calculated</h2>
          <div className="space-y-6 text-gray-700">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Step 1: Parsing Your Response Sheet</h3>
              <p className="text-sm leading-relaxed">
                First, we read your PDF file and extract the text from every page. We look for question numbers, 
                your chosen options, answers, and the status of each question (whether you attempted it or not). 
                This is done using smart text recognition.
              </p>
            </div>

            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Step 2: Organizing Questions</h3>
              <p className="text-sm leading-relaxed mb-2">
                Here's where it gets tricky - your response sheet PDF shows questions in a different order than 
                the actual question paper! This is because every student gets a shuffled version to prevent copying. 
                The PDF might show Q1, Q2, Q3... but they're not in the same sequence as the original paper.
              </p>
              <p className="text-sm leading-relaxed">
                To solve this, we don't rely on the question numbers in your PDF. Instead, we look at the actual 
                question text and match it with the original question paper. We search for specific phrases and 
                patterns from each question to figure out which question from the paper (Q1 to Q44) it actually is. 
                This way, we correctly map your answers to the right questions, no matter how shuffled they are.
              </p>
            </div>

            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Step 3: Comparing with Answer Key</h3>
              <p className="text-sm leading-relaxed">
                We then compare your answers with the official answer key. For each question, we check if your 
                answer matches the correct answer. This tells us which questions you got right, which ones you 
                got wrong, and which ones you didn't attempt.
              </p>
            </div>

            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Step 4: Applying Marking Scheme</h3>
              <p className="text-sm leading-relaxed mb-3">
                Finally, we calculate your score based on the official marking scheme for each type of question:
              </p>
              <div className="space-y-2 ml-4">
                <div className="bg-blue-50 p-3 rounded-lg">
                  <p className="font-semibold text-sm">🔢 NAT (Numerical Answer Type) - 8 Questions</p>
                  <p className="text-xs text-gray-600 mt-1">+4 marks for correct answer | 0 for wrong/unattempted | Max: 32 marks</p>
                </div>
                <div className="bg-purple-50 p-3 rounded-lg">
                  <p className="font-semibold text-sm">☑️ MSQ (Multiple Select Question) - 10 Questions</p>
                  <p className="text-xs text-gray-600 mt-1">+4 for all correct | Partial marks for partially correct | -1 if any selected option is wrong | 0 for unattempted | Max: 40 marks</p>
                </div>
                <div className="bg-green-50 p-3 rounded-lg">
                  <p className="font-semibold text-sm">✓ MCQ (Multiple Choice Question) - 26 Questions</p>
                  <p className="text-xs text-gray-600 mt-1">+3 for correct | -0.5 for wrong | 0 for unattempted | Max: 78 marks</p>
                </div>
              </div>
            </div>

            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2 text-sm">⚠️ Important Note</h3>
              <p className="text-xs text-gray-600 leading-relaxed">
                While we've done our best to make this calculator accurate, the final score shown is an estimate. 
                The accuracy depends on how well your PDF was parsed and how clearly the text could be extracted. 
                Small variations might occur if the PDF quality is poor or if the text layout is unusual. Always 
                cross-check with official results when they're released.
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-gray-700 text-sm py-4">
          <p className="font-medium">© 2026 CEED Score Calculator | Results are for reference only</p>
          <div className="mt-4">
            <p className="text-sm text-gray-600 mb-2">Follow the developer</p>
            <div className="flex justify-center space-x-4">
              <a 
                href="https://www.linkedin.com/in/rohith-narasimhan-a16657220/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 font-medium transition-colors"
              >
                LinkedIn
              </a>
              <a 
                href="https://www.instagram.com/rohithwokeup/?hl=en" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-pink-600 hover:text-pink-800 font-medium transition-colors"
              >
                Instagram
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
