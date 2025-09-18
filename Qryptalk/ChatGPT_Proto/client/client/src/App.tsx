import React, { useState, useEffect } from "react";
import { encryptMessage, decryptMessage } from "./crypto";
import socket from "./socket";

export default function App() {
  const [msg, setMsg] = useState("");
  const [chat, setChat] = useState<string[]>([]);
  const sharedSecret = new Uint8Array(32); // mock PQC shared secret for demo

  useEffect(() => {
    socket.onmessage = async (event) => {
      const { iv, ciphertext } = JSON.parse(event.data);
      const text = await decryptMessage(sharedSecret, new Uint8Array(iv), new Uint8Array(ciphertext));
      setChat(prev => [...prev, "Friend: " + text]);
    };
  }, []);

  const sendMessage = async () => {
    const { iv, ciphertext } = await encryptMessage(sharedSecret, msg);
    socket.send(JSON.stringify({ iv: Array.from(iv), ciphertext: Array.from(new Uint8Array(ciphertext)) }));
    setChat(prev => [...prev, "You: " + msg]);
    setMsg("");
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">Qryptalk Demo</h1>
      <div className="border p-2 h-64 overflow-y-scroll">
        {chat.map((line, i) => <div key={i}>{line}</div>)}
      </div>
      <input value={msg} onChange={(e) => setMsg(e.target.value)} className="border p-1 mr-2" />
      <button onClick={sendMessage} className="bg-blue-500 text-white p-1 rounded">Send</button>
    </div>
  );
}
