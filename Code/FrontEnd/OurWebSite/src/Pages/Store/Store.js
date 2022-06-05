import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom'
import axios from 'axios'
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import { useNavigate } from "react-router-dom";
import './Store.css'


function Store({storesProducts, setStoresProducts}){
    const [storeName, setStoreName] = useState('');
    const [storeRank, setRank] = useState('');
    const [founderName, setFounderName] = useState('')
    const [productName, setProductName] = useState('')
    const [description, setDecription]  = useState('')
    const [price, setPrice] = useState(0)
    const [category, setCategory] = useState('')
    const params = useParams()
    const [options,setOptions] = useState([])
    const storeId = params.storeId
    const [permissions, setPermissions] = useState({})
    const Navigate = useNavigate() 

    const addProduct = async (e) =>{
        const newP = {
            store_id: storeId,
            name: productName,
            description: description,
            price: price,
            category: category,
            id: localStorage.getItem("user_id")
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
            const response = await axios.get("http://127.0.0.1:8000/permission/"+storeId+"/"+ localStorage.getItem("user_id"))
            console.log(response)
            setPermissions(permissions => response.data)
        }
        catch (err){
            console.log(err.response);
        }
        try{
            const response = await axios.get("http://127.0.0.1:8000/stores/"+storeId)
            console.log(response)
            setStoreName(response.data["store_name"])
            setFounderName(response.data["founder_id"])
            setRank(response.data["rank"])
            setStoresProducts(storesProducts => [response.data["products"].map(x=><li key={x["_Product__ID"]} style={{cursor:'pointer'}} onClick={()=>Navigate("../"+ x["_Product__ID"])}><h3 style={{display:'inline'}}>{x["_Product__name"]}</h3></li>)])
            setOptions(options => response.data["products"].map(function(x){
                return {label:x["_Product__name"],
                        value:x["_Product__ID"]}
        }))
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
        <div className='split left'>
            <h2>Store details:</h2>
            <ul>
                <li>store name: <h3 style={{display:'inline'}}>{storeName}</h3></li>
                <li>store founder's name: <h3 style={{display:'inline'}}>{founderName}</h3></li>
                <li>store ranking: <h3 style={{display:'inline'}}>{storeRank}</h3></li>
                <li>store products:
                </li>
                <ul>
                {storesProducts.length === 0 ? <li>no products</li>: storesProducts}
                </ul>
            </ul>
        </div>
        <div className='split right'>
            <h2>Actions:</h2>
                {hasPermition(1) ? <li> <Popup  trigger={<button style={{margin:'5px'}}> Add new product</button>} position="right center">
                    <div>
                        please fill the information below:
                        <form  onSubmit = {addProduct}>
                            <input type = 'text' name = 'name' placeholder="product name..." required onChange={(e)=> setProductName(e.target.value)}/>
                            <textarea style={{resize:'none'}} type = 'text' name = 'description' placeholder="description..."  onChange={(e)=> setDecription(e.target.value)}/>
                            <input type = 'number' name = 'price' placeholder="price..." required onChange={(e)=> setPrice(e.target.value)}/>
                            <input type = 'text' name = 'category' placeholder="category..." required onChange={(e)=> setCategory(e.target.value)}/>
                            <button style={{marginLeft: '40%'}}  onSubmit = {addProduct}>add</button>
                        </form>
                    </div> </Popup> </li>: ""}

                {hasPermition(1) ? <li><Popup trigger={<button style={{margin:'5px'}}>Add products to inventory</button>} position="right center">
                <div>
                    please choose a product:
                    <form  onSubmit = {addProduct}>
                        <select>
                            {options.map((option) => (
                                <option value={option.value}>{option.label}</option>))}
                         </select>
                         <input type = 'number' name = 'amount' placeholder="amount..." required onChange={(e)=> setPrice(e.target.value)}/>
                        <button style={{marginLeft: '40%'}}  onSubmit = {addProduct}>add</button>
                    </form>
                </div> </Popup></li>: ""}

                {hasPermition(1) ? <li><Popup trigger={<button style={{margin:'5px'}}>Remove products from inventory</button>} position="right center">
                    <div>
                        please choose a product:
                        <form  onSubmit = {addProduct}>
                        <select>
                            {options.map((option) => (
                                <option value={option.value}>{option.label}</option>))}
                         </select>
                         <input type = 'number' name = 'amount' placeholder="amount..." required onChange={(e)=> setPrice(e.target.value)}/>
                            <button style={{marginLeft: '40%'}}  onSubmit = {addProduct}>add</button>
                        </form>
                    </div> </Popup></li>: ""}

                {hasPermition(1) ? <li><Popup trigger={<button style={{margin:'5px'}}>edit product</button>} position="right center">
                    <div>
                         please choose a product and fill the information that you want to change:
                        <form  onSubmit = {addProduct}>
                            <select>
                                {options.map((option) => (
                                    <option value={option.value}>{option.label}</option>))}
                            </select>                           
                            <input type = 'text' name = 'name' placeholder="name..."  onChange={(e)=> setPrice(e.target.value)}/>
                            <textarea style={{resize:'none'}} type = 'text' name = 'description' placeholder="description..."  onChange={(e)=> setDecription(e.target.value)}/>
                            <input type = 'number' name = 'price' placeholder="price..."  onChange={(e)=> setPrice(e.target.value)}/>
                            <input type = 'text' name = 'category' placeholder="category..." onChange={(e)=> setCategory(e.target.value)}/>
                            <button style={{marginLeft: '40%'}}  onSubmit = {addProduct}>add</button>
                        </form>
                    </div> </Popup></li>: ""}

                {hasPermition(2) ? <li><Popup trigger={<button style={{margin:'5px'}}>Add store owner</button>} position="right center">
                <div>
                    please fill the information below:
                    <form  onSubmit = {addProduct}>
                        <input type = 'text' name = 'name' placeholder="new owner name..." required onChange={(e)=> setProductName(e.target.value)}/>
                        <button style={{marginLeft: '40%'}}  onSubmit = {addProduct}>add</button>
                    </form>
                </div> </Popup></li>: ""}

                {hasPermition(3) ? <li><Popup trigger={<button style={{margin:'5px'}}>Add store manager</button>} position="right center">
                <div>
                    please fill the information below:
                    <form  onSubmit = {addProduct}>
                        <input type = 'text' name = 'name' placeholder="new manager name..." required onChange={(e)=> setProductName(e.target.value)}/>
                        <button style={{marginLeft: '40%'}}  onSubmit = {addProduct}>add</button>
                    </form>
                </div> </Popup></li>: ""}

                {hasPermition(4) ? <li><Popup trigger={<button style={{margin:'5px'}}>change manager permissions</button>} position="right center">
                <div>
                    in the requminets?
                    <form  onSubmit = {addProduct}>
                        <input type = 'text' name = 'name' placeholder="in the requminets?..." required onChange={(e)=> setProductName(e.target.value)}/>
                        <button style={{marginLeft: '40%'}}  onSubmit = {addProduct}>add</button>
                    </form>
                </div> </Popup></li>: ""}

                {hasPermition(6) ? <li><Popup trigger={<button style={{margin:'5px'}}>Get store's roles</button>} position="right center">
                <div>
                    <form  onSubmit = {addProduct}>
                        {storesProducts}
                    </form>
                </div> </Popup></li>: ""}
            
                
        </div>
    </div>
)
}

export default Store;
