import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom'
import axios from 'axios'
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import Product from '../Product/Product';



function Store({products, ip}){
    const [storeName, setStoreName] = useState('');
    const [storeRank, setRank] = useState('');
    const [founderName, setFounderName] = useState('')
    const [storesProducts, setStoresProducts] = useState([])
    const [productName, setProductName] = useState('')
    const [description, setDecription]  = useState('')
    const [price, setPrice] = useState(0)
    const [category, setCategory] = useState('')
    const params = useParams()
    const storeId = params.storeId

    const handleSubmit = async (e) =>{
        const newP = {
            store_id: storeId,
            name: productName,
            description: description,
            price: price,
            category: category,
            id: ip
        
        }
        try{
        const response = await axios.post("http://127.0.0.1:8000/users/add_new_product_to_inventory",newP)
        console.log(response)
        } catch (err){
            console.log(err.response);
        }
    }

    const getStoreInfo = async () =>{
        try{
        const response = await axios.get("http://127.0.0.1:8000/stores/"+storeId,{storeId:storeId})
        console.log(response)
        setStoreName(response.data["store_name"])
        setFounderName(response.data["founder_id"])
        setRank(response.data["rank"])
        console.log(response.data["products"])
       // setStoresProducts(storesProducts => [...storesProducts,...response.data["products"].map(x=><li style={{cursor:'pointer'}}>hello</li>)])
        } catch (err){
            console.log(err.response);
        }
    }
    useEffect(() => {   
        getStoreInfo()
      }, []);

return(
    //if(!my_store){}
    <div>
        <h2>Store details:</h2>
        <ul>
            <li>store name: {storeName}</li>
            <li>store founder's name: {founderName}</li>
            <li>store ranking: {storeRank}</li>
            <li>store products:<Popup trigger={<button> Add new product</button>} position="right center">
                <div>
                please fill the information below:
                <form  onSubmit = {handleSubmit}>
                    <input type = 'text' name = 'name' placeholder="product name..." required onChange={(e)=> setProductName(e.target.value)}/>
                    <textarea style={{resize:'none'}} type = 'text' name = 'description' placeholder="description..."  onChange={(e)=> setDecription(e.target.value)}/>
                    <input type = 'number' name = 'price' placeholder="price..." required onChange={(e)=> setPrice(e.target.value)}/>
                    <input type = 'text' name = 'category' placeholder="category..." required onChange={(e)=> setCategory(e.target.value)}/>
                    <button style={{marginLeft: '40%'}}  onSubmit = {handleSubmit}>add</button>
                </form>
               </div> </Popup>
            </li>
            <ul>
            <li>{storesProducts.length === 0 ? "no products": {storesProducts}}</li>
            </ul>
        </ul>
        
    </div>
)
}

export default Store;
