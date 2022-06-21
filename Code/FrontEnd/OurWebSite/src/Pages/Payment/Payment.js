import React, { useState, useEffect } from 'react';
import axios from "axios";
import { useNavigate } from "react-router-dom";


function Payment(){
    const [customer_id, SetCustomer_id] = useState("");
    const [customer_name, SetCustomer_name] = useState("");
    const [credit_card, SetCredit_card] = useState("");
    const [cvv, SetCvv] = useState("");
    const [errMsg, setErrMsg] = useState("")
    const [amount_to_pay, SetAmount_to_pay] = useState(0);



    const handlePayment = async (e) => {
        e.preventDefault()
        const paymentInfo = {
            customer_id: localStorage.getItem("user_id"),
            customer_name: customer_name,
            credit_card: credit_card,
            cvv: cvv,
            amount_to_pay: amount_to_pay,
        }
        try{
			const response = await axios.post("http://127.0.0.1:8000/pay", paymentInfo);
            console.log(response.data);
        } catch (err){
            console.log(err.response);
        }
    }
    
    const getTotalPrice = async () => {
        try{
			const response = await axios.get("http://127.0.0.1:8000/get_cart_price/" + localStorage.getItem('user_id'));
            console.log(response);
            SetAmount_to_pay(response.data)
        } catch (err){
            console.log(err.response);
        }
    }

    useEffect(() => {   
        getTotalPrice()
      }, []);


    return (
        <div>
            please fill the information below:
            <form  onSubmit = {handlePayment}>
                    {errMsg !== "" ?<p style={{textAlign:'center', color:'red'}} >{errMsg}</p> : <br />}
                <input type = 'text' name = 'customer_name' placeholder="customer name..." required onChange={(e)=> SetCustomer_name(e.target.value)}/>
                <input  type = 'text' name = 'credit_card' placeholder="credit_card..."  onChange={(e)=> SetCredit_card(e.target.value)}/>
                <input type = 'number' name = 'cvv' placeholder="cvv..." required onChange={(e)=> SetCvv(e.target.value)}/>
                <h4>Your total amount after discounts is: {amount_to_pay}$</h4>
                <button style={{marginLeft: '40%'}}  onSubmit = {handlePayment}>Pay</button>
            </form>
        </div> 
    )
    
}

export default Payment;