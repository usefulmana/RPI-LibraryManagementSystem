import React, { Component } from 'react';
import axios from 'axios'
import JwPagination from 'jw-react-pagination'
import { DELETE_BOOK } from './rest_api_routes';

export default class DataTable extends Component {
  constructor(props){
    super(props)
    this.state = {
      pageOfItems: []
    }
    this.onChangePage = this.onChangePage.bind(this);
  }

  onChangePage(pageOfItems) {
    // update local state with new page of items
    this.setState({ pageOfItems });
  }

  handleDelete(id){
    if(window.confirm("This transaction is irreversible. Are you sure?")){
        const config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        axios.delete(`${DELETE_BOOK}/${id}`, config)
            .then(res => alert("Success!")).then(res => window.location.reload())
    }
    else {
        alert("Transaction cancelled")
    }
  }
  render() {
    return (
      <React.Fragment>
        <table className="table table-striped">
          <thead className='thead-dark'>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Title</th>
              <th scope="col">Author</th>
              <th scope="col">Published Date</th>
              <th scope="col">ISBN</th>
              <th scope="col">Action(s)</th>
            </tr>
          </thead>
          <tbody>
            {this.state.pageOfItems.map(d => (
              <tr>
                <td>{d.id}</td>
                <td>{d.title}</td>
                <td>{d.author}</td>
                <td>{d.published_date}</td>
                <td>{d.ISBN}</td>
                <td>
                    <button className="btn btn-danger" onClick={this.handleDelete.bind(this,d.id)}> Delete </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="text-center">
          <JwPagination items={this.props.data} onChangePage={this.onChangePage} pageSize={10} />
        </div>
      </React.Fragment>
    );
  }
}
