import React, { useState, FormEvent } from 'react';
import './Chat.css';

// Define API URL based on environment
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000'
  : 'https://movne-chatbot-v2-production.up.railway.app';

interface Message {
    text: string;
    isBot: boolean;
}

const Chat: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!input.trim()) return;

        setMessages(prev => [...prev, { text: input, isBot: false }]);

        try {
            const response = await fetch(`${API_URL}/api/chat`, {
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
        <div className="chat-container">
            <div className="chat-header">
                <h1>Movne Investment Advisor - יועץ השקעות מובנות</h1>
                <p className="subtitle">Your Personal Guide to Structured Investment Products</p>
            </div>
            <div className="chat-messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.isBot ? 'bot' : 'user'}`} dir="rtl">
                        {msg.text}
                    </div>
                ))}
            </div>
            <form onSubmit={handleSubmit} className="chat-input-form">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="הקלד/י שאלה כאן..."
                    dir="rtl"
                />
                <button type="submit">שלח</button>
            </form>
        </div>
    );
};

export default Chat;
