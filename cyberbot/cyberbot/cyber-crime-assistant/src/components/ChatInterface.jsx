import { useEffect, useRef } from 'react';
import './ChatInterface.css';

const ChatInterface = ({ messages, onSelectOption, currentOptions }) => {
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chat-interface">
      <div className="message-list">
        {messages.map((msg, index) => (
          <div key={index}>
            <div className={`message-bubble ${msg.sender}`}>
              <p>{msg.text}</p>
            </div>
            {msg.templateContent && (
              <pre className="template-box">{msg.templateContent}</pre>
            )}
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <div className="options-container">
        {currentOptions?.map((option, index) => (
          <button
            key={index}
            className="option-button"
            onClick={() => onSelectOption(option.value)}
          >
            {option.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ChatInterface;