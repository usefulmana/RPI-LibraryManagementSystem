import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';

class Navbar extends Component {
  logOut(e) {
    e.preventDefault();
    localStorage.removeItem('usertoken');
    this.props.history.push(`/`);
  }

  render() {
    const loginLink = (
      <div className='container'>
        <div className="text-center">
          <Link to="/login" className="nav-link">
            Login
          </Link>
        </div>
      </div>
    );

    const userLink = (
      <div className="container">
        <div className="text-center">
          <a href="" onClick={this.logOut.bind(this)} className="nav-link">
            Logout
          </a>
        </div>
      </div>
    );

    return (
      <div className='container'>
        <div className="text-center">
              <Link to="/" className="nav-link">
                Home
              </Link>
                {localStorage.usertoken ? userLink : loginLink}
        </div>
      </div>
    );
  }
}

export default withRouter(Navbar);
