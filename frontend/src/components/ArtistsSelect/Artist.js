import React from 'react'

const Artist = props => {
    console.log(props.obj)


    return (
        <li onClick={props.onClick}>
            {props.obj.images.length > 0 &&
                <img src={props.obj.images[0].url}/>
            }
            {props.obj.id} / {props.obj.name}
        </li>
    )
}

export default Artist
