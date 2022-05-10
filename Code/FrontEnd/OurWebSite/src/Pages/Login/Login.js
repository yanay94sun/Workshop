import axios from "axios";
import React from "react";
import { withRouter } from "../../Components/Navigate";
import "./Login.css";
// import { FormProvider, useForm } from "react-hook-form";


class Login extends React.Component{
    state ={
        email:'',
        pwd:''
    }
    handleChange = (e) =>{
        const {name,value} = e.target
        // console.log(name, value)
        this.setState({[name]:value})
    }
    handleSubmit = (e) =>{
        e.preventDefault()
        // connecting to back
        const {name,value} = e.target
        console.log(name, value)

        this.props.isLogin(true)
        this.props.navigate('/home')
    }
    handleGuestSubmit = (e) =>{
        e.preventDefault()
        this.props.navigate('/home')
    }
    render(){

        return (
            <div>
            <div className="div-login">
                <div className="div-login-logo">
                </div>
                <div>
                    <form onSubmit = {this.handleSubmit}>
                        <input type = 'email' name = 'email' placeholder="email..." required onChange = {this.handleChange}/>
                        <input type = 'password' name ='pwd' placeholder="password..." required onChange = {this.handleChange}/>
                        <button onSubmit = {this.handleSubmit}>Log in</button>
                    </form>
                    <form onSubmit={this.handleGuestSubmit}>
                    <button className="btnGuest" onSubmit = {this.handleGuestSubmit}>Enter as guest</button>

                    </form>
                    
                </div>
            </div>
            <div className="register-text">
                <p>not registerd? <span style={{color:'dodgerblue', cursor:'pointer'}} onClick={() => this.props.navigate('/register')}>click here</span></p>
            </div>
        </div>
        )
    }
}

export default withRouter(Login);
