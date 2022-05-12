import React, {useState} from "react";
import "./MyStore.css"
import axios from 'axios'
import { useNavigate } from "react-router-dom";


function MyStores(){
    //("<li>" + {input} + "</li>")
    const Navigate = useNavigate()

    const [storeName,setStoreName] = useState('')

    const handleSumbit = async (e) =>{
        e.preventDefault()
        const storeNameToBack = {
            store_name: storeName,
        }
        const response = await axios.post("http://127.0.0.1:8000/users/open_store",storeNameToBack)
        console.log(response)
    }

    return(
        <div>
            <h3 style={{textAlign:'center'}}>{welomeText()}</h3>
            <form className="div-list" onSubmit = {handleSumbit}>
                <input type="text" placeholder="please enter store name" required onChange = {(e) => setStoreName(e.target.value)}/> 
                <button style={{ cursor:'pointer'}} onSubmit={handleSumbit}>add</button>
                <ul>
                    <li style={{cursor:'pointer'}} onClick={()=>Navigate('/Store{id}')} >exmaple store</li>
                    {/* {should be a updating list here} */}
                </ul>
            </form>
        </div>
)
}

function welomeText(){
    //if somthing 
    return "You dont have any store you own but you can create a new one here:"
    //else 
    // return "here are the stores you own"
}

export default MyStores;     