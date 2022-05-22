import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom'
import axios from 'axios'
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import { useNavigate } from "react-router-dom";


function Store({ip}){
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
    const permissions = {1: true, 2: false,3: false, 4: false, 5: false, 6: false, 7: false}  // need to get the user permission for this site
    
    const Navigate = useNavigate() 

    const addProduct = async (e) =>{
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
        setStoresProducts(storesProducts => [response.data["products"].map(x=><li key={x["_Product__ID"]} style={{cursor:'pointer'}} onClick={()=>Navigate("../"+ x["_Product__ID"])}><h3 style={{display:'inline'}}>{x["_Product__name"]}</h3></li>)])
        } catch (err){
            console.log(err.response);
        }
    }

    const hasPermition = (per) =>{
        return permissions[per];
    }
    useEffect(() => {   
        getStoreInfo()
      }, []);

return(
    <div>
        <h2>Store details:</h2>
        <ul>
            <li>store name: <h3 style={{display:'inline'}}>{storeName}</h3></li>
            <li>store founder's name:<h3 style={{display:'inline'}}>{founderName}</h3></li>
            <li>store ranking:<h3 style={{display:'inline'}}>{storeRank}</h3></li>
            <li>store products:{hasPermition(1) ? <Popup trigger={<button style={{margin:'5px'}}> Add new product</button>} position="right center">
                <div>
                please fill the information below:
                <form  onSubmit = {addProduct}>
                    <input type = 'text' name = 'name' placeholder="product name..." required onChange={(e)=> setProductName(e.target.value)}/>
                    <textarea style={{resize:'none'}} type = 'text' name = 'description' placeholder="description..."  onChange={(e)=> setDecription(e.target.value)}/>
                    <input type = 'number' name = 'price' placeholder="price..." required onChange={(e)=> setPrice(e.target.value)}/>
                    <input type = 'text' name = 'category' placeholder="category..." required onChange={(e)=> setCategory(e.target.value)}/>
                    <button style={{marginLeft: '40%'}}  onSubmit = {addProduct}>add</button>
                </form>
               </div> </Popup>: ""}
            </li>
            <ul>
            {storesProducts.length === 0 ? <li>no products</li>: storesProducts}
            </ul>
        </ul>
        
    </div>
)
}

export default Store;
