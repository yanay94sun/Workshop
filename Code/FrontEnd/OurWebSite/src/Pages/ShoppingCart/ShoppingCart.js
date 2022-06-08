import React, { Component, useEffect } from 'react';
import NavBar from './components/navbar';
import Counters from './components/counters.js';
import axios from "axios";
import { useNavigate } from 'react-router-dom';


function ShoppingCart() {
	// state = {
	// 	counters: [
	// 		// { id: 1, value: 5, tags: ['tag1', 'tag2', 'tag3'] },
	// 		// { id: 2, value: 0, tags: ['tag1', 'tag2', 'tag3'] },
	// 		// { id: 3, value: 0, tags: ['tag1', 'tag2', 'tag3'] },
	// 		// { id: 4, value: 0, tags: ['tag1', 'tag2', 'tag3'] },
	// 	],
	// };
	const [products, setProducts] = useState([{ id: 1, value: 5, product_name: "Nike Jordan" },
											{ id: 2, value: 0, product_name: "Nike Lebron" },]);
	const [productName, setProductName] = useState("");

    const Navigate = useNavigate() 


	const handleDelete = (counterId) => {
		const counters_filtered = products.filter((c) => c.id !== counterId);
		setProducts( counters_filtered );
	};

	const handleIncrement = (counter) => {
		const counters2inc = [...products];
		const idx = counters2inc.indexOf(counter);
		counters2inc[idx] = { ...counter };
		counters2inc[idx].value++;
		setProducts( counters2inc );
	};
	//
	const handleDicrement = (counter) => {
		const counters2dic = [...products];
		const idx = counters2dic.indexOf(counter);
		counters2dic[idx] = { ...counter };
		if (counters2dic[idx].value > 0) counters2dic[idx].value--;
		setProducts( counters2dic );
	};

	const handleReset = () => {
		const counters2rest = products.map((c) => {
			c.value = 0;
			return c;
		});
		setProducts(counters2rest );
	};

	const getProductInfo = async (storeId, productId) =>{
        let res = ""
		try{
			const response = await axios.get("http://127.0.0.1:8000/product/" + storeId + "/" + productId)
			 res = response.data['product']['_Product__name'];
			// return res;
			console.log(res);
			setProductName(res);
			// return res;
			// console.log(response)
			// console.log(response.data['product'])
			// setName(response.data['product']['_Product__name']);
			// setDescription(response.data['product']['_Product__description']);
			// setRating(response.data['product']['_Product__rating']);
			// setFixPrice(response.data['product']['_Product__price']);
			// setCatagory(response.data['product']['_Product__category']);
        } catch (err){
            console.log(err.response);
        }
		// return res;
    }

	// const handleBuyNow = 

	const getCartInfo = async () =>{
        try{
            const response = await axios.get("http://127.0.0.1:8000/cart/" + localStorage.getItem("user_id"));
            console.log(response.data["shopping_baskets"]);
			const products_temp = [];
			const basket = response.data["shopping_baskets"];
			for (const store in basket) {
				// console.log(basket[item]["_ShoppingBasket__store"])
				const store_id = basket[store]["_ShoppingBasket__store"];
				// console.log(basket[store]["_ShoppingBasket__purchase_quantities"]);
				const productId_qunt = basket[store]["_ShoppingBasket__purchase_quantities"]; 
				for (const product_id in productId_qunt){
					// console.log(product_id);
					const quantity = productId_qunt[product_id];
					// console.log(quantity);
					// getProductInfo(store_id, product_id);
					const response = await axios.get("http://127.0.0.1:8000/product/" + store_id + "/" + product_id)
					const product_name = response.data['product']['_Product__name'];
					const product_price = response.data['product']['_Product__price'];
					// const product_name = getProductInfo(store_id, product_id); //productName
					// console.log(product_name)
					products_temp.push({id: [store_id, product_id], 
										value: quantity,
										product_name: product_name,
										product_price: product_price * quantity})
				}
				
			}
			console.log(products_temp);
			setProducts(products_temp);
			

//

        }
        catch (err){
            console.log(err.response);
        }
    }

	useEffect(() => {   
        getCartInfo()
      }, []);

	// render() {
		// console.log("App rendered !!")
	return (
		<div>
			{/* {console.log(Array.isArray(counters))} */}
			<NavBar
				totalCounters={
					products.filter((c) => c.value !== 0).length
					
				}
			/>
			<div
				className='container'
				style={{
					position: 'fixed',
					left: 0,
					// width: 300,
				}}>
				<button style={{ cursor: 'pointer' }} onClick={() => Navigate("../payment")}>Buy Now !</button>
				<h4 style={{ color: 'red' }}>
					Discount available only for today! hurry up!!
				</h4>
				<Counters
					counters={products}
					onDelete={handleDelete}
					onIncrement={handleIncrement}
					onDicrement={handleDicrement}
					onReset={handleReset}
				/>
			</div>
		</div>
	);
// }
}

export default ShoppingCart;
