import axios from 'axios';
import React from 'react';
import { useState, useEffect } from 'react';
import Counter from '../ShoppingCart/components/counter';

function Product({Products}) {
	const [name, setName] = useState('NIKE AIR JORDAN');
	const [description, setDescription] = useState(
		'the actual shoes Michel Jordan ware in his final game !'
	);
	const [rating, setRating] = useState(5);
	const [fixprice, setFixPrice] = useState(200);
	const [totalPrice, setTotalPrice] = useState(0);
	const [catagory, setCatagory] = useState('Shoes');
	const [storeId, setStoreId] = useState('');
	const [productId, setProductId] = useState('');

	const [count, setCount] = useState(0);

	// example ------------------
	// setName('FuckShit');
	// setDescription(
	// 	'this Website is suck ! and the products even worst ! and yanay gay'
	// );
	// setRating(-42);
	// setFixPrice(555);
	// setCatagory('gay stuff');
	// setStoreId(1);
	// setProductId(1);
	// // example ------------------
	const handleAddToCart = async () => {
		try {
			const args = {
				store_id: storeId,
				product_id: productId,
				quantity: count,
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
		setTotalPrice(fixprice * count);
	}, [count]);

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
					<strong>${totalPrice}</strong>
				</p>
			</div>
		</div>
		// <div>
		// 	<h1>Product</h1>
		// </div>
	);
}

export default Product;
