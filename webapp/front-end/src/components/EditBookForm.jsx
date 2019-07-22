import React, { Component } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { GET_BOOK_BY_ID, UPDATE_BOOK } from './rest_api_routes';
import axios from 'axios'

class EditBookForm extends Component {
  constructor() {
    super();
    this.state = {
      book: [],
      id: '',
      title: '',
      author: '',
      published_date: new Date(),
      ISBN: '',
      quantity: '',
      form_on: false
    };
    this.onChange = this.onChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this)
    this.handleChange = this.handleChange.bind(this);
    this.toggle_form = this.toggle_form.bind(this);
  }

  componentDidMount() {
    this.fetchBookInfo();
  }

  fetchBookInfo() {
    fetch(`${GET_BOOK_BY_ID}/${this.props.match.params.id}`)
      .then(res => res.json())
      .then(res =>
        this.setState({
          book: res
        })
      );
  }

  handleChange(date) {
    this.setState({
      published_date: date
    });
  }

  onChange(e) {
    this.setState({ [e.target.name]: e.target.value });
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
          published_date: formatted_date,
          quantity: parseInt(this.state.quantity)
      }
      const config = {
          headers: {
              'Content-Type': 'application/json'
          }
      }
      const body = JSON.stringify(book)
      axios.put(`${UPDATE_BOOK}/${this.props.match.params.id}`, body, config)
          .then(res => alert("Success!")).then(res => this.props.history.push('/dashboard'))
  }

  toggle_form() {
    this.setState({
      form_on: !this.state.form_on
    });
  }

  handleEdit(id, title, author, ISBN, quantity) {
    this.toggle_form();
    this.setState({
      id: id,
      title: title,
      author: author,
      ISBN: ISBN,
      quantity: quantity
    });
  }
  formatDate(input) {
    var datePart = input.match(/\d+/g),
        year = datePart[0], // get only two digits
        month = datePart[1], day = datePart[2];

    return day + '/' + month + '/' + year;
}
  render() {
    const form = () => {
      return (
        <div>
          <form onSubmit={this.onSubmit}>
            <div className="form-group">
              <label htmlFor="title">Title</label>
              <input
                type="text"
                onChange={this.onChange}
                class="form-control"
                name="title"
                placeholder="Title"
                value={this.state.title}
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
                value={this.state.author}
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
                value={this.state.ISBN}
                placeholder="ISBN"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="quantity">Quantity</label>
              <input
                type="number"
                onChange={this.onChange}
                class="form-control"
                name="quantity"
                value={this.state.quantity}
                placeholder="Quantity"
                min="1"
                step="1"
                max="100"
                required
              />
            </div>
            <div className="form-group">
                      <label htmlFor="">Old Published Date (dd/MM/yyyy)</label>
                <br/>
                <input
                    type="text"
                    value={this.formatDate(this.state.book.published_date)}
                    readOnly
                />
            </div>
            <div className="form-group">
                      <label htmlFor="">New Published Date (dd/MM/yyyy)</label>
              <br />
              <DatePicker
                selected={this.state.published_date}
                onChange={this.handleChange}
                dateFormat="dd/MM/yyyy"
                required
              />
            </div>
            <button type="submit" class="btn btn-primary">
              Submit
            </button>
          </form>
        </div>
      );
    };
    return (
      <div className="container">
        <button
          className="btn btn-primary mb-2 mt-3"
          onClick={this.handleEdit.bind(this,
            this.state.book.id,
            this.state.book.title,
            this.state.book.author,
            this.state.book.ISBN,
            this.state.book.quantity
          )}
        >
          {' '}
          Edit Book{' '}
        </button>
        {this.state.form_on ? form() : null}
      </div>
    );
  }
}

export default EditBookForm;
