import React from 'react';
import {useParams} from 'react-router-dom'

function Store(){
    const params = useParams()
    const storeId = params.storeId
return(
    <h2>Store id is {storeId}</h2>
)
}

export default Store;
