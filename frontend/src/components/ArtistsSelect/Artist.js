import React from 'react'

import './Artist.css'

const Artist = props => {
    const hasGenres = props.obj.genres.length > 0
    const genres = props.obj.genres.join(', ')

    return (
        <li 
            className="Artist"
            onClick={props.onClick}>
            <div className="Artist__img_container">
                <div className="Artist__img_clipper">
                    {props.obj.images.length > 0 ?
                        <img
                            className="Artist__img"
                            src={props.obj.images[0].url}
                            alt={props.obj.name + ' image'}/> :
                        <div className="Artist__img--blank"/>
                    }
                </div>
            </div>
            <div className="Artist__titles">
                <h2>{props.obj.name}</h2>
                {hasGenres && <i>{genres}</i>}
            </div>
        </li>
    )
}

export default Artist
