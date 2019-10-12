
// hack: change the page in the store to a nice route name by lowercasing it and cropping
export const transformRoute = pagename => {
    const cropped = pagename.slice(8).toLowerCase()
    return (cropped === 'splash') ? '/' : '/' + cropped
}

export const urify = component => encodeURIComponent(component)
