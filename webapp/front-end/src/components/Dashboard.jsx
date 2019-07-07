import React, { Component } from 'react'
import ReactTable from 'react-table'
import AddBookForm from './AddBookForm';

export default class Dashboard extends Component {
    constructor(){
        super()
        this.state = {
            books: []
        }
    }

    componentDidMount() {
        this.fetchBooks()
    }
    onChange(e) {
        this.setState({ [e.target.name]: e.target.value });
    }
    onSubmit(e){

    }

    fetchBooks(){
        fetch('http://127.0.0.1:5000/books')
        .then(res => res.json())
        .then(res => this.setState({
            books: res
        }))
    }

    render() {
        const columns = [{
            Header: 'ID',
            accessor: 'id'
        },{
            Header: 'Title',
            accessor: 'title'
        },{
            Header: 'Author',
            accessor: 'author'
        },{
            Header: 'Published Date',
            accessor: 'published_date'
        },{
            Header: 'ISBN',
            accessor: 'ISBN'
        }]
        return (

            <div className='container'>
                <div>
                    <AddBookForm/>
                </div>
                <br/>        
                <div>
                    <ReactTable
                        data={this.state.books}
                        columns={columns}
                        defaultPageSize={10}
                    />
                </div>         
            </div>
        )
    }
}
