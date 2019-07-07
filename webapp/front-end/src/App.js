import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import Home from './components/Home';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <Router>
      <div className="App">
        <div className="mx-auto">
          <h1 className="text-center">Library Management System</h1>
          <NavBar />
          <hr className="w-50" />
        </div>
        <Route exact path="/" component={Home} />
        <Route exact path="/login" component={Login} />
        <Route exact path="/dashboard" component={Dashboard}/>
      </div>
    </Router>
  );
}

export default App;
