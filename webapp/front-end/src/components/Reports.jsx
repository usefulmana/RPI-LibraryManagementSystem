import React, { Component } from 'react'
import { GET_DAILY_CHART } from './rest_api_routes';

export default class Reports extends Component {
    
    render() {
        return (
            <div className='container'>
                <img src={GET_DAILY_CHART} alt="Daily Chart" /><br />
                <p><b>Daily</b></p>
                {/* <div className="row">
                    <div className='col-6'>
                        <img src={GET_DAILY_CHART} alt="Daily chart" /><br />
                        <p><b>Daily</b></p>
                    </div>
                    <div className='col-6'>
                        <img src={GET_WEEKLY_CHART} alt="Weekly chart" /><br />
                        <p><b>Weekly</b></p>
                    </div>  
                </div> */}
                                        
            </div>
        )
    }
}
