import { store } from './index'

// hack: change the page in the store to a nice route name by lowercasing it and cropping
export const transformRoute = pagename => {
    const cropped = pagename.slice(8).toLowerCase()
    return (cropped === 'splash') ? '/' : '/' + cropped
}

export const urify = component => encodeURIComponent(component)

export const spotify = (url, params) => {
    console.log(store)
    const apikey = store.getState().trip.getIn(['spotify', 'token'])

    if (apikey === null) {
        throw new Error('Spotify not authorized!')
    }

    // process the param object into a slug
    const slug = Object.keys(params).map(k => `${k}=${urify(params[k])}`).join('&')

    return fetch(`https://api.spotify.com/v1/${url}?${slug}`, {
            headers: {
                'Authorization': `Bearer ${apikey}`
            }
        }
    ).then(r => r.json())
}
