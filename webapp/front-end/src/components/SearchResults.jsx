import React, { Component } from 'react'
import { GET_BOOKS_FROM_QUERY } from './rest_api_routes';
import DataTable from './DataTable';


export default class SearchResults extends Component {
    constructor(){
        super()
        this.state = {
            books: []
        }
    }

    componentDidMount() {
        this.fetchBooks()
    }

    fetchBooks(){
    fetch(`${GET_BOOKS_FROM_QUERY}/${this.props.match.params.query}`)
      .then(res => res.json())
      .then(res =>
        this.setState({
            books: res
        })
      );
    }
    

    render() {
        return (
        <div className="container">
            <div className='text-center mt-3'>
                <DataTable data={this.state.books} />
            </div>
        </div>
        )
    }
}