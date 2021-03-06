import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom'
import axios from 'axios'
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import { useNavigate } from "react-router-dom";
import './Store.css'



function Store({storesProducts, setStoresProducts}){
    const [storeName, setStoreName] = useState('');
    const [storeRank, setRank] = useState(-1);
    const [founderName, setFounderName] = useState('')
    const [productName, setProductName] = useState('')
    const [description, setDecription]  = useState('')
    const [price, setPrice] = useState(-1)
    const [category, setCategory] = useState('')
    const [chosenProductiD, setChosenProduct]  = useState('1')
    const [amount, setAmount]  = useState(-1)
    const [officalsName, setOfficalsName] = useState('')
    const [roles, setRoles] = useState([])
    const [newDiscountType, setnewDiscountType] = useState('visible') 
    const [discountOn, setDiscountOn] = useState('product')
    const [discount_price, setDiscount_price] = useState('0')
    const [end_date, setEnd_date] = useState('')
    const [prodForDiscount, setProdForDiscount] = useState('1')
    const [amountForDiscount, setAmountForDiscount] = useState(0)
    const [min_price_for_discount, setMin_price_for_discount] = useState(0)
    const [minOrAmount, setMinOrAmount] = useState("0")   // 0 is min 1 is amount
    const [firstDiscount, setFirstDiscount] = useState(1)
    const [secondDiscount, setSecondDiscount] = useState(1)
    const [combineType, setCombineType] = useState("or")
    const [newPurhcaseType, setNewPurhcaseType ] = useState('product')

    const params = useParams()
    const [options,setOptions] = useState([])
    const [categoryOptions, setCategoryOptions] = useState([])
    const [discountOptions, setDiscountOptions] = useState([])
    const storeId = params.storeId
    const [permissions, setPermissions] = useState({})
    const [errMsg, setErrMsg] = useState("")
    const Navigate = useNavigate() 

    const addNewProduct = async (e) =>{
        e.preventDefault()
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
        window.location.reload(false);
        } catch (err){
            console.log(err.response);
            setErrMsg(err.response.data['detail'])
        }
    }

    const addProductToInvetory = async (e) =>{
        e.preventDefault()
        const prod = {
            store_id: storeId,
            product_id: chosenProductiD,
            quantity: amount , 
            id: localStorage.getItem("user_id")
        }
        try{
            const response = await axios.post("http://127.0.0.1:8000/users/add_products_to_inventory",prod)
            console.log(response)
            window.location.reload(false);
       }catch (err){
            console.log(err.response);
            setErrMsg(err.response.data['detail'])
    }
    }

    const removeProductFromInvetory = async (e) =>{
        e.preventDefault()
        const prod = {
            store_id: storeId,
            product_id: chosenProductiD,
            quantity: amount , 
            id: localStorage.getItem("user_id")
        }
        try{
            const response = await axios.post("http://127.0.0.1:8000/users/remove_products_from_inventory",prod)
            console.log(response)
            window.location.reload(false);
       }catch (err){
            console.log(err.response);
            setErrMsg(err.response.data['detail'])
    }
    }

    const editProduct = async (e) =>{
        e.preventDefault()
        const prod = {
            store_id: storeId,
            product_id: chosenProductiD,
            id: localStorage.getItem("user_id"),
            name: productName,
            description: description,
            rating: 0,
            price: price,
            category: category 
        }
        console.log(prod)
        try{
            const response = await axios.post("http://127.0.0.1:8000/users/edit_product_info",prod)
            console.log(response)
            window.location.reload(false);
       }catch (err){
            console.log(err.response);
            setErrMsg(err.response.data['detail'])
    }
    }

    const addStoreOwner = async (e) =>{
        e.preventDefault()
        const info = {
            user_id: localStorage.getItem("user_id"),
            store_id: storeId,
            new_owner_name: officalsName 
        }
        try{
            const response = await axios.post("http://127.0.0.1:8000/users/add_store_owner" ,info)
            console.log(response)
            window.location.reload(false);
       }catch (err){
            console.log(err.response);
            setErrMsg(err.response.data['detail'])
    }
    }

    const addStoreManager= async (e) =>{
        e.preventDefault()
        const info = {
            user_id: localStorage.getItem("user_id"),
            store_id: storeId,
            new_owner_name: officalsName 
        }
        try{
            const response = await axios.post("http://127.0.0.1:8000/users/add_store_manager" ,info)
            console.log(response)
            window.location.reload(false);
       }catch (err){
            console.log(err.response);
            setErrMsg(err.response.data['detail'])
    }
    }

    const getStoreRoles= async (e) =>{
        e.preventDefault()
        const info = {
            store_name: storeId, 
            id: localStorage.getItem("user_id"),
        }
        try{
            const response = await axios.post("http://127.0.0.1:8000/users/get_store_roles" ,info)
            console.log(response.data)
            setRoles(roles => [Object.values(response.data).map( x => <li key={x}>{x['appointed']}</li>)])

       }catch (err){
            console.log(err.response);
            setErrMsg(err.response.data['detail'])
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
            if (response.data["products"].length > 0)
                setStoresProducts(storesProducts => [response.data["products"].map(x=><div key={x["_Product__ID"]} style={{width:'3px'}}><li style={{cursor:'pointer'}} ><h3 onClick={()=>Navigate("../"+ x["_Product__ID"])} style={{display:'inline'}}>{x["_Product__name"]}</h3></li></div>)])
                setOptions(options => response.data["products"].map(function(x){
                return {label:x["_Product__name"],
                        value:x["_Product__ID"]}
        }))
            const catgs = [... new Set(response.data["products"].map(item =>item["_Product__category"]))]
            setCategoryOptions(categryOptions => catgs.map(function(x){
                return {label:x,
                        value:x}
                
            }))
            if (categoryOptions.length >0)
                setCategory(categoryOptions[0].value)
        } catch (err){
            console.log(err.response);
        }
    }

    const addNewDiscount = async (e)=>{
        e.preventDefault()
        try{
            const discount = {
                user_id: localStorage.getItem("user_id"),
                store_id: storeId,
                discount_price:discount_price,
                end_date: end_date,
                product_id: chosenProductiD,
                category_name: category,
                prodForDiscount: prodForDiscount,
                amountForDiscount: amountForDiscount,
                min_price_for_discount: min_price_for_discount
            }
            console.log(discount)
            const response = await axios.post("http://127.0.0.1:8000/discount/"+newDiscountType+"/"+discountOn,discount)         
            console.log(response)
            window.location.reload(false);
        }catch (err){
             console.log(err.response);
             setErrMsg(err.response.data['detail'])
     }
    }

    const combineDiscounts = async (e) => {
        e.preventDefault()
        try{
            const discount = {
                user_id: localStorage.getItem("user_id"),
                store_id: storeId,
                first_discount_id: firstDiscount,
                second_discount_id: secondDiscount
            }
            console.log(discount)
            const response = await axios.post("http://127.0.0.1:8000/discount/"+combineType, discount)         
            console.log(response)
            window.location.reload(false);
        }catch (err){
             console.log(err.response);
             setErrMsg(err.response.data['detail'])
     }
    }   

    const addNewPurchaseRule = async (e)=>{
        e.preventDefault()
        try{
            const purchase = {
                user_id: localStorage.getItem("user_id"),
                store_id: storeId,
                by_category: category,  
                products_to_have_for_purchase: prodForDiscount,
                amount_of_products_to_have: amountForDiscount,
                min_price_to_have_for_purchase: min_price_for_discount
            }
            console.log(purchase)
            const response = await axios.post("http://127.0.0.1:8000/purchase/simple/" + newPurhcaseType,purchase)         
            console.log(response)
           // window.location.reload(false);
        }catch (err){
             console.log(err.response);
             setErrMsg(err.response.data['detail'])
     }         

    }

    const hasPermition = (per) =>{
        return permissions[per];
    }

    const disablePastDate = () => {
        const today = new Date();
        const dd = String(today.getDate() + 1).padStart(2, "0");
        const mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
        const yyyy = today.getFullYear();
        return yyyy + "-" + mm + "-" + dd;
    };

    const reset = () =>{
        setErrMsg("")
        setChosenProduct("1")
        setAmount("0")
        if (categoryOptions.length >0)
            setCategory(categoryOptions[0].value)
        setnewDiscountType('visible')
        setMinOrAmount('0')
        setMin_price_for_discount('0')
        setProdForDiscount('1')
        setAmountForDiscount(0)
    }
    const groupVisibleDiscounts =(x) =>{
        var type = ''
        var val = ''
        if (x['Type'] === 1){
            type = 'product'
            for (var i = 0; i < storesProducts.length; i++){
                if (options[i].key == x[discountOn]){
                    val = options[i].label 
                    break;
                }
            }
        }
        else if (x['Type'] === 2){
            type = 'category'
            for (var i = 0; i < categoryOptions.length; i++){
                if (categoryOptions[i].key == x[discountOn]){
                    val = categoryOptions[i].label 
                    break;
                }
            }
        }
        else
            type = 'store'
        const str = type === 'store' ? 'visible: ' + x['my_discount']*100 + '% on all products' :
        'visible: ' + x['my_discount']*100 + '% on ' + type + ' ' + val 
        return {label:str,
                value:x["discount_id"]}
}

    const groupConditionalDiscounts = (x)=>{
        var type = ''
        var val = ''
        var condition = ''
        if (x['Type'] === 1){
            type = 'product'
            for (var i = 0; i < storesProducts.length; i++){
                if (options[i].key == x[discountOn]){
                    val = options[i].label 
                    break;
                }
            }
        }
        else if (x['Type'] === 2){
            type = 'category'
            for (var i = 0; i < categoryOptions.length; i++){
                if (categoryOptions[i].key == x[discountOn]){
                    val = categoryOptions[i].label 
                    break;
                }
            }
        }
        else
            type = 'store'
        if (x['min_price_for_discount'] !== 0)
            condition = 'min price for discount is'
        else{
            for (var i = 0; i < storesProducts.length; i++){
                if (options[i].key == Object.entries(x['products_to_have_for_discount'])[0][0]){
                    val = options[i].label 
                    break;
                }
            }
            condition = 'bought at least ' + Object.entries(x['products_to_have_for_discount'])[0][1] + ' of product: '+ val
        }
        const str = type === 'store' ? 'conditional: ' + x['my_discount']*100 + '% on all products if':
        'conditional: ' + x['my_discount']*100 + '% on ' + type + ' ' + val + ' if ' + condition 

        return {label:str,
                value:x["discount_id"]}
}
    const getDiscounts = async ()=>  {
        try{
        const response = await axios.get('http://127.0.0.1:8000/discount/visible/'+storeId)
        console.log(response)
        const response2 = await axios.get('http://127.0.0.1:8000/discount/conditional/'+storeId)
        console.log(response2)
        // const response3 = await axios.get('http://127.0.0.1:8000/discount/combined/'+storeId)
        // console.log(response3)
        setDiscountOptions(discounts => response.data.map(groupVisibleDiscounts))
        setDiscountOptions(discounts => [...discounts, ...response2.data.map(groupConditionalDiscounts)])
        // setDiscountOptions(discounts => [...discounts, ...response3.data.map((x)=>{
        //     setDiscountOptions(inerdiscounts => [...inerdiscounts, ...[x['firstDiscount'],x['secondDiscount']]])
        // })])


        }catch (err){
            console.log(err.response);
        }

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
                <li>store products:</li>
                <div className='scroller'>
                {storesProducts.length === 0 ? <li>no products</li>: storesProducts}
                </div>
            </ul>
        </div>
        <div className='split right'>
            {Object.values(permissions).some(per => per) ? <h2>Actions:</h2>: ""}
            {/* 1 */}
                {hasPermition(1) ? <li> <Popup  onClose={reset} trigger={<button style={{margin:'5px'}}> Add new product</button>} position="right center">
                    <div>
                        please fill the information below:
                        <form  onSubmit = {addNewProduct}>
                             {errMsg !== "" ?<p style={{textAlign:'center', color:'red'}} >{errMsg}</p> : <br />}
                            <input type = 'text' name = 'name' placeholder="product name..." required onChange={(e)=> setProductName(e.target.value)}/>
                            <textarea style={{resize:'none'}} type = 'text' name = 'description' placeholder="description..."  onChange={(e)=> setDecription(e.target.value)}/>
                            <input type = 'number' name = 'price' placeholder="price..." required onChange={(e)=> setPrice(e.target.value)}/>
                            <input type = 'text' name = 'category' placeholder="category..." required onChange={(e)=> setCategory(e.target.value)}/>
                            <button style={{marginLeft: '40%'}}  onSubmit = {addNewProduct}>add</button>
                        </form>
                    </div> </Popup> </li>: ""}
            {/* 2 */}
                {hasPermition(1) ? <li><Popup onClose={reset} trigger={<button style={{margin:'5px'}}>Add products to inventory</button>} position="right center">
                <div>
                    please choose a product:
                    <form  onSubmit = {addProductToInvetory}>
                        {errMsg !== "" ?<p style={{textAlign:'center', color:'red'}} >{errMsg}</p> : <br />}
                        <select onChange={(e) => setChosenProduct(e.target.value)}>
                            {options.map((option) => (
                                <option key={option.value} value={option.value}>{option.label}</option>))}
                         </select>
                         <input type = 'number' name = 'amount' placeholder="amount..." required onChange={(e)=> setAmount(e.target.value)}/>
                        <button style={{marginLeft: '40%'}}  onSubmit = {addProductToInvetory}>add</button>
                    </form>
                </div> </Popup></li>: ""}
            {/* 3 */}
                {hasPermition(1) ? <li><Popup onClose={reset} trigger={<button style={{margin:'5px'}}>Remove products from inventory</button>} position="right center">
                    <div>
                        please choose a product:
                        <form  onSubmit = {removeProductFromInvetory}>
                        {errMsg !== "" ?<p style={{textAlign:'center', color:'red'}} >{errMsg}</p> : <br />}
                        <select onChange={(e) => setChosenProduct(e.target.value)}>
                            {options.map((option) => (
                                <option value={option.value}>{option.label}</option>))}
                         </select>
                         <input type = 'number' name = 'amount' placeholder="amount..." required onChange={(e)=> setAmount(e.target.value)}/>
                            <button style={{marginLeft: '40%'}}  onSubmit = {removeProductFromInvetory}>remove</button>
                        </form>
                    </div> </Popup></li>: ""}
            {/* 4 */}
                {hasPermition(1) ? <li><Popup onClose={reset} trigger={<button style={{margin:'5px'}}>edit product</button>} position="right center">
                    <div>
                         please choose a product and fill the information that you want to change:
                        <form  onSubmit = {editProduct}>
                            {errMsg !== "" ?<p style={{textAlign:'center', color:'red'}} >{errMsg}</p> : <br />}
                            <select onChange={(e) => setChosenProduct(e.target.value)}>
                                {options.map((option) => (
                                    <option value={option.value}>{option.label}</option>))}
                            </select>                           
                            <input type = 'text' name = 'name' placeholder="name..."  onChange={(e)=> setProductName(e.target.value)}/>
                            <textarea style={{resize:'none'}} type = 'text' name = 'description' placeholder="description..."  onChange={(e)=> setDecription(e.target.value)}/>
                            <input type = 'number' name = 'price' placeholder="price..."  onChange={(e)=> setPrice(e.target.value)}/>
                            <input type = 'text' name = 'category' placeholder="category..." onChange={(e)=> setCategory(e.target.value)}/>
                            <button style={{marginLeft: '40%'}}  onSubmit = {editProduct}>edit</button>
                        </form>
                    </div> </Popup></li>: ""}
            {/* 5 */}
                {hasPermition(2) ? <li><Popup onClose={reset} trigger={<button style={{margin:'5px'}}>Add store owner</button>} position="right center">
                <div>
                    please fill the information below:
                    <form  onSubmit = {addStoreOwner}>
                        {errMsg !== "" ?<p style={{textAlign:'center', color:'red'}} >{errMsg}</p> : <br />}
                        <input type = 'text' name = 'name' placeholder="new owner name..." required onChange={(e)=> setOfficalsName(e.target.value)}/>
                        <button style={{marginLeft: '40%'}}  onSubmit = {addStoreOwner}>add</button>
                    </form>
                </div> </Popup></li>: ""}
            {/* 6  */}
                {hasPermition(3) ? <li><Popup onClose={reset} trigger={<button style={{margin:'5px'}}>Add store manager</button>} position="right center">
                <div>
                    please fill the information below:
                    <form  onSubmit = {addStoreManager}>
                        {errMsg !== "" ?<p style={{textAlign:'center', color:'red'}} >{errMsg}</p> : <br />}
                        <input type = 'text' name = 'name' placeholder="new manager name..." required onChange={(e)=> setOfficalsName(e.target.value)}/>
                        <button style={{marginLeft: '40%'}}  onSubmit = {addStoreManager}>add</button>
                    </form>
                </div> </Popup></li>: ""}
            {/* 7 */}
                {hasPermition(4) ? <li><Popup  onClose={reset} trigger={<button style={{margin:'5px'}}>change manager permissions</button>} position="right center">
                <div>
                    in the requminets?
                    <form  onSubmit = {addNewProduct}>
                    {errMsg !== "" ?<p style={{textAlign:'center', color:'red'}} >{errMsg}</p> : <br />}
                        <input type = 'text' name = 'name' placeholder="in the requminets?..." required onChange={(e)=> setProductName(e.target.value)}/>
                        <button style={{marginLeft: '40%'}}  onSubmit = {addNewProduct}>add</button>
                    </form>
                </div> </Popup></li>: ""}
            {/* 8 */}
                {hasPermition(6) ? <li><Popup  onClose={reset} onOpen={getStoreRoles} trigger={<button style={{margin:'5px'}}>Get store's roles</button>} position="right center">
                <div>
                    {roles}
                </div> </Popup></li>: ""}
            {/* 9 */}
                {hasPermition(8) ? <li><Popup  onClose={reset} onOpen={reset} trigger={<button style={{margin:'5px'}}>add new discount</button>} position="right center">
                    <div>
                        {storesProducts.length > 0 ?
                        <form  onSubmit = {addNewDiscount}>
                        {errMsg !== "" ?<p style={{textAlign:'center', color:'red'}} >{errMsg}</p> : <br />}
                            <p>choose discount type:</p>
                            <select onChange={(e) => setnewDiscountType(e.target.value)}>
                                <option value = 'visible'>visible</option>
                                <option value = 'conditional'>conditional</option>
                            </select> 
                            {newDiscountType === 'conditional' ? <div ><p>choose condition</p><select style={{width:'200px'}} onChange={(e) => setMinOrAmount(e.target.value)}>
                                    <option value={"0"}>{"min price for discount"}</option>
                                    <option value={"1"}>{`product and the amount to have for discount`}</option>
                            </select> 
                            </div>:""}  
                            {newDiscountType === 'conditional'  ? minOrAmount === '0' ?
                            <input type = 'number' name = 'price' placeholder="min amount for a..."  onChange={(e)=> setMin_price_for_discount(e.target.value)}/> 
                            :<div> <p>choose product to have for discount </p> 
                                <select style={{width:'200px'}} onChange={(e) => setProdForDiscount(e.target.value)}>
                                {options.map((option) => (
                                    <option value={option.value}>{option.label}</option>))}
                                 </select>
                                 <p>choose the amount of the product to have for discount</p>
                                <input type = 'number' name = 'price' placeholder="amount of products to have..."  onChange={(e)=> setAmountForDiscount(e.target.value)}/> 
                             </div> : ''}  
                            <p>choose discount by:</p>   
                            <select onChange={(e) => setDiscountOn(e.target.value)}>
                                <option value = 'product'>product</option>
                                <option value = 'category'>category</option>
                                <option value = 'store'>store</option>
                            </select>          
                            {discountOn === 'product' ? <div><p>choose product to have discount on</p><select onChange={(e) => setChosenProduct(e.target.value)}>
                                {options.map((option) => (
                                    <option value={option.value}>{option.label}</option>))}
                            </select> 
                            </div>:""}  
                            {discountOn === 'category' ? <div><p>choose category to have discount on</p> <select onChange={(e) => setCategory(e.target.value)}>
                                {categoryOptions.map((option) => (
                                    <option value={option.value}>{option.label}</option>))}
                            </select> </div> :""} 
                            <p>choose end date</p>
                            <input type = 'date'min={disablePastDate()} name = 'price' placeholder="discount price..."  onChange={(e)=> setDiscount_price(e.target.value)}/> 
                            <p>discount price:</p>
                            <input type = 'number' step="0.01" name = 'price' placeholder="discount price..."  onChange={(e)=> setDiscount_price(e.target.value)}/>
                            
                            <button style={{marginLeft: '40%'}}  onSubmit = {addNewDiscount}>add</button>
            
                        </form>
                        : <p>pleasea add prodcsts first</p>}
                    </div> </Popup></li>: ""}
            {/* 10 */}
                {hasPermition(8) ? <li><Popup  onOpen={getDiscounts} onClose={reset} trigger={<button style={{margin:'5px'}}>combine discounts</button>} position="right center">
                    <div>
                    <form  onSubmit = {combineDiscounts}>
                    {errMsg !== "" ?<p style={{textAlign:'center', color:'red'}} >{errMsg}</p> : <br />}

                        <p>choose first discount</p>
                        <select  onChange={(e) => setFirstDiscount(e.target.value)} style={{width:'200px'}}>
                            {discountOptions.map((option) => (
                                            <option value={option.value}>{option.label}</option>))}
                        </select>
                        <p>choose second discount</p>
                        <select  onChange={(e) => setSecondDiscount(e.target.value)} style={{width:'200px'}}>
                            {discountOptions.map((option) => (
                                            <option value={option.value}>{option.label}</option>))}
                        </select>
                        <p>choose type of combination</p>
                        <select  onChange={(e) => setCombineType(e.target.value)} style={{width:'200px'}}>
                            <option value={'or'}>{'or'}</option>
                            <option value={'and'}>{'and'}</option>
                            <option value={'xor'}>{'xor'}</option>
                            <option value={'sum'}>{'sum'}</option>
                            <option value={'max'}>{'max'}</option>
                        </select>
                        <button style={{marginLeft: '40%'}}  onSubmit = {combineDiscounts}>add</button>
                    </form>
                  </div> </Popup></li>: ""}
            {/* 11 */}
                {hasPermition(8) ? <li><Popup  onOpen={getDiscounts} onClose={reset} trigger={<button style={{margin:'5px'}}>add purhcase rule</button>} position="right center">
                    <div>
                    <form  onSubmit = {addNewPurchaseRule}>
                    {errMsg !== "" ?<p style={{textAlign:'center', color:'red'}} >{errMsg}</p> : <br />}

                         <p>choose purchase rule by:</p>   
                            <select onChange={(e) => setDiscountOn(e.target.value)}>
                                <option value = 'product'>product</option>
                                <option value = 'category'>category</option>
                                <option value = 'price'>price</option>
                            </select> 
                        {discountOn === 'product' ?<div> <p>choose product to have for rule </p> 
                                <select style={{width:'200px'}} onChange={(e) => setProdForDiscount(e.target.value)}>
                                {options.map((option) => (
                                    <option value={option.value}>{option.label}</option>))}
                                 </select>
                                 <p>choose the amount of the product to have for rule</p>
                                <input type = 'number' name = 'price' placeholder="amount of products to have..."  onChange={(e)=> setAmountForDiscount(e.target.value)}/> 
                             </div>:""}  
                        {discountOn === 'category' ? <div><p>choose category to have rule apply on</p> <select onChange={(e) => setCategory(e.target.value)}>
                            {categoryOptions.map((option) => (
                                <option value={option.value}>{option.label}</option>))}        
                                     </select> 
                                     <p>choose the amount of the product to have for rule</p>
                                <input type = 'number' name = 'price' placeholder="amount of products to have..."  onChange={(e)=> setAmountForDiscount(e.target.value)}/> </div> :""} 
                        {discountOn === 'price' ? <div>
                                <p>choose the minimum amount to spend in store</p>
                        <input type = 'number' name = 'price' placeholder=" minimum amount..."  onChange={(e)=> setMin_price_for_discount(e.target.value)}/> </div> :""} 
                        <button style={{marginLeft: '40%'}}  onSubmit = {addNewPurchaseRule}>add</button>
                    </form>
                  </div> </Popup></li>: ""}
            
                
        </div>
    </div>
)
}

export default Store;
