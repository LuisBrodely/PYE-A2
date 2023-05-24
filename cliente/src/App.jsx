import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import { ContextProvider } from "./context/context";
import Sidebar from './components/Sidebar';
import Table from './screens/Table';
import Graphics from './screens/Graphics';

function App() {

  return (
    <>
      <Router>
        <ContextProvider>
          <Sidebar>
            <Routes>
              <Route path="/" element={<Table />} />
              <Route path="/graphics" element={<Graphics />} />
            </Routes>
          </Sidebar>
        </ContextProvider>
      </Router>
    </>
  )
}

export default App
