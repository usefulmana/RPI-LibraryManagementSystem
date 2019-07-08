import React, { Component } from 'react'
import { GET_DAILY_REPORT_PLOT, GET_WEEKLY_REPORT_PLOT } from './rest_api_routes';
import { Link } from 'react-router-dom';

export default class Reports extends Component {

    componentDidMount() {
        this.fetchReports()
    }

    fetchReports(){
        fetch(GET_DAILY_REPORT_PLOT).then(res=> res.json()).then(res=> console.log(res))
        fetch(GET_WEEKLY_REPORT_PLOT).then(res => res.json()).then(res => console.log(res))
    }

    render() {
        return (
            <div className='container'>
                <Link to='/dashboard'>Dashboard</Link>
                <div className="row">
                    <div className='col-6'>
                        <img src="/images/daily.png" alt="Daily chart" /><br />
                        <p><b>Daily</b></p>
                    </div>
                    <div className='col-6'>
                        <img src="/images/weekly.png" alt="Weekly chart" /><br />
                        <p><b>Weekly</b></p>
                    </div>  
                </div>
                                        
            </div>
        )
    }
}
