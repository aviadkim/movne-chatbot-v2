import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, Send, Globe, Loader2, User, Clock } from 'lucide-react';

const LuxuryChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [language, setLanguage] = useState('he');
  const [clientId, setClientId] = useState(null);
  const messagesEndRef = useRef(null);

  // Elegant Glass Effect Classes
  const glassEffect = "backdrop-filter backdrop-blur-lg bg-white/30 border border-white/20";
  const luxuryGradient = "bg-gradient-to-r from-slate-900 via-purple-900 to-slate-900";
  const goldAccent = "text-amber-400";

  useEffect(() => {
    // זיהוי או יצירת מזהה לקוח
    const storedId = localStorage.getItem('clientId');
    if (storedId) {
      setClientId(storedId);
    } else {
      const newId = `client_${Date.now()}`;
      localStorage.setItem('clientId', newId);
      setClientId(newId);
    }
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    try {
      setLoading(true);
      setError(null);
      
      const userMessage = {
        type: 'user',
        content: input,
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, userMessage]);
      setInput('');

      const response = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          client_id: clientId,
          language: language
        }),
      });

      if (!response.ok) throw new Error('API request failed');

      const data = await response.json();
      
      const botMessage = {
        type: 'assistant',
        content: data.response,
        timestamp: data.timestamp
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString(language === 'he' ? 'he-IL' : 'en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className={`min-h-screen ${luxuryGradient} py-8 px-4 md:px-0`} dir={language === 'he' ? 'rtl' : 'ltr'}>
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className={`${glassEffect} rounded-t-2xl p-6 flex items-center justify-between`}>
          <div className="flex items-center gap-4">
            <div className={`w-12 h-12 rounded-full ${goldAccent} flex items-center justify-center`}>
              <MessageCircle className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-semibold text-white">
                {language === 'he' ? 'מובנה גלובל' : 'Movne Global'}
              </h1>
              <p className={`text-sm ${goldAccent}`}>
                {language === 'he' ? 'שירות לקוחות מתקדם' : 'Advanced Customer Service'}
              </p>
            </div>
          </div>
          <button
            onClick={() => setLanguage(prev => prev === 'he' ? 'en' : 'he')}
            className={`p-3 rounded-full ${glassEffect} hover:bg-white/40 transition-all duration-300`}
          >
            <Globe className="w-5 h-5 text-white" />
          </button>
        </div>

        {/* Chat Container */}
        <div className={`${glassEffect} h-[600px] flex flex-col`}>
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} items-end gap-2`}
              >
                {message.type === 'assistant' && (
                  <div className={`w-8 h-8 rounded-full ${goldAccent} flex items-center justify-center`}>
                    <User className="w-4 h-4" />
                  </div>
                )}
                <div className={`relative max-w-[80%] ${
                  message.type === 'user'
                    ? 'bg-purple-600 text-white rounded-l-xl rounded-tr-xl'
                    : `${glassEffect} text-white rounded-r-xl rounded-tl-xl`
                } p-4 shadow-lg`}>
                  {message.content}
                  <div className={`absolute ${message.type === 'user' ? '-left-16' : '-right-16'} bottom-0 flex items-center gap-1 text-xs text-gray-400`}>
                    <Clock className="w-3 h-3" />
                    {formatTimestamp(message.timestamp)}
                  </div>
                </div>
                {message.type === 'user' && (
                  <div className={`w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center`}>
                    <User className="w-4 h-4 text-white" />
                  </div>
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {error && (
            <div className="p-4 mx-4 mb-4 rounded-lg bg-red-500/20 border border-red-500/30">
              <p className="text-red-200">
                {language === 'he' 
                  ? 'אירעה שגיאה. אנא נסה שוב.'
                  : 'An error occurred. Please try again.'}
              </p>
            </div>
          )}

          {/* Input Area */}
          <form onSubmit={handleSubmit} className="p-4 border-t border-white/20">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={
                  language === 'he'
                    ? 'הקלד את שאלתך כאן...'
                    : 'Type your question here...'
                }
                disabled={loading}
                className={`flex-1 p-4 rounded-xl ${glassEffect} text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500`}
              />
              <button
                type="submit"
                disabled={loading}
                className={`p-4 rounded-xl ${goldAccent} hover:bg-amber-500 transition-colors duration-300 disabled:opacity-50`}
              >
                {loading ? (
                  <Loader2 className="w-6 h-6 animate-spin" />
                ) : (
                  <Send className="w-6 h-6" />
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LuxuryChatInterface;
