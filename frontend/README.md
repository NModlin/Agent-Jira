# Jira Cheer Dashboard - Frontend

React-based frontend for the AI-Powered Jira Dashboard with LangSmith Agent.

## Features

- **Modern UI**: Beautiful, responsive chat interface
- **Real-time Chat**: Communicate with the AI agent
- **Suggested Queries**: Quick-start buttons for common questions
- **Loading States**: Visual feedback during agent processing
- **Error Handling**: Graceful error messages

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start the Development Server

Make sure both backend servers are running first:

```bash
# Terminal 1 - Jira Tool Server
cd jira-tool-server
python app.py

# Terminal 2 - Agent Server
cd agent-server
python app.py

# Terminal 3 - Frontend
cd frontend
npm run dev
```

The frontend will start on `http://localhost:3000`

### 3. Open in Browser

Navigate to `http://localhost:3000` and start chatting with your Jira AI assistant!

## Architecture

The frontend is built with:
- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **Lucide React**: Beautiful icon library
- **CSS Modules**: Scoped styling

### Component Structure

```
src/
├── components/
│   ├── JiraDashboard.jsx    # Main dashboard component
│   └── JiraDashboard.css    # Dashboard styles
├── App.jsx                   # Root component
├── main.jsx                  # Entry point
└── index.css                 # Global styles
```

## API Integration

The frontend communicates with the Agent Server via:

```javascript
POST /api/agent/chat
{
  "query": "How many bugs do we have?"
}
```

Response:
```javascript
{
  "response": "We currently have 12 open bugs...",
  "query": "How many bugs do we have?"
}
```

## Customization

### Adding New Suggested Queries

Edit `JiraDashboard.jsx`:

```javascript
const suggestedQueries = [
  "How many bugs do we have?",
  "What is Alice Smith working on?",
  "Show me our team progress",
  "Your new query here"
];
```

### Changing Colors

Edit the CSS variables in `JiraDashboard.css` or `index.css` to match your brand colors.

### Modifying the Welcome Message

Edit the initial message in `JiraDashboard.jsx`:

```javascript
const [messages, setMessages] = useState([
  {
    id: 1,
    type: 'ai',
    text: 'Your custom welcome message here!'
  }
]);
```

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` directory.

To preview the production build:

```bash
npm run preview
```

## Troubleshooting

### "Failed to fetch" errors

- Ensure the Agent Server is running on port 5002
- Check the proxy configuration in `vite.config.js`
- Verify CORS is enabled on the Agent Server

### Blank screen

- Check the browser console for errors
- Ensure all dependencies are installed (`npm install`)
- Try clearing the browser cache

### Styling issues

- Make sure `JiraDashboard.css` is imported in `JiraDashboard.jsx`
- Check that `index.css` is imported in `main.jsx`

## Future Enhancements

- **Streaming Responses**: Use Server-Sent Events for real-time streaming
- **Message History**: Persist conversation history
- **Rich Formatting**: Support markdown in responses
- **Voice Input**: Add speech-to-text capability
- **Dark Mode**: Theme toggle

