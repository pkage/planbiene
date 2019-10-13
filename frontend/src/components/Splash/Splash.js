import React from 'react'
import './Splash.css'
import logo from './logo.png'

const Splash = props => (
    <div className="Splash">
        <div className="Splash__left">
            <h2 className="Splash__title--invisible">&nbsp;</h2>
            <img src={logo} alt="planbiene logo" width="auto" height="150px"/>
            <h2 className="Splash__title">GigScanner</h2>
        </div>
        <div className="Splash__right">
            {props.children}
        </div>
    </div>
)

export default Splash
