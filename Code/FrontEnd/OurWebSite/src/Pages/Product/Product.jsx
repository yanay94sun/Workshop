import axios from 'axios';
import React from 'react';
import { useState, useEffect } from 'react';
import {useParams} from 'react-router-dom'
import Counter from '../ShoppingCart/components/counter';

function Product({storesProducts}) {
	const [name, setName] = useState('');
	const [description, setDescription] = useState('');
	const [rating, setRating] = useState(0);
	const [fixprice, setFixPrice] = useState(0);
	const [totalPrice, setTotalPrice] = useState(1);
	const [catagory, setCatagory] = useState('');
	const [discount, setDiscount] = useState(0);

	const [count, setCount] = useState(0);

	const params = useParams()
	const storeId = params.storeId
	const productId = params.productId

	const getProductInfo = async () =>{
        try{
			const response = await axios.get("http://127.0.0.1:8000/product/" + storeId + "/" + productId)
			console.log(response)
			console.log(response.data['product'])
			setName(response.data['product']['_Product__name']);
			setDescription(response.data['product']['_Product__description']);
			setRating(response.data['product']['_Product__rating']);
			setFixPrice(response.data['product']['_Product__price']);
			setCatagory(response.data['product']['_Product__category']);
			getDiscounts()
        } catch (err){
            console.log(err.response);
        }
    }
		
	useEffect(() => {   
        getProductInfo()
      }, []);

	const handleAddToCart = async () => {
		try {
			const args = {
				store_id: storeId,
				product_id: productId,
				quantity: count,
				id: localStorage.getItem("user_id")
			};
			const response = await axios.post(
				'http://127.0.0.1:8000/add_product_to_shopping_cart',
				args
			);
			console.log(response.data);
		} catch (err) {
			console.log(err);
		}
	};

	useEffect(() => {
		if (discount > 0)
			setTotalPrice(fixprice * count * discount);
		else
			setTotalPrice(fixprice * count);
	}, [count, discount, fixprice]);

	const getBadgeClasses = () => {
		let badgeStyle = {
			border: '1px solid blue',
			fontSize: '18px',
			margin: '5px',
			marginLeft: '10px',
			width: '100px',
		};
		count === 0
			? (badgeStyle.backgroundColor = 'gold')
			: (badgeStyle.backgroundColor = 'dodgerblue');

		// classes += this.props.counter.value === 0 ? 'warning' : 'primary';
		return badgeStyle;
	};

	const formatCount = () => {
		// const { value: count } = count;
		return count === 0 ? 'Zero' : count;
	};
	const handleIncrement = (count) => {
		setCount(count + 1);
	};
	//
	const handleDicrement = (count) => {
		if (count > 0) setCount(count - 1);
	};

	const getDiscounts = async ()=>  {
        try{
        const response = await axios.get('http://127.0.0.1:8000/discount/visible/'+storeId)
		for (var i = 0; i < response.data.length; i++){
			if (productId === response.data[i]['discount_on']){
				setDiscount(response.data[i]['my_discount'])
			}
		}
        }catch (err){
            console.log(err.response);
        }
	}

	return (
		<div
			className='product'
			style={{
				width: '300px',
				height: '400px',
				magin: '0 auto',
				padding: '50px',
			}}>
			<div className='product-info'>
				<h1>
					{name} - {catagory}
				</h1>
				<h3>Rating: {rating}</h3>
				<p>{description}</p>
				<span>
					<span style={getBadgeClasses()}>{formatCount()}</span>
					<button
						style={{
							width: '35px',
							backgroundColor: 'gray',
							margin: '5px',
							cursor: 'pointer',
						}}
						// className='btn btn-secondary btn-sm m-2'
						onClick={() => handleIncrement(count)}>
						+
					</button>
					<button
						style={{
							width: '35px',
							backgroundColor: 'gray',
							margin: '5px',
							cursor: 'pointer',
						}}
						// className='btn btn-secondary btn-sm'
						onClick={() => handleDicrement(count)}>
						-
					</button>
				</span>
				<button style={{ cursor: 'pointer' }} onClick={() => handleAddToCart()}>
					Add to cart
				</button>
				<p>
					<strong>price: ${fixprice}</strong>
					<strong style={{color:'red'}}>      discount: {discount*100}%</strong>

				</p>
				<strong>total price: ${totalPrice}</strong>

			</div>
		</div>
	);
}

export default Product;
