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
                <ul>
                    {/* {should be a updating list here} */}
                </ul>
            </div>
        </div>
)
}


export default Explore;     