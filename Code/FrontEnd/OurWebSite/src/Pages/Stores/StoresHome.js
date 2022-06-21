import React , {useEffect, useState} from "react";
import {Routes , Route} from 'react-router-dom';
import axios from "axios";
import Store from "../Store/Store";
import Product from "../Product/Product";


const StoreHome = ({myId}) => {
    // need to replace logic in store and place it in here (calling axios)

    const [storesProducts, setStoresProducts] = useState([])

    return (
        <div>
            <Routes>
                <Route path = '/' element = {<Store storesProducts = {storesProducts} setStoresProducts = {setStoresProducts}/>}/>
                <Route path ='/:productId' element= {<Product/>}/>
            </Routes>
            
        </div>
    )
}

export default StoreHome;