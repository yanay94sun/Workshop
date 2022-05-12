import axios from "axios";
import React from "react";
import { withRouter } from "../../Components/Navigate";
import "./Login.css";
// import { FormProvider, useForm } from "react-hook-form";


class Login extends React.Component{
    state ={
        username:'',
        password:'',
    }
    handleChange = (e) =>{
        const {name,value} = e.target
        this.setState({[name]:value})
    }
    handleSubmit = async (e) =>{
        e.preventDefault()
        const {name,value} = e.target
        const signIn = {
            username: this.state.username,
            password: this.state.password
        }
        try{
            console.log(signIn)
            const response = await axios.post("http://127.0.0.1:8000/guests/login",signIn)
            this.props.isLogin(true)
            console.log(response)
            this.props.navigate('/home')
            } catch (err){
                console.log(err.response);
            }
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
                        <input type = 'text' name = 'username' placeholder="username..." required onChange = {this.handleChange}/>
                        <input type = 'password' name ='password' placeholder="password..." required onChange = {this.handleChange}/>
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
