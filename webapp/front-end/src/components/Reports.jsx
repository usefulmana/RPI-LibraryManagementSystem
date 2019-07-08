import React, { Component } from 'react'

export default class Reports extends Component {

    render() {
        return (
            <div className='container'>
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
