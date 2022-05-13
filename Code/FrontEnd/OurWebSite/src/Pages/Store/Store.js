import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom'
import axios from 'axios'


function Store({products}){
    const [storeName, setStoreName] = useState('');
    const [storeRank, setRank] = useState('');
    const [founderName, setFounderName] = useState('')
    const [storesProducts, setStoresProducts] = useState([])
    const params = useParams()
    const storeId = params.storeId
    const getStoreInfo = async () =>{
        try{
        const response = await axios.get("http://127.0.0.1:8000/stores/"+storeId,{storeId:storeId})
        console.log(response)
        setStoreName(response.data["store_name"])
        setFounderName(response.data["founder_id"])
        setRank(response.data["rank"])
        setStoresProducts(storesProducts => [...storesProducts,...response.data["products"]])
        } catch (err){
            console.log(err.response);
        }
    }
    useEffect(() => {   
        getStoreInfo()
      }, []);

return(
    <div>
        <h2>Store details:</h2>
        <ul>
            <li>store name: {storeName}</li>
            <li>store founder's name: {founderName}</li>
            <li>store ranking: {storeRank}</li>
            <li>store products: {storesProducts.length == 0 ? "no products": storesProducts}</li>
        </ul>
        
    </div>
)
}

export default Store;
