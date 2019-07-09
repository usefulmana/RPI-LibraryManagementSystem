import React, { Component } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import axios from 'axios'
import { ADD_BOOK } from './rest_api_routes';

export default class AddBookForm extends Component {
  constructor() {
    super();
    this.state = {
      title: '',
      author: '',
      ISBN: '',
      published_date: new Date(),
      dateError: ''
    };
    this.onChange = this.onChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  onChange(e) {
    this.setState({ [e.target.name]: e.target.value });
  }

  toggle = () => {
    this.setState({
      modal: !this.state.modal
    });
  };
  validate = (date) =>{
    // Validating user's input with regular expression
    let dateRegex = /^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$/
    if (date.match(dateRegex))
    {
      return true
    }
    else{
      return false  
    }
  }
  handleChange(date) {
      this.setState({
          published_date: date
      });
  }
  onSubmit(e) {
    e.preventDefault();
    let another_format = ('0' + this.state.published_date.getDate()).slice(-2) + "/" + ('0' + (this.state.published_date.getMonth() + 1)).slice(-2) +
      '/' +
      this.state.published_date.getFullYear();
    // Proceed if the user's input is legitimate
    if (this.validate(another_format)){
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
        headers: {
          'Content-Type': 'application/json'
        }
      }
      const body = JSON.stringify(book)
      axios.post(ADD_BOOK, body, config)
        .then(res => alert("Success!")).then(res => window.location.reload())
    }
    else{
      this.setState({
        dateError: 'Wrong date format! (dd/mm/yyy) only'
      })
    }
    
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
          <p style={{ color: 'red' }}> {this.state.dateError}</p>
         
          <button type="submit" class="btn btn-primary">
            Submit
          </button>
        </form>
      </div>
    );
  }
}
