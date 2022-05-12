import React from "react";
import {Routes , Route} from 'react-router-dom';
import Header from "../../Components/Header/Header";
import Explore from "../Explore/Explore";
import MyStores from "../MyStores/MyStores";
import ShoppingCart from "../ShoppingCart/ShoppingCart"
import MyAccount from "../MyAccount"
import Product from "../Product/Product";
import Store from "../Store/Store"


const Home = ({handleLogged}) => {
    return (
        <div>
            <Header isLogged={handleLogged}/>
            <Routes>
                <Route path ='/MyStores' element= {<MyStores/>}/>
                <Route path ='/explore' element= {<Explore/>}/>
                <Route path ='/shopping-cart' element= {<ShoppingCart/>}/>
                <Route path ='/my-account' element= {<MyAccount/>}/>
                <Route path="/stores/:storeId" element= {<Store/>}/>
                <Route path ='/product' element= {<Product/>}/>
            </Routes>
            
        </div>
    )
}

export default Home;