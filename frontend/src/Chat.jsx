import React, { useState } from "react";
import axios from "axios";

function Chat() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = { sender: "You", text: message };

    // Append user message first
    setChatHistory((prevHistory) => [...prevHistory, userMessage]);

    try {
      const response = await axios.post("http://127.0.0.1:5000/chat", { message });

      const botReply = { sender: "Bot", text: response.data.reply || "No response received." };

      // Append bot response
      setChatHistory((prevHistory) => [...prevHistory, botReply]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setChatHistory((prevHistory) => [
        ...prevHistory,
        { sender: "Bot", text: "Error: Unable to fetch response. Try again." }
      ]);
    }

    setMessage("");
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen w-full bg-gradient-to-r from-pink-300 to-blue-300">
      <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-blue-500 mb-6  text-center">
  College Chatbot
</h1>

      <div className="w-11/12 max-w-md h-96 overflow-y-auto bg-white rounded-lg shadow-lg p-4 flex flex-col">
        {chatHistory.map((msg, index) => (
          <div
            key={index}
            className={`p-2 my-1 rounded-lg max-w-[75%] ${
              msg.sender === "You"
                ? "bg-green-500 text-white self-end"
                : "bg-gray-200 text-black self-start"
            }`}
          >
            <strong>{msg.sender}: </strong> {msg.text}
          </div>
        ))}
      </div>
      <div className="flex flex-col items-center w-11/12 max-w-md mt-3">
        <input
          type="text"
          placeholder="Ask me something..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          className="text-black w-full p-2 border-2 border-gray-300 rounded-md text-lg outline-none mb-2"
        />
        <button
          onClick={sendMessage}
          className="w-full p-2 bg-blue-500 text-white rounded-md text-lg hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default Chat;
