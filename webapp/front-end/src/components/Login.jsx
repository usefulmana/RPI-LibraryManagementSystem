import React, { Component } from 'react';
import { login } from './UserFunctions';

class Login extends Component {
  constructor() {
    super();
    this.state = {
      username: '',
      password: '',
      error: ''
    };

    this.onChange = this.onChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
  }

  onChange(e) {
    this.setState({ [e.target.name]: e.target.value });
  }
  onSubmit(e) {
    e.preventDefault();

    const user = {
      username: this.state.username,
      password: this.state.password
    };

    login(user).then(res => {
      if (!res.error) {
       this.props.history.push('/dashboard')
      }
      else{
        this.setState({"error": res.error})
      }
    });
  }

  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="text-center">
            <form noValidate onSubmit={this.onSubmit}>
              <h1 className="h3 mb-3 font-weight-normal">Please sign in</h1>
              <div className="form-group">
                <label htmlFor="username">Username</label>
                <input
                  type="test"
                  className="form-control"
                  name="username"
                  placeholder="Enter email"
                  value={this.state.username}
                  onChange={this.onChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  className="form-control"
                  name="password"
                  placeholder="Password"
                  value={this.state.password}
                  onChange={this.onChange}
                />
              </div>
              <button
                type="submit"
                className="btn btn-lg btn-primary btn-block"
              >
                Sign in
              </button>
              <h1 style={{color: 'red' }}>{this.state.error}</h1>
            </form>
          </div>
        </div>
      </div>
    );
  }
}

export default Login;
