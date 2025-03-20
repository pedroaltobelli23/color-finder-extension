import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ButtonAppBar from './Components/Header';
import About from './Pages/About';
import Home from './Pages/Home';
import { Divider } from '@mui/material';

export default function AppRouter() {
  return (
    <Router>
      <ButtonAppBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Router>
  );
}
