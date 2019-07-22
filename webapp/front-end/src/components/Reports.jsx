import React, { Component } from 'react'
import {GET_DAILY_REPORT_PLOT, GET_WEEKLY_REPORT_PLOT } from './rest_api_routes';

export default class Reports extends Component {

    render() {
        return (
            <div className='container'>
                <div className="row">
                    <div className='col-6'>
                        <img src={GET_DAILY_REPORT_PLOT} alt="Daily chart" /><br />
                        <p><b>Daily</b></p>
                    </div>
                    <div className='col-6'>
                        <img src={GET_WEEKLY_REPORT_PLOT} alt="Weekly chart" /><br />
                        <p><b>Weekly</b></p>
                    </div>
                </div>
                                        
            </div>
        )
    }
}
