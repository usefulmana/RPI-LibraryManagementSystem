import React, { Component } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import axios from 'axios'

export default class AddBookForm extends Component {
  constructor() {
    super();
    this.state = {
      title: '',
      author: '',
      ISBN: '',
      published_date: new Date()
    };
    this.onChange = this.onChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  onChange(e) {
    this.setState({ [e.target.name]: e.target.value });
  }

  toggle = () => {
    // Clear errors
    this.setState({
      modal: !this.state.modal
    });
  };
    handleChange(date) {
        this.setState({
            published_date: date.toDateString()
        });
    }
  onSubmit(e) {
    e.preventDefault();
    let formatted_date = this.state.published_date.getFullYear() + ":" + (this.state.published_date.getMonth() + 1) +
          ':' +
          this.state.published_date.getDate();
    const book = {
        title: this.state.title,
        author: this.state.author,
        ISBN: this.state.ISBN,
        published_date: formatted_date
    }
    
    const config = {
        headers:{
            'Content-Type': 'application/json'
        }
    }
    const body = JSON.stringify(book)
    console.log(body)
    axios.post('http://127.0.0.1:5000/books',body, config)
    .then(res => alert("Success!")).then(res=> window.location.reload())
  }

  render() {
    return (
      <div class="container">
        <form onSubmit={this.onSubmit}>
          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input
              type="text"
              onChange={this.onChange}
              class="form-control"
              name="title"
              placeholder="Title"
              autoFocus
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="author">Author</label>
            <input
              type="text"
              onChange={this.onChange}
              class="form-control"
              name="author"
              placeholder="Author"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="ISBN">ISBN</label>
            <input
              type="text"
              onChange={this.onChange}
              class="form-control"
              name="ISBN"
              placeholder="ISBN"
              required
            />
          </div>
          <div className='form-group'>
            <label htmlFor="">Published Date</label>
            <br/>
            <DatePicker
                selected={this.state.published_date}
                onChange={this.handleChange}
                required
            />
          </div>
          <button type="submit" class="btn btn-primary">
            Submit
          </button>
        </form>
      </div>
    );
  }
}