import React , {useState, useEffect} from "react";
import "./Explore.css"
import axios from 'axios'
import { useNavigate } from "react-router-dom";


function Explore(){

    const Navigate = useNavigate() 


    const [stores,setStores] = useState([])  // list of all stores

    const [foundStores,setFoundStores] = useState([]) // list of stores from serach

    const get_stores = async ()=>{

        try{
            const response = await axios.get("http://127.0.0.1:8000/stores")
            setStores(stores => [...stores,...response.data])
        }catch (err){
                console.log(err.response);
            }
    
    }

    useEffect(() => {
        get_stores();
      }, []);

    const get_store = (name) => {
        const res = stores.filter(obj => obj["store_name"].includes(name))
        console.log(res)
        return res
    }

    const [text, setText] = useState("")
    
    const [searchType, setSearchType] = useState(true) // true is products

    const [proudctType, setProudctType] = useState(true) // true is by name


    const handleSumbit = async (e) =>{
        e.preventDefault()
        if (!searchType){
            setFoundStores(get_store(text).map(x=><li key={x["store_name"]} style={{cursor:'pointer'}} onClick={()=>Navigate("../Stores/"+x["ID"])}>{x["store_name"]}</li>))
        }
    }


    return(
        <div>
            <div className="div-list">
                <table>
                    <tbody>
                <tr className="table">
                    <td ><input type="radio"  name="type" checked={!searchType} onChange={() =>setSearchType(!searchType)}/>search stores</td>
                    <td style={{paddingLeft: "200px"}}><input type="radio" name="type" checked={searchType} onChange={() =>setSearchType(!searchType)}/>search prodcuts</td>
                </tr>
                </tbody>
                </table>

                <input type="text" placeholder="Search for anything" onChange = {(e) => setText(e.target.value)}/> 
                <button className="buttonS" style={{cursor:'pointer'}} onClick={handleSumbit}>search</button>
                {searchType ?
                <table>
                    <tbody>
                    <tr className="table">
                        <th style={{paddingLeft: "40px"}}><input type="radio" name="search" checked={proudctType} onChange={() =>setProudctType(!proudctType)}/>by name</th>
                        <th style={{paddingLeft: "70px"}}><input type="radio" name="search" checked={!proudctType} onChange={() =>setProudctType(!proudctType)}/>by category</th>
                    </tr>
                    </tbody>
                    </table>
                : ""}
                <div className="products-type">
                <ul>
                    {foundStores}
                </ul>
                </div>
            </div>
        </div>
)
}


export default Explore;     