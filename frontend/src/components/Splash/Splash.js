import React from 'react'
import './Splash.css'

const Splash = props => (
    <div className="Splash">
        <div className="Splash__left">
            <h2 className="Splash__title--invisible">&nbsp;</h2>
            <img src="https://picsum.photos/150/150?grayscale" alt="planbien logo"/>
            <h2 className="Splash__title">plan biene</h2>
        </div>
        <div className="Splash__right">
            {props.children}
        </div>
    </div>
)

export default Splash
