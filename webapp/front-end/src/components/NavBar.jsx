import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';
import { isAuthenticated } from './UserFunctions';

class Navbar extends Component {
  logOut(e) {
    e.preventDefault();
    sessionStorage.removeItem('usertoken');
    this.props.history.push(`/`);
  }

  render() {
    const loginLink = (
      <div className='container'>
        <div className="text-center">
          <Link to="/login" className="nav-link">
            Login
          </Link>
          <p className='mt-2'>
            Please Log In to Use This Website
          </p>

        </div>
      </div>
    );

    const userLink = (
      <div className="container">
        <div className="text-center">
          <a href="" onClick={this.logOut.bind(this)} className="nav-link">
            Logout
          </a>
          <p className='mt-2'>You are logged in</p>
          <Link to='/dashboard'>Dashboard</Link>
        </div>
      </div>
    );

    return (
      <div className='container'>
        <div className="text-center">
              <Link to="/" className="nav-link">
                Home
              </Link>
                {sessionStorage.usertoken ? userLink : loginLink}
        </div>
      </div>
    );
  }
}

export default withRouter(Navbar);
