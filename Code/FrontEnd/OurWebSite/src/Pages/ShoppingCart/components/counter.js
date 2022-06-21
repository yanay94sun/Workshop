import React, { useState, useEffect } from 'react';

function Counter({onDelete, onIncrement, onDicrement, counter}) {
	// state = {
	// 	value: this.props.counter.value,
	// 	tags: ['tag1', 'tag2', 'tag3'],
	// };

	// handleIncrement = () => {
	// 	this.setState({ value: this.props.counter.value + 1 });
	// };
	// handleDicrement = () => {
	// 	this.setState({ value: this.props.counter.value - 1 });
	// };

	// render() {
	const getBadgeClasses = () => {
		let badgeStyle = {
			border: '1px solid blue',
			fontSize: 18,
			margin: 5,
			marginLeft: '10px',
		};
		counter.value === 0
			? (badgeStyle.backgroundColor = 'gold')
			: (badgeStyle.backgroundColor = 'dodgerblue');

		// classes += this.props.counter.value === 0 ? 'warning' : 'primary';
		return badgeStyle;
	}

	const formatCount = () => {
		const { value: count } = counter;
		return count === 0 ? 'Zero' : count;
	}
	return (
		<div>
			<span>
				<span style={getBadgeClasses()}>{formatCount()}</span>

				{/* <button
					style={{
						width: 50,
						backgroundColor: 'gray',
						margin: 5,
						cursor: 'pointer',
					}}
					// className='btn btn-secondary btn-sm m-2'
					onClick={() => onIncrement(counter)}>
					+
				</button> */}
				{/* <button
					style={{
						width: 50,
						backgroundColor: 'gray',
						margin: 5,
						cursor: 'pointer',
					}}
					// className='btn btn-secondary btn-sm'
					onClick={() => onDicrement(counter)}>
					-
				</button> */}
				<span>{counter.product_name}  {counter.product_price}$  </span>
				<button
					style={{
						width: 50,
						backgroundColor: 'red',
						margin: 5,
						cursor: 'pointer',
					}}
					// className='btn btn-danger btn-sm m-2'
					onClick={() => onDelete(counter.id)}>
					Delete
				</button>
			</span>
			{/* <ul>
				{counter.tags.map((tag) => (
					<li key={tag}>{tag}</li>
				))}
			</ul> */}
		</div>
	);
	// }

	
}

export default Counter;
