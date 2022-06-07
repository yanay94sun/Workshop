import React, {useState,useEffect} from "react";
import "./MyStore.css"
import axios from 'axios'
import { useNavigate } from "react-router-dom";


function MyStores({listItems, setListItems, ip }){
    const Navigate = useNavigate() 

    const [storeName,setStoreName] = useState('')

    const [errMsg, setErrMsg] = useState("")

    const handleSumbit = async (e) =>{
        e.preventDefault()
        const storeNameToBack = {
            store_name: storeName,
            id: ip
        }
       try{
       const response = await axios.post("http://127.0.0.1:8000/users/open_store",storeNameToBack)
       setErrMsg("")
       setListItems(listItems => [...listItems, <li key={storeName} style={{cursor:'pointer' ,width:'40px'}} onClick={()=>Navigate("../Stores/"+response.data)}>{storeName}</li>])
       console.log(response)
    } catch (err){
        console.log(err.response);
        setErrMsg(err.response.data['detail'])

    }  
    }
       
    const getMyStores = async () =>{
        try{
        const keys = listItems.map(x=> x.key)
        const response = await axios.get("http://127.0.0.1:8000/users/"+localStorage.getItem("user_id"))
        console.log(response)
        for (const [id, Sname] of Object.entries(response.data.value)) {
            if (!keys.includes(Sname))
                setListItems(listItems => [...listItems, <li key={Sname} style={{cursor:'pointer' ,width:'40px'}} onClick={()=>Navigate("../Stores/"+id)}>{Sname}</li>])
        }
        } catch (err){
            console.log(err.response);
        }
    }

    useEffect(() => {   
        getMyStores()
      }, []);

    return(
        <div>
            <h3 style={{textAlign:'center'}}>{welomeText(listItems)}</h3>
            {errMsg != "" ?<p style={{textAlign:'center', color:'red'}} >{errMsg}</p> : <br />}
            <form className="div-list" onSubmit = {handleSumbit}>
                <input type="text" placeholder="please enter store name" required onChange = {(e) => setStoreName(e.target.value)}/> 
                <button className="buttonS" style={{ cursor:'pointer'}} onSubmit={handleSumbit}>add</button>
                <ul>
                    {listItems}
                </ul>
            </form>
        </div>
)
}

function welomeText(listItems){
    if (listItems.length == 0) {
        return "You dont have any store you own but you can create a new one here:"
    }
    else {
        return "here are the stores you own"
    }
}

export default MyStores;     