App.jsx
import { useState, useEffect } from 'react';
import AppBar from './components/AppBar';
import ChatInterface from './components/ChatInterface';
import EvidenceChecklist from './components/EvidenceChecklist';
import CaseNotes from './components/CaseNotes';
import decisionTree from './data/decisionTree.json';
import { useTranslation } from 'react-i18next';
import './App.css';

function App() {
  const { t } = useTranslation();
  const [messages, setMessages] = useState([]);
  const [currentStep, setCurrentStep] = useState('start');
  const [checklist, setChecklist] = useState([]);
  const [isAiChatActive, setAiChatActive] = useState(false);
  const [userInput, setUserInput] = useState('');

  // Initialize the chat on component mount or language change
  useEffect(() => {
    const initialMessage = decisionTree.start;
    const initialBotMessage = {
      sender: 'bot',
      text: t(initialMessage.query, { defaultValue: initialMessage.query }),
      options: initialMessage.options.map(opt => ({
        ...opt,
        label: t(opt.label, { defaultValue: opt.label })
      }))
    };
    setMessages([initialBotMessage]);
  }, [t]);

  const handleUserInputSubmit = async (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    const userMessage = { sender: 'officer', text: userInput };
    setMessages(prev => [...prev, userMessage]);
    setUserInput('');

    // --- API Call to Python Backend ---
    try {
      const response = await fetch('http://localhost:5000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userInput }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const botMessage = { sender: 'bot', text: data.response };
      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error("Failed to fetch from AI:", error);
      const errorMessage = { sender: 'bot', text: "Sorry, I'm having trouble connecting to the AI assistant." };
      setMessages(prev => [...prev, errorMessage]);
    }
  };


  const handleOptionSelect = (optionValue) => {
    if (optionValue === 'Other') {
        setAiChatActive(true);
        const nextStep = decisionTree.aiChatStart;
        const botMessage = {
            sender: 'bot',
            text: t(nextStep.query, { defaultValue: nextStep.query }),
            options: [] // No options in AI mode
        };
        const officerMessage = { sender: 'officer', text: 'Other' };
        setMessages(prev => [...prev, officerMessage, botMessage]);
        setCurrentStep('aiChatStart');
        return;
    }


    // Add the officer's selection to the chat messages
    const officerMessage = {
      sender: 'officer',
      text: t(optionValue, { defaultValue: optionValue })
    };
    setMessages((prevMessages) => [...prevMessages, officerMessage]);

    const nextStepKey = decisionTree[currentStep]?.options.find(opt => opt.value === optionValue)?.nextStep;

    if (optionValue === 'New Case') {
      setAiChatActive(false); // Deactivate AI mode
      setCurrentStep('start');
      setChecklist([]);
      setTimeout(() => {
        const initialMessage = decisionTree.start;
        const initialBotMessage = {
          sender: 'bot',
          text: t(initialMessage.query, { defaultValue: initialMessage.query }),
          options: initialMessage.options.map(opt => ({
            ...opt,
            label: t(opt.label, { defaultValue: opt.label })
          }))
        };
        setMessages([initialBotMessage]);
      }, 500);
      return;
    }

    if (nextStepKey) {
      const nextStep = decisionTree[nextStepKey];
      const botMessage = {
        sender: 'bot',
        text: t(nextStep.query, { defaultValue: nextStep.query }),
        options: nextStep.options.map(opt => ({
          ...opt,
          label: t(opt.label, { defaultValue: opt.label })
        })),
        templateContent: nextStep.templateContent
      };

      if (nextStep.checklist) {
        const translatedChecklist = nextStep.checklist.map(item => t(item, { defaultValue: item }));
        setChecklist(translatedChecklist);
      } else {
        setChecklist([]);
      }

      setTimeout(() => {
        setMessages((prevMessages) => [...prevMessages, botMessage]);
        setCurrentStep(nextStepKey);
      }, 500);
    }
  };

  return (
    <div className="app-container">
      <AppBar />
      <div className="content-area">
        <div className="chatbot-container">
          <ChatInterface
            messages={messages}
            onSelectOption={handleOptionSelect}
            currentOptions={isAiChatActive ? [] : (messages.length > 0 ? messages[messages.length - 1].options : [])}
          />
          {isAiChatActive && (
            <form onSubmit={handleUserInputSubmit} className="user-input-form">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Ask the AI assistant..."
                className="user-input"
              />
              <button type="submit" className="send-button">Send</button>
            </form>
          )}
        </div>
        <div className="assistance-panel">
          <EvidenceChecklist checklist={checklist} />
          <CaseNotes />
        </div>
      </div>
    </div>
  );
}

export default App;