import axios from 'axios';
import { getIdToken } from './firebase';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  async (config) => {
    const token = await getIdToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Types for API responses
export interface TranscribeResponse {
  transcription: string;
  success: boolean;
  message: string;
}

export interface MatchSentenceResponse {
  matched_ayah: string | null;
  similarity_score: number;
  surah: number | null;
  ayah: number | null;
  arabic_text: string;
  english_text: string;
  success: boolean;
}

export interface TranscriptionLog {
  id: string;
  transcription_text: string;
  matched_ayah: string | null;
  similarity_score: number | null;
  created_at: string;
}

export interface MemorizationStat {
  surah: number;
  ayah: number;
  times_attempted: number;
  last_attempted: string;
}

// API functions
export const transcribeAudio = async (audioBlob: Blob): Promise<TranscribeResponse> => {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.wav');
  
  const response = await api.post('/api/transcribe', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const matchSentence = async (sentence: string): Promise<MatchSentenceResponse> => {
  const response = await api.post('/api/match_sentence', { sentence });
  return response.data;
};

export const getTranscriptionLogs = async (limit: number = 50): Promise<TranscriptionLog[]> => {
  const response = await api.get(`/api/transcription_logs?limit=${limit}`);
  return response.data;
};

export const getMemorizationStats = async (surah?: number): Promise<MemorizationStat[]> => {
  const params = surah ? `?surah=${surah}` : '';
  const response = await api.get(`/api/memorization_stats${params}`);
  return response.data;
};

export const healthCheck = async (): Promise<{ status: string; service: string }> => {
  const response = await api.get('/api/health');
  return response.data;
}; 