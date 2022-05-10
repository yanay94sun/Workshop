import React from "react";
import { withRouter } from "../../Components/Navigate";
import "../Register/Register.css"
import axios from 'axios'


class Register extends React.Component{
    state ={
        fullName:'',
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
            username: this.state.fullName,
            // email: this.state.email,
            password: this.state.pwd
        }
        const response = await axios.post("http://127.0.0.1:8000/guests/register",signUp)
        console.log(response.data)
        this.setState({register:true})
    }
    render(){
        if(!this.state.register)
        return (
            <div className="div-register">
            <div>
                <form onSubmit = {this.handleSubmit}>
                    <p style={{textAlign: "center"}}>Enter your email and password</p>
                    <input type = 'text' name = 'fullName' placeholder="fullName..." required onChange = {this.handleChange}/>
                    <input type = 'email' name = 'email' placeholder="email..." required onChange = {this.handleChange}/>
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
                    <p style={{textAlign:"center"}}>Go back to <span style={{color:'dodgerblue', cursor:'pointer'}} onClick={() => this.props.navigate('/')()}>Login page</span></p>
                </div>
                )
        }
        }
}

export default withRouter(Register);