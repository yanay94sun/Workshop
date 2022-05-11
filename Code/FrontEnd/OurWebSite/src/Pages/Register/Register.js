import React from "react";
import { withRouter } from "../../Components/Navigate";
import "../Register/Register.css"
import axios from 'axios'
import {useNavigate} from "react-router-dom"; 

const USER_REGEX = /^[A-z][A-z0-9-_]{3,23}$/;
const PWD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{8,24}$/;
const REGISTER_URL = '/register';

class Register extends React.Component{
    state ={
        userName:'',
        email:'',
        pwd:'',
        register:false 
    }
    handleChange = (e) =>{
        const {name,value} = e.target
        this.setState({[name]:value})
    }
    handleSubmit = async (e) =>{
        //this.props.navigate('/')
        e.preventDefault()
        const signUp = {
            username: this.state.userName,
            // email: this.state.email,
            password: this.state.pwd
        }
        try{
        const response = await axios.post("http://127.0.0.1:8000/guests/register",signUp)
        this.setState({register:true})

        } catch (err){
            console.log(err.response);
            this.handleSubmit()
        }
        // console.log(response.data)
        
    }

    // handleClick = ()=>{
    //     const navigate = useNavigate();
    //     navigate('/')
    // }
    render(){
        if(!this.state.register)
        return (
            <div className="div-register">
                    <button type="button" className="button-header" onClick={() => this.props.navigate("/Login")} style={{ cursor:'pointer', position: 'fixed',width: 50, right: '10px', top: '5px'}}>Back</button>
            <div>
                <form onSubmit = {this.handleSubmit}>
                    <p style={{textAlign: "center"}}>Enter your email and password</p>
                    {/* <input type = 'text' name = 'fullName' placeholder="fullName..." required onChange = {this.handleChange}/> */}
                    <input type = 'text' name = 'userName' placeholder="username..." required onChange = {this.handleChange}/>
                    <input type = 'password' name ='pwd' placeholder="password..." required onChange = {this.handleChange}/>
                    <button style={{backgroundColor:'rgb(161, 28, 28)'}} onSubmit = {this.handleSubmit}>Register</button>
                </form>
            </div>
        </div>
        )
        else{
            return(
                <div className="div-register">
                    <h1 style={{textAlign:"center"}}>Registration complete :)</h1>
                    <p style={{textAlign:"center"}}>Go back to <span style={{color:'dodgerblue', cursor:'pointer'}} onClick={() => this.props.navigate('/Login')}>Login page</span></p>
                </div>
                )
        }
        }
}

export default withRouter(Register);