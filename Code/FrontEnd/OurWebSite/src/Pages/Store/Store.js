import React, {useEffect} from 'react';
import {useParams} from 'react-router-dom'
import axios from 'axios'


function Store({products}){
    const params = useParams()
    const storeId = params.storeId
    const getStoreInfo = async () =>{
        const response = await axios.get("http://127.0.0.1:8000/stores/"+storeId,{storeId:storeId})
        console.log(response)
    }

return(
    <div>
        <h2>Store id is {storeId}</h2>
    </div>
)
}

export default Store;
