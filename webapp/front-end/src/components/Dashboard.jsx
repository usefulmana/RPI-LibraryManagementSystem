import React, { Component } from 'react';
import AddBookForm from './AddBookForm';
import DataTable from './DataTable';
import SearchBar from './SearchBar';
import { GET_ALL_BOOKS} from './rest_api_routes';
import {Link} from 'react-router-dom'
export default class Dashboard extends Component {
  constructor() {
    super();
    this.state = {
      books: [],
      form_on: false
    };
    this.toggle_form = this.toggle_form.bind(this);
  }

  componentDidMount() {
    this.fetchBooks();
  }
  onChange(e) {
    this.setState({ [e.target.name]: e.target.value });
  }
  toggle_form() {
    this.setState({
      form_on: !this.state.form_on
    });
  }

  fetchBooks() {
    fetch(GET_ALL_BOOKS)
      .then(res => res.json())
      .then(res =>
        this.setState({
          books: res
        })
      );
  }

  render() {
    const form = () => {
      return <AddBookForm />;
    };
    return (
      <div className="container">

        <div>
          <Link to='/reports'>View Reports</Link>
        </div>
        <div>
          <button className="btn btn-primary mb-2 mt-3" onClick={this.toggle_form}>
            {' '}
            Add Book{' '}
          </button>
          {this.state.form_on ? form() : null}
        </div>
        <br />
        <div className='mb-3'>
          <SearchBar />
        </div>
        <div className='text-center'>
          <DataTable data={this.state.books} />
        </div>
      </div>
    );
  }
}
