import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'
// import Index from './components/Index'

function App() {
  const [messages, setMessages] = useState([])

  const url = 'http://localhost:8001/message'

  const getMessages = async () => {
    try {
      const response = await axios.get(url)
      setMessages(response.data)
    } catch (error) {
      console.log('error: ' + error)
    }
  }

  useEffect(() => {
    getMessages()
    const interval = setInterval(getMessages, 2000)
    return () => clearInterval(interval)
  }, [])


  return (
    <>
    <h1>Current Messages From the Database: </h1>
    {messages && messages.length > 0 && (messages.map(message => (
      <div key={message.id}>
        <p>id: {message.id}</p>
        <p>Message: {message.message}</p>
      </div>
    ))) || (
      <div>
        No messages yet!
      </div>
    )}
    </>
  )
}

export default App
