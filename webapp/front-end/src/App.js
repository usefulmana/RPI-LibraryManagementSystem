import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { Switch } from 'react-router-dom';
import NavBar from './components/NavBar';
import Home from './components/Home';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import SearchResults from './components/SearchResults';
import Reports from './components/Reports';
import EditBookForm from './components/EditBookForm';
import { ProtectedRoute } from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <div className="App">
        <div className="mx-auto">
          <h1 className="text-center mt-5">Library Management System</h1>
          <NavBar />
          <hr className="w-50" />
        </div>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route exact path="/login" component={Login} />
          <ProtectedRoute exact path="/dashboard" component={Dashboard} />
          <ProtectedRoute exact path="/reports" component={Reports} />
          <ProtectedRoute path="/edit/:id" component={EditBookForm} />
          <ProtectedRoute
            path="/search/:query?"
            component={props => (
              <SearchResults timestamp={new Date().toString()} {...props} />
            )}
          />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
