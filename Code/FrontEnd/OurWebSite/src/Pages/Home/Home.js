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
import HomePage from "../HomePage/HomePage";
import StoreHome from "../Stores/StoresHome";
import Payment from "../Payment/Payment"

const Home = ({setLogin,isLogged,myId}) => {

    const [myStoreList,setMyStoreList] = useState([])   

    return (
        <div>
            <Header handleLogin={setLogin} checkLogged = {isLogged} ip = {myId}/>
            <Routes>
                <Route path = '/' element = {<HomePage/>}/>
                <Route path ='/MyStores' element= {<MyStores listItems={myStoreList} setListItems ={setMyStoreList} ip = {myId}/>}/>
                <Route path ='/explore' element= {<Explore/>}/>
                <Route path ='/shopping-cart' element= {<ShoppingCart/>}/>
                <Route path ='/my-account/:userId' element= {<MyAccount/>}/>
                <Route path="/stores/:storeId/*" element= {<StoreHome ip = {myId}/>}/>
                <Route path="/payment" element = {<Payment/>}/>
            </Routes>
            
        </div>
    )
}

export default Home;