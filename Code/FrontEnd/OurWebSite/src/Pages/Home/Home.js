import React from "react";
import {Routes , Route} from 'react-router-dom';
import Header from "../../Components/Header/Header";
import Explore from "../Explore/Explore";
import NewHome from "../NewHome/NewHome";
import ShoppingCart from "../ShoppingCart/ShoppingCart"
import MyAccount from "../MyAcoount"
import product from "../Product/Product"
import Product from "../Product/Product";


const Home = ({handleLogged}) => {
    return (
        <div>
            <Header isLogged={handleLogged}/>
            <Routes>
                <Route path ='/newHome' element= {<NewHome/>}/>
                <Route path ='/explore' element= {<Explore/>}/>
                <Route path ='/shopping-cart' element= {<ShoppingCart/>}/>
                <Route path ='/my-account' element= {<MyAccount/>}/>
                <Route path ='/product' element= {<Product/>}/>

            </Routes>
            
        </div>
    )
}

export default Home;