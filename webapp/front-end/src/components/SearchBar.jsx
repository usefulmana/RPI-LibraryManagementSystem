import React, { Component } from 'react'
import { Link } from 'react-router-dom'

export default class SearchBar extends Component {
    constructor() {
        super()
        this.state = {
            query: ''
        }
        this.onChange = this.onChange.bind(this)
    }
    onChange(e) {
        this.setState({ [e.target.name]: e.target.value });
    }

    render() {
        return (
            <React.Fragment>
                <form className="form-inline">
                    <input className="form-control" type="search" placeholder="Title, Author, ISBN..." name="query" id="search" required onChange={this.onChange} />
                    <Link to={{ pathname: `/search/${this.state.query}`, state: 'flushDeal' }}>
                        <span className="input-group-append">
                            <button class="btn btn-search my-2 my-sm-0 " type="submit">
                            </button>
                        </span>
                    </Link>
                </form>
            </React.Fragment>
        )
    }
}
