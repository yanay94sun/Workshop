import React , {useState} from "react";
import "./Explore.css"
import axios from 'axios'

function Explore(){
    const [text, setText] = useState("")

    const handleSumbit = async (e) =>{
        e.preventDefault()
        
    }

    return(
        <div>
            <div className="div-list">
                <input type="text" placeholder="Search for anything" onChange = {(e) => setText(e.target.value)}/> 
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