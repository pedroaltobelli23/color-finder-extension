import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import ColorFinder from './pages/ColorFinder'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <ColorFinder/>
  )
}

export default App
