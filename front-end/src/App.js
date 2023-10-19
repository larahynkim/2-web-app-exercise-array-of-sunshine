import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import React from 'react';
import './App.css'
import Journal from './Journal'
import Home from './Home'
import Header from './Header'
import Navbar from './Navbar'
import Calendar from './Calendar';


const App = props => {
  return (
    <div className="App">
      <Router>
      <Header />
        <Navbar />
        <main className="App-main">
          <Routes>
            <Route path="/" element={<Home />} />

            <Route path="/journal" element={<Journal />} />
            <Route path="/calendar" element={<Calendar />}/>

          </Routes>
        </main>
      </Router>
    </div>
  )
}

export default App
