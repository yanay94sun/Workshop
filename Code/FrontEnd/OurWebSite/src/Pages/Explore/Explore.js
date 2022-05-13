import React from "react";
import "./Explore.css"
import axios from 'axios'

function Explore(){
    //("<li>" + {input} + "</li>")
    var state ={
        text:'',
    }

    const handleChange = (e) =>{
        const {value} = e.target
        state = value
    }

    const handleSumbit = async (e) =>{
        e.preventDefault()
        const storeName = {
            text: state.text,
        }
        //const response = await axios.post("http://127.0.0.1:8000/users/open_store",storeName)
        //console.log(response)
    }

    return(
        <div>
            <div className="div-list">
                <input type="text" placeholder="Search for anything" onChange = {handleChange}/> 
                <button style={{cursor:'pointer'}} onClick={handleSumbit}>search</button>
                <div className="products-type">
                    <a href="/products/food">
                        <h1 style={{cursor:'pointer'}}>FOOD</h1>
                    </a>
                    <a href="/products/clothes">
                        <h1 style={{cursor:'pointer'}}>CLOTHES</h1>
                    </a>
                    <a href="/products/electronic">
                        <h1 style={{cursor:'pointer'}}>ELECTRONIC</h1>
                    </a>
                    <a href="/products/house-goods">
                        <h1 style={{cursor:'pointer'}}>HOUSE GOODS</h1>
                    </a>
                <ul>
                    {/* {should be a updating list here} */}

                </ul>
                </div>
            </div>
        </div>
)
}


export default Explore;     