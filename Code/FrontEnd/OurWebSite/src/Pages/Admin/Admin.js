import React, { useState, useEffect } from 'react';
import Popup from 'reactjs-popup';
import axios from "axios";



function Admin(){

    const [errMsg, setErrMsg] = useState('')
    const [memberToRemove, setMemberToRemove] = useState('')

    const removeMember = async (e)=>{
        e.preventDefault()
        const removed = {
            user_id:  localStorage.getItem("user_id"),
            store_id: '',
            new_owner_name:memberToRemove
        }
        try{
        const response = await axios.post("http://127.0.0.1:8000/remove_member",removed)
        console.log(response)
       // window.location.reload(false);
        } catch (err){
            console.log(err.response);
            setErrMsg(err.response.data['detail'])
        }
    }

    const reset = ()=>{
        setErrMsg('')
        setMemberToRemove('')
    }

    return(
        <div>
        <h1 style={{textAlign:'center'}}>admin page</h1>
        <Popup  onClose={reset} trigger={<button style={{margin:'5px', position:'fixed' ,left:'43%'}}> Remove member from System</button>} position="right center">
                    <div>
                        please type the name of the member to remove:
                        <form  onSubmit = {removeMember}>
                             {errMsg !== "" ?<p style={{textAlign:'center', color:'red'}} >{errMsg}</p> : <br />}
                             <input type = 'text' name = 'name' placeholder="member name..." required onChange={(e)=> setMemberToRemove(e.target.value)}/>
                            <button style={{marginLeft: '40%'}}  onSubmit = {removeMember}>remove</button>
                        </form>
                       
                    </div> </Popup>
        </div>
        
    )
}

export default Admin;