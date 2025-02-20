import React, { useState, useEffect } from 'react';
import { TextField, Button, Paper, Typography, Box, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

interface Message {
  text: string;
  isBot: boolean;
}

const API_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:8000'
  : 'https://movne-chatbot-v2-production.up.railway.app';

const API_HEALTH_URL = `${API_URL}/health`;

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch(API_HEALTH_URL);
        if (!response.ok) {
          setError('השרת אינו זמין כרגע. אנא נסה שוב מאוחר יותר. / Server is currently unavailable. Please try again later.');
        }
      } catch (err) {
        setError('לא ניתן להתחבר לשרת. אנא בדוק את החיבור שלך. / Cannot connect to server. Please check your connection.');
      }
    };
    checkHealth();
  }, []);
  const detectLanguage = (text: string): string => {
    const hebrewPattern = /[\u0590-\u05FF]/;
    return hebrewPattern.test(text) ? 'he' : 'en';
  };
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
  const userMessage = { text: input, isBot: false };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);
  try {
      const response = await fetch(`${API_URL}/api/v1/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, language: detectLanguage(input) })
      });
  if (!response.ok) {
        throw new Error('שגיאה בתקשורת עם השרת / Error communicating with server');
      }
  const data = await response.json();
      setMessages(prev => [...prev, { text: data.response, isBot: true }]);
    } catch (err) {
      setError('שגיאה: לא ניתן להתחבר לשרת / Error: Cannot connect to server');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <Paper elevation={3} sx={{
      p: 4,
      height: '85vh',
      display: 'flex',
      flexDirection: 'column',
      bgcolor: '#f8fafc',
      borderRadius: 2,
      boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)'
    }}>
      <Typography variant="h4" component="h1" gutterBottom align="center" sx={{
        fontWeight: 600,
        color: '#1e293b',
        mb: 3
      }}>
        Movne Investment Advisor
      </Typography>
      <Typography variant="subtitle1" align="center" sx={{ mb: 4, color: '#64748b' }}>
        Your Premium Financial Guide
      </Typography>
        {messages.map((msg, index) => (
          <Box
            key={index}
            sx={{
              display: 'flex',
              justifyContent: msg.isBot ? 'flex-start' : 'flex-end',
              mb: 2.5
            }}
          >
            <Paper
              elevation={1}
              sx={{
                p: 2.5,
                maxWidth: '75%',
                bgcolor: msg.isBot ? '#f1f5f9' : '#2563eb',
                color: msg.isBot ? '#334155' : '#fff',
                borderRadius: 2,
                boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)'
              }}
            >
              <Typography sx={{ fontSize: '1rem', lineHeight: 1.6 }}>{msg.text}</Typography>
            </Paper>
          </Box>
        ))}
        {error && (
          <Typography color="error" align="center" sx={{ mt: 2 }}>
            {error}
          </Typography>
        )}
      </Box>

      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '1rem' }}>
        <TextField
          fullWidth
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="הקלד הודעה כאן..."
          disabled={isLoading}
          dir="rtl"
        />
        <Button
          type="submit"
          variant="contained"
          endIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <SendIcon />}
          disabled={isLoading}
        >
          שלח
        </Button>
      </form>
    </Paper>
  );
};

export default ChatInterface;