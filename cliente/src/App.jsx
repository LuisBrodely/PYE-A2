import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import { ContextProvider } from "./context/context";
import Header from './components/Header';
import Table from './screens/Table';
import Graphics from './screens/Graphics';
import Frecuency from './screens/Frecuency';

function App() {

  return (
    <>
      <Router>
        <ContextProvider>
          <Header />
          <Routes>
            <Route path="/" element={<Table />} />
            <Route path="/graphics" element={<Graphics />} />
            <Route path="/frecuency" element={<Frecuency />} />
          </Routes>
        </ContextProvider>
      </Router>
    </>
  )
}

export default App
