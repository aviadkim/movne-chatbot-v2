const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const chatAPI = {
    sendMessage: async (message, language = 'he') => {
        try {
            const response = await fetch(`${API_URL}/api/v1/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message,
                    language,
                }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }
};
