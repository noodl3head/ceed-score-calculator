import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Upload, FileText, Loader2, Download, TestTube } from 'lucide-react';

const UploadPage = ({ onScoreCalculated }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === 'application/pdf') {
        setFile(droppedFile);
        setError('');
      } else {
        setError('Please upload a PDF file');
      }
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type === 'application/pdf') {
        setFile(selectedFile);
        setError('');
      } else {
        setError('Please upload a PDF file');
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const response = await axios.post(`${apiUrl}/api/calculate-score`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      onScoreCalculated(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to calculate score. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTrySample = async () => {
    try {
      setLoading(true);
      setError('');
      
      // Fetch the sample PDF
      const response = await fetch('/sample-response.pdf');
      const blob = await response.blob();
      const sampleFile = new File([blob], 'sample-response.pdf', { type: 'application/pdf' });
      
      setFile(sampleFile);
      
      // Automatically upload the sample
      const formData = new FormData();
      formData.append('file', sampleFile);
      
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const apiResponse = await axios.post(`${apiUrl}/api/calculate-score`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      onScoreCalculated(apiResponse.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load sample. Please try again.');
      setFile(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-2xl space-y-6">
        <div className="bg-white rounded-2xl shadow-2xl p-8 space-y-6">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              CEED 2026 Score Calculator
            </h1>
            <p className="text-gray-600">
              Upload your response sheet PDF to calculate your score
            </p>
          </div>

          <div
            className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all ${
              dragActive
                ? 'border-primary bg-purple-50'
                : 'border-gray-300 hover:border-primary'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="hidden"
            />

            {!file ? (
              <div className="space-y-4 cursor-pointer">
                <Upload className="mx-auto h-12 w-12 text-gray-400" />
                <div>
                  <p className="text-gray-700 font-medium">
                    Click to upload or drag and drop
                  </p>
                  <p className="text-sm text-gray-500 mt-1">PDF files only</p>
                </div>
              </div>
            ) : (
              <div className="space-y-4 cursor-pointer">
                <FileText className="mx-auto h-12 w-12 text-primary" />
                <div>
                  <p className="text-gray-700 font-medium">{file.name}</p>
                  <p className="text-sm text-gray-500 mt-1">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
            )}
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <button
            onClick={handleUpload}
            disabled={!file || loading}
            className="w-full bg-[rgba(17,11,196,1)] hover:bg-[rgba(12,8,147,1)] active:bg-[rgba(10,6,120,1)] text-white font-semibold py-3 px-6 rounded-xl hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin h-5 w-5" />
                <span>Calculating...</span>
              </>
            ) : (
              <span>Calculate Score</span>
            )}
          </button>

          <div className="text-center">
            <button
              onClick={handleTrySample}
              disabled={loading}
              className="text-sm text-blue-600 hover:text-blue-800 underline disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center mx-auto space-x-1"
            >
              <TestTube className="h-4 w-4" />
              <span>Try with sample response sheet</span>
            </button>
          </div>
        </div>

        {/* How to Download Section */}
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <Download className="h-6 w-6 mr-2" />
            How to Download Your Response Sheet
          </h2>
          <div className="space-y-4 text-gray-700">
            <div className="space-y-2">
              <p className="font-semibold text-gray-900">Step 1: Visit the CEED Portal</p>
              <p className="text-sm">Go to the official CEED exam portal and log in with your credentials.</p>
            </div>
            <div className="space-y-2">
              <p className="font-semibold text-gray-900">Step 2: Navigate to Response Sheet</p>
              <p className="text-sm">Find the "Download Response Sheet" or "View Response" section in your candidate dashboard.</p>
            </div>
            <div className="space-y-2">
              <p className="font-semibold text-gray-900">Step 3: Download as PDF</p>
              <p className="text-sm">Download your response sheet in PDF format. This is the file you'll upload here.</p>
            </div>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-4">
              <p className="text-sm text-blue-900">
                <strong>Note:</strong> Make sure the PDF contains your marked responses with clear question numbers and selected options.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;
