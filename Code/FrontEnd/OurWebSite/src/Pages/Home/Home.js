import React , {useEffect, useState} from "react";
import {Routes , Route} from 'react-router-dom';
import Header from "../../Components/Header/Header";
import Explore from "../Explore/Explore";
import MyStores from "../MyStores/MyStores";
import ShoppingCart from "../ShoppingCart/ShoppingCart"
import MyAccount from "../MyAccount"
import Product from "../Product/Product";
import Store from "../Store/Store"
import axios from "axios";


const Home = ({setLogin,isLogged}) => {
    const [storeList,setStoreList] = useState([])   
    const [products, setProducts] = useState([]); //{producdid: product} should get from database
    useEffect(() => {
        const getProducts = async () => {
            try {
           const response = await axios.get('http://127.0.0.1:8000/')
           setProducts(response.data) 

        }catch{

        }
        getProducts();
        }
    }, []);
    return (
        <div>
            <Header handleLogin={setLogin} checkLogged = {isLogged}/>
            <Routes>
                <Route path ='/MyStores' element= {<MyStores listItems={storeList} setListItems ={setStoreList}/>}/>
                <Route path ='/explore' element= {<Explore/>}/>
                <Route path ='/shopping-cart' element= {<ShoppingCart/>}/>
                <Route path ='/my-account/:userId' element= {<MyAccount/>}/>
                <Route path="/stores/:storeId" element= {<Store products = {products}/>}/>
                <Route path ='/products/:productId' element= {<Product/>}/>
            </Routes>
            
        </div>
    )
}

export default Home;