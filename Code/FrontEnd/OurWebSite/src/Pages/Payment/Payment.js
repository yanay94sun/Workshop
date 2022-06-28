import React, { useState, useEffect } from 'react';
import axios from "axios";
import { useNavigate } from "react-router-dom";


function Payment(){
    // const [customer_id, SetCustomer_id] = useState("");
    // const [customer_name, SetCustomer_name] = useState("");
    // const [credit_card, SetCredit_card] = useState("");
    // const [cvv, SetCvv] = useState("");
    // bla bla
    const [id, SetId] = useState(''); // teudat zehoot
    const [holder, SetHolder] = useState('');
    const [card_number, SetCard_number] = useState('');
    const [ccv, SetCcv] = useState('');
    const [year, SetYear] = useState('');
    const [month, SetMonth] = useState('');

    const [name, SetName] = useState('');
    const [address, SetAddress] = useState('');
    const [city, SetCity] = useState('');
    const [country, SetCountry] = useState('');
    const [zip, SetZip] = useState('');


    const [errMsg, setErrMsg] = useState("")
    const [amount_to_pay, SetAmount_to_pay] = useState(0);
    const [msg, setMsg] = useState('');


    const handlePayment = async (e) => {
        e.preventDefault()
        const paymentInfo = {
            customer_id: localStorage.getItem("user_id"),
            // customer_name: customer_name,
            // credit_card: credit_card,
            // cvv: cvv,
            // amount_to_pay: amount_to_pay,
            id: id,
            holder: holder,
            card_number: card_number,
            ccv: ccv,
            year: year,
            month: month,
        }
        const supplyInfo = {
            customer_id: localStorage.getItem("user_id"),
            name: name,
            address: address,
            city: city,
            country: country,
            zip: zip,
        }
        try{
			const response = await axios.post("http://127.0.0.1:8000/pay", paymentInfo);
            console.log(response.data);
            const response2 = await axios.post("http://127.0.0.1:8000/supply", supplyInfo);
            setMsg(response.data)
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
                {/*<input type = 'text' name = 'customer_name' placeholder="customer name..." required onChange={(e)=> SetCustomer_name(e.target.value)}/>*/}
                {/*<input  type = 'text' name = 'credit_card' placeholder="credit_card..."  onChange={(e)=> SetCredit_card(e.target.value)}/>*/}
                {/*<input type = 'number' name = 'cvv' placeholder="cvv..." required onChange={(e)=> SetCvv(e.target.value)}/>*/}

                <input type = 'text' name = 'id' placeholder="id..." required onChange={(e)=> SetId(e.target.value)}/>
                <input  type = 'text' name = 'holder' placeholder="holder..."  onChange={(e)=> SetHolder(e.target.value)}/>
                <input type = 'text' name = 'card_number' placeholder="card_number..." required onChange={(e)=> SetCard_number(e.target.value)}/>
                <input type = 'text' name = 'ccv' placeholder="ccv..." required onChange={(e)=> SetCcv(e.target.value)}/>
                <input type = 'text' name = 'year' placeholder="year..." required onChange={(e)=> SetYear(e.target.value)}/>
                <input type = 'text' name = 'month' placeholder="month..." required onChange={(e)=> SetMonth(e.target.value)}/>

                <input type = 'text' name = 'name' placeholder="name..." required onChange={(e)=> SetName(e.target.value)}/>
                <input  type = 'text' name = 'address' placeholder="address..."  onChange={(e)=> SetAddress(e.target.value)}/>
                <input type = 'text' name = 'city' placeholder="city..." required onChange={(e)=> SetCity(e.target.value)}/>
                <input type = 'text' name = 'country' placeholder="country..." required onChange={(e)=> SetCountry(e.target.value)}/>
                <input type = 'text' name = 'zip' placeholder="zip..." required onChange={(e)=> SetZip(e.target.value)}/>

                <h4>Your total amount after discounts is: {amount_to_pay}$</h4>
                <button style={{marginLeft: '40%'}}  onSubmit = {handlePayment}>Pay</button>
                <p></p>
				{msg === '' ? <strong> </strong> : <strong style={{color: 'red'}}> {msg}</strong>}
            </form>
        </div> 
    )
    
}

export default Payment;