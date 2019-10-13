import React from 'react'
import './LoadingScreen.css'

const LoadingScreen = props => {
    return (
        <div className="LoadingScreen">
            <div className="LoadingScreen__left">
                <div className="LoadingScreen__spinner"/>
            </div>
            <div className="LoadingScreen__right">
                <h2> loading... </h2>
                <i> finding the best grooves for you...</i>
            </div>
        </div>
    )
}


export default LoadingScreen
