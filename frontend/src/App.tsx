import React, { useState, useEffect } from 'react';
import { onAuthStateChanged, User } from 'firebase/auth';
import { auth, signInWithGoogle, logout } from './firebase';
import { transcribeAudio, matchSentence, getTranscriptionLogs, getMemorizationStats } from './api';
import AudioRecorder from './components/AudioRecorder';
import { TranscriptionLog, MemorizationStat, MatchSentenceResponse } from './api';

interface AppState {
  user: User | null;
  loading: boolean;
  transcription: string;
  matchResult: MatchSentenceResponse | null;
  isProcessing: boolean;
  logs: TranscriptionLog[];
  stats: MemorizationStat[];
}

function App() {
  const [state, setState] = useState<AppState>({
    user: null,
    loading: true,
    transcription: '',
    matchResult: null,
    isProcessing: false,
    logs: [],
    stats: []
  });

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setState(prev => ({ ...prev, user, loading: false }));
      if (user) {
        loadUserData();
      }
    });

    return unsubscribe;
  }, []);

  const loadUserData = async () => {
    try {
      const [logs, stats] = await Promise.all([
        getTranscriptionLogs(10),
        getMemorizationStats()
      ]);
      setState(prev => ({ ...prev, logs, stats }));
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  };

  const handleSignIn = async () => {
    const user = await signInWithGoogle();
    if (user) {
      setState(prev => ({ ...prev, user }));
    }
  };

  const handleSignOut = async () => {
    await logout();
    setState(prev => ({ 
      ...prev, 
      user: null, 
      transcription: '', 
      matchResult: null, 
      logs: [], 
      stats: [] 
    }));
  };

  const handleRecordingComplete = async (audioBlob: Blob) => {
    setState(prev => ({ ...prev, isProcessing: true, transcription: '', matchResult: null }));
    
    try {
      // Step 1: Transcribe audio
      const transcribeResult = await transcribeAudio(audioBlob);
      setState(prev => ({ ...prev, transcription: transcribeResult.transcription }));

      // Step 2: Match sentence to ayah
      if (transcribeResult.success && transcribeResult.transcription) {
        const matchResult = await matchSentence(transcribeResult.transcription);
        setState(prev => ({ ...prev, matchResult }));

        // Reload user data to get updated logs and stats
        await loadUserData();
      }
    } catch (error) {
      console.error('Error processing audio:', error);
      alert('Error processing audio. Please try again.');
    } finally {
      setState(prev => ({ ...prev, isProcessing: false }));
    }
  };

  if (state.loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-100 to-white flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    );
  }

  if (!state.user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-100 to-white flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-xl max-w-md w-full mx-4">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-green-800 mb-2">Dhikra</h1>
            <p className="text-gray-600 mb-6">Qur'an Memorization Assistant</p>
            <button
              onClick={handleSignIn}
              className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200"
            >
              Sign in with Google
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-100 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-green-800">Dhikra</h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">
              Welcome, {state.user.displayName || state.user.email}
            </span>
            <button
              onClick={handleSignOut}
              className="text-green-600 hover:text-green-800 transition-colors duration-200"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recording Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Record Your Recitation</h2>
            
            <AudioRecorder 
              onRecordingComplete={handleRecordingComplete}
              isProcessing={state.isProcessing}
            />

            {/* Transcription Result */}
            {state.transcription && (
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <h3 className="font-medium text-gray-800 mb-2">Transcription:</h3>
                <p className="text-gray-700">{state.transcription}</p>
              </div>
            )}

            {/* Match Result */}
            {state.matchResult && (
              <div className="mt-6 p-6 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl border border-green-200 shadow-sm">
                <h3 className="font-semibold text-green-900 mb-4 flex items-center">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                  Matched Ayah
                </h3>
                
                {state.matchResult.matched_ayah ? (
                  <div className="space-y-4">
                    {/* Surah and Ayah Info */}
                    <div className="flex justify-between items-center bg-white rounded-lg p-4 shadow-sm">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                          <span className="text-green-700 font-bold text-sm">📖</span>
                        </div>
                        <div>
                          <p className="text-lg font-semibold text-gray-900">
                            Surah {state.matchResult.surah}, Ayah {state.matchResult.ayah}
                          </p>
                          <p className="text-sm text-gray-500">
                            {state.matchResult.surah === 1 ? "Al-Fatiha" : 
                             state.matchResult.surah === 2 ? "Al-Baqarah" :
                             state.matchResult.surah === 3 ? "Al-Imran" :
                             `Surah ${state.matchResult.surah}`}
                          </p>
                        </div>
                      </div>
                      <div className="text-center">
                        <div className="inline-flex items-center px-3 py-2 bg-green-500 text-white rounded-full text-sm font-medium">
                          <span className="mr-1">✨</span>
                          {(state.matchResult.similarity_score * 100).toFixed(1)}% match
                        </div>
                      </div>
                    </div>
                    
                    {/* Arabic Text */}
                    {state.matchResult.arabic_text && (
                      <div className="bg-white rounded-lg p-6 shadow-sm border-r-4 border-green-400">
                        <p className="arabic-text text-2xl text-gray-800 leading-relaxed text-center mb-2">
                          {state.matchResult.arabic_text}
                        </p>
                        <div className="text-center">
                          <span className="inline-block w-8 h-0.5 bg-gradient-to-r from-green-300 to-emerald-300 rounded"></span>
                        </div>
                      </div>
                    )}
                    
                    {/* English Translation */}
                    {state.matchResult.english_text && (
                      <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-gray-300">
                        <p className="text-gray-700 italic leading-relaxed">
                          {state.matchResult.english_text}
                        </p>
                      </div>
                    )}

                    {/* Success Message */}
                    <div className="flex items-center justify-center space-x-2 text-green-600 bg-green-50 rounded-lg py-3">
                      <span className="text-lg">🎉</span>
                      <span className="font-medium">Great job! Ayah successfully identified</span>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-6">
                    <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
                      <span className="text-2xl">🔍</span>
                    </div>
                    <p className="text-gray-600">No matching ayah found. Try reciting more clearly.</p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* History and Stats Section */}
          <div className="space-y-6">
            {/* Recent Attempts */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Attempts</h2>
              
              {state.logs.length > 0 ? (
                <div className="space-y-3 max-h-64 overflow-y-auto">
                  {state.logs.map((log) => (
                    <div key={log.id} className="p-3 border border-gray-200 rounded">
                      <div className="flex justify-between items-start mb-1">
                        <span className="text-sm font-medium text-gray-800">
                          {log.matched_ayah || 'No match'}
                        </span>
                        <span className="text-xs text-gray-500">
                          {new Date(log.created_at).toLocaleDateString()}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 truncate">{log.transcription_text}</p>
                      {log.similarity_score && (
                        <span className="text-xs text-green-600">
                          {(log.similarity_score * 100).toFixed(1)}% similarity
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-4">No attempts yet. Start recording!</p>
              )}
            </div>

            {/* Memorization Stats */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Memorization Progress</h2>
              
              {state.stats.length > 0 ? (
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {state.stats.slice(0, 10).map((stat, index) => (
                    <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                      <span className="text-sm font-medium">
                        Surah {stat.surah}, Ayah {stat.ayah}
                      </span>
                      <span className="text-sm text-green-600">
                        {stat.times_attempted} attempt{stat.times_attempted !== 1 ? 's' : ''}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-4">No progress yet. Start practicing!</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
