import React, {useEffect } from "react";
import axios from "axios";
import { withRouter } from "../../Components/Navigate";
import { useNavigate } from "react-router-dom";




const Transition = () => {
    const Navigate = useNavigate()

    const handleEnter = async () =>{
        // connecting to back
        // e.preventDefault();
        const response = await axios.get('http://127.0.0.1:8000/guests/enter')
        console.log(response.data)
      }

    useEffect(() => {
        handleEnter()
        Navigate('/Login')
      }, []) 

    return(
        <div> 
            <h2>lodaing</h2>
            {/* <span></span> */}
        </div>

    )
}

export default withRouter(Transition);     