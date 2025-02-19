import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { TextField, IconButton, Paper, Typography } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import './PremiumChat.css';

const PremiumChat: React.FC = () => {
    const [messages, setMessages] = useState<Array<{text: string; isBot: boolean}>>([]);
    const [input, setInput] = useState('');
    const messagesEndRef = useRef<null | HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        setMessages(prev => [...prev, { text: input, isBot: false }]);
        
        try {
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input, language: 'he' })
            });
            const data = await response.json();
            
            setMessages(prev => [...prev, { text: data.response, isBot: true }]);
        } catch (error) {
            console.error('Error:', error);
        }

        setInput('');
    };

    return (
        <Paper elevation={3} className="premium-chat-container">
            <div className="premium-chat-header">
                <Typography variant="h4" component="h1">
                    Movne Investment Advisor
                </Typography>
                <Typography variant="subtitle1">
                    Your Personal Financial Guide
                </Typography>
            </div>

            <div className="premium-chat-messages">
                <AnimatePresence>
                    {messages.map((msg, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0 }}
                            className={`message ${msg.isBot ? 'bot' : 'user'}`}
                        >
                            <Paper elevation={1} className="message-content">
                                {msg.text}
                            </Paper>
                        </motion.div>
                    ))}
                </AnimatePresence>
                <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSubmit} className="premium-chat-input">
                <TextField
                    fullWidth
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask about investment opportunities..."
                    variant="outlined"
                    dir="rtl"
                />
                <IconButton type="submit" color="primary" size="large">
                    <SendIcon />
                </IconButton>
            </form>
        </Paper>
    );
};

export default PremiumChat;
