import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useNavigate } from 'react-router-dom';

import MessageItem from './MessageItem';
import ThinkingIndicator from './ThinkingIndicator';
import WelcomeScreen from './WelcomeScreen';
import ChatInput from './ChatInput';
import AnimationStyles from './AnimationStyles';
import { Message } from './types';
import { getTimestamp, getOrCreateUserUUID } from './utils';
import { fetchUserProfile } from '@/api/fetchUserProfile';

// Base URL loaded from environment variables (Vite or CRA fallback).
// In development, default to relative '/api' to use the frontend proxy for API calls.
const BASE_URL =
  import.meta.env?.VITE_API_BASE_URL || import.meta.env?.VITE_BACKEND_URL ||
  process.env.REACT_APP_API_BASE_URL || process.env.REACT_APP_BACKEND_URL ||
  '/api';

// Remove unused interface to fix the warning
export interface RagChatViewProps {}

export default function RagChatView(props: RagChatViewProps) {
  const navigate = useNavigate();
  const { user, idToken } = useAuth();

  const [uuid, setUUID] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  // Keep avatar state for ChatInput component compatibility
  const [avatar, setAvatar] = useState('chappelle');

  const setActiveView = (view: string) => {
    console.log('Navigating to view:', view);
    navigate(`/${view}`);
  };

  const bottomRef = useRef<HTMLDivElement>(null);
  const isInitialLoad = useRef(true);

  const [typingSpeed] = useState(8);
  const [typingChunkSize] = useState(2);
  const [typingVariability] = useState(true);

  useEffect(() => {
    setUUID(getOrCreateUserUUID());
  }, []);

  useEffect(() => {
    if (!uuid) return;
    (async () => {
      try {
        console.log(`Fetching memory from ${BASE_URL}/storage/memory/get/${uuid}`);
        // Fetch memory from storage service according to docs
        const res = await fetch(`${BASE_URL}/storage/memory/get/${uuid}`, {
          headers: { 
            Authorization: `Bearer foo`, // Use the development token
            'Content-Type': 'application/json',
          },
        });
        
        if (!res.ok) {
          const errorText = await res.text();
          console.error(`Server responded with ${res.status}:`, errorText);
          return;
        }
        
        const contentType = res.headers.get('content-type');
        console.log('Memory response content type:', contentType);
        
        if (!contentType || !contentType.includes('application/json')) {
          const textResponse = await res.text();
          console.error('Memory response is not JSON:', textResponse);
          return;
        }
        
        const data = await res.json();
        console.log('Received memory data:', data);
        
        // Handle different potential response formats
        if (Array.isArray(data)) {
          // Format from docs: array of {role, content} objects
          if (data.length > 0 && data[0].role && data[0].content) {
            try {
              // Make sure we create valid Message objects that match our type
              const convertedMessages: Message[] = data.map(item => ({
                sender: item.role === 'user' ? 'user' : 'assistant',
                text: item.content,
                timestamp: getTimestamp(),
              }));
              console.log('Converted messages:', convertedMessages);
              setMessages(convertedMessages);
            } catch (convErr) {
              console.error('Error converting messages:', convErr);
            }
          }
        } else if (typeof data === 'object' && data !== null) {
          // Alternative format: {messages: [...]}
          if (data.messages && Array.isArray(data.messages)) {
            try {
              console.log('Using messages from response:', data.messages);
              setMessages(data.messages);
            } catch (msgErr) {
              console.error('Error setting messages from response:', msgErr);
            }
          }
        }
      } catch (err) {
        console.error('❌ Error fetching session memory:', err);
      }
    })();
  }, [uuid]);

  useEffect(() => {
    if (messages.length > 0) {
      const scrollBehavior = isInitialLoad.current ? 'auto' : 'smooth';
      bottomRef.current?.scrollIntoView({ behavior: scrollBehavior });
      isInitialLoad.current = false;
    }
  }, [messages, isTyping]);

  useEffect(() => {
    const typingMessage = messages.find((m) => m.isTyping);
    if (!typingMessage) return;

    const fullText = typingMessage.fullText || '';
    const currentText = typingMessage.text || '';

    if (currentText.length >= fullText.length) {
      setMessages((prev) => prev.map((m) => (m.isTyping ? { ...m, isTyping: false } : m)));
      return;
    }

    const charsToAdd = Math.min(typingChunkSize, fullText.length - currentText.length);
    const newText = fullText.substring(0, currentText.length + charsToAdd);
    const nextChar = fullText[currentText.length];
    let adjustedSpeed = typingSpeed;

    if (typingVariability && nextChar) {
      if ('.!?'.includes(nextChar)) adjustedSpeed *= 4;
      else if (',;:'.includes(nextChar)) adjustedSpeed *= 2;
      else if (nextChar === ' ' && Math.random() < 0.1) adjustedSpeed *= 1.5;
    }

    const timer = setTimeout(() => {
      setMessages((prev) => prev.map((m) => (m.isTyping ? { ...m, text: newText } : m)));
    }, adjustedSpeed);

    return () => clearTimeout(timer);
  }, [messages, typingSpeed, typingChunkSize, typingVariability]);

  const sendMessage = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;

    // Add user message immediately for better UX
    const userMessage: Message = {
      sender: 'user',
      text: trimmed,
      timestamp: getTimestamp(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      // Use the RAG endpoint via the same API base path (proxed in development).
      const ragUrl = `${BASE_URL}/rag/query?prompt=${encodeURIComponent(trimmed)}`;
      console.log(`Using RAG service: ${ragUrl}`);
      
      const ragRes = await fetch(ragUrl, {
        headers: {
          'Authorization': 'Bearer foo'
        }
      });
      
      if (!ragRes.ok) {
        throw new Error(`RAG service returned ${ragRes.status}`);
      }
      
      const ragData = await ragRes.json();
      
      // Build a dynamic, context-aware response based on the query
      let responseText = '';
      const fullText = (ragData.result || '').trim();
      const lowerQuery = trimmed.toLowerCase();

      if (ragData.result) {
        // Definition queries (e.g., "what is X", "definition of X")
        if (lowerQuery.includes('what is') || lowerQuery.includes('definition of')) {
          const conceptMatch = lowerQuery.match(/what is ([^?]+)|definition of ([^?]+)/i);
          const concept = conceptMatch ? (conceptMatch[1] || conceptMatch[2]).trim() : '';
          const paragraphs = fullText.split('\n\n');
          if (concept && fullText.toLowerCase().includes(concept.toLowerCase())) {
            const relevant = paragraphs.filter((p: string) =>
              p.toLowerCase().includes(concept.toLowerCase()) && p.length > 50 && !p.includes(': ')
            );
            if (relevant.length) {
              responseText = `${concept.charAt(0).toUpperCase() + concept.slice(1)} refers to ${relevant[0].trim()}`;
            } else {
              const sentences = fullText.split(/[.!?]/).filter((s: string) => s.trim().length > 0);
              const rs = sentences.filter((s: string) => s.toLowerCase().includes(concept.toLowerCase()) && s.length > 20);
              if (rs.length) {
                responseText = `${concept.charAt(0).toUpperCase() + concept.slice(1)} refers to ${rs[0].trim()}.`;
                if (rs[1]) responseText += ` ${rs[1].trim()}.`;
              } else {
                const defPara = paragraphs.find((p: string) => p.includes(': ') || p.includes(' is ') || p.includes(' are '));
                responseText = (defPara || paragraphs[0] || fullText).trim();
              }
            }
          } else {
            responseText = paragraphs[0] || fullText;
          }
        }
        // Instructional ("how to") queries
        else if (lowerQuery.includes('how to')) {
          const actionMatch = lowerQuery.match(/how to ([^?]+)/i);
          const action = actionMatch ? actionMatch[1].trim() : '';
          const paragraphs = fullText.split('\n\n');
          const instr = paragraphs.filter((p: string) =>
            (p.includes('•') || p.includes(':') || p.toLowerCase().includes('step') ||
             p.toLowerCase().includes('try') || p.toLowerCase().includes('practice')) &&
            p.length > 40
          );
          responseText = instr.length
            ? `Here's how you can ${action}:\n\n${instr.slice(0, 2).join('\n\n')}`
            : `To ${action}, consider this information:\n\n${paragraphs[0]}`;
        }
        // Personal context queries
        else if (lowerQuery.includes('my') || lowerQuery.includes(' i ') || lowerQuery.includes(' me')) {
          const intro = "I don't have access to your specific profile information. To get your personal Multiple Natures profile, you would need to take the assessment. However, I can provide general information about how Multiple Natures traits work together:\n\n";
          const paragraphs = fullText.split('\n\n');
          const rel = paragraphs.filter((p: string) => (p.includes('High') || p.includes('Facet') || p.includes('Nature')) && p.length > 40);
          responseText = intro + (rel.length ? rel.slice(0, 2).join('\n\n') : "Multiple Natures helps you understand your natural behavioral traits and how they can be applied to find alignment in your life and work. Consider taking the assessment to discover your unique profile.");
        }
        // Default fallback for other queries
        else {
          const paragraphs = fullText.split('\n\n').filter((p: string) => p.trim().length > 40 && !p.includes(':') && !p.startsWith('•'));
          responseText = paragraphs.length
            ? paragraphs.slice(0, 2).join('\n\n')
            : fullText.split('\n\n').find((p: string) => p.trim().length > 40) || fullText.substring(0, 300);
        }

        // Add conversational intro
        if (lowerQuery.includes('how')) {
          responseText = `Here's what I can tell you:\n\n${responseText}`;
        } else if (!lowerQuery.includes('what is') && !lowerQuery.includes('definition')) {
          responseText = `Based on the Multiple Natures framework:\n\n${responseText}`;
        }

        // Cleanup whitespace and ensure punctuation
        responseText = responseText.trim().replace(/\n{3,}/g, '\n\n').replace(/\s{2,}/g, ' ');
        if (!['.', '!', '?', ':'].some(ch => responseText.endsWith(ch))) {
          responseText += '.';
        }
      } else {
        responseText = "I'm sorry, I don't have enough information to answer that question about Multiple Natures.";
      }
      
      // Add assistant response
      const assistantMessage: Message = {
        sender: 'assistant',
        text: '',
        fullText: responseText,
        isTyping: true,
        timestamp: getTimestamp(),
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      
      // Save the conversation to memory
      try {
        const memoryData = {
          userId: uuid,
          sessionId: uuid,
          messages: [
            { role: 'user', content: trimmed },
            { role: 'assistant', content: responseText }
          ]
        };
        
        await fetch(`${BASE_URL}/storage/memory/save`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer foo'
          },
          body: JSON.stringify(memoryData)
        });
        
        console.log('Conversation saved to memory');
      } catch (memErr) {
        console.warn('Failed to save to memory:', memErr);
      }
    } catch (err: any) {
      console.error('Error:', err);
      
      // Add error message
      setMessages(prev => [...prev, {
        sender: 'assistant',
        text: `I'm sorry, I encountered an error: ${err.message}`,
        timestamp: getTimestamp(),
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSuggestionClick = (text: string) => {
    setInput(text);
    setTimeout(() => {
      document.querySelector('textarea')?.focus();
    }, 100);
  };

  const renderMessages = () => {
    if (messages.length === 0) {
      return <WelcomeScreen onSuggestionClick={handleSuggestionClick} />;
    }

    return messages.map((message, index) => (
      <MessageItem key={index} message={message} isUser={message.sender === 'user'} />
    ));
  };

  return (
    <>
      <AnimationStyles />
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          height: '100%',
          background: '#FAFAFA',
          borderRadius: '12px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1)',
          maxWidth: '900px',
          margin: '0 auto',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '24px',
            display: 'flex',
            flexDirection: 'column',
            backgroundColor: '#FAFAFA',
            justifyContent: messages.length > 0 ? 'flex-start' : 'flex-end',
          }}
        >
          {renderMessages()}
          {isTyping && <ThinkingIndicator />}
          <div ref={bottomRef} />
        </div>

        <ChatInput
          input={input}
          setInput={setInput}
          sendMessage={sendMessage}
          avatar={avatar}
          setAvatar={setAvatar}
          setActiveView={setActiveView}
          disabled={isTyping}
        />
      </div>
    </>
  );
}