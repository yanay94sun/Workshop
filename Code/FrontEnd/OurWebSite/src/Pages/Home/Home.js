import React from "react";
import {Routes , Route} from 'react-router-dom';
import Header from "../../Components/Header/Header";
import Explore from "../Explore/Explore";
import NewHome from "../NewHome/NewHome";

const Home = ({handleLogged}) => {
    return (
        <div>
            <Header isLogged={handleLogged}/>
            <Routes>
                <Route path ='/newHome' element= {<NewHome/>}/>
                <Route path ='/explore' element= {<Explore/>}/>
            </Routes>
            
        </div>
    )
}

export default Home;