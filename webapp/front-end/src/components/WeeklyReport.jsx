import React, { Component } from 'react'
import { GET_WEEKLY_CHART } from './rest_api_routes';

export default class WeeklyReport extends Component {
    render() {
        return (
            <div>
               <img src={GET_WEEKLY_CHART} alt="Weekly Chart"></img>
               <p><b>Weekly</b></p> 
            </div>
        )
    }
}
