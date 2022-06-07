import React, { useState, useEffect } from 'react';
import NavBar from './components/navbar';
import Counters from './components/counters.js';

function ShoppingCart() {
	// state = {
	// 	counters: [
	// 		// { id: 1, value: 5, tags: ['tag1', 'tag2', 'tag3'] },
	// 		// { id: 2, value: 0, tags: ['tag1', 'tag2', 'tag3'] },
	// 		// { id: 3, value: 0, tags: ['tag1', 'tag2', 'tag3'] },
	// 		// { id: 4, value: 0, tags: ['tag1', 'tag2', 'tag3'] },
	// 	],
	// };
	const [counters, setCounters] = useState([{ id: 1, value: 5, tags: ['tag1', 'tag2', 'tag3'] },
											{ id: 2, value: 0, tags: ['tag1', 'tag2', 'tag3'] },]);


	const handleDelete = (counterId) => {
		const counters_filtered = counters.filter((c) => c.id !== counterId);
		setCounters({ counters_filtered });
	};

	const handleIncrement = (counter) => {
		const counters2inc = [...counters];
		const idx = counters2inc.indexOf(counter);
		counters2inc[idx] = { ...counter };
		counters2inc[idx].value++;
		setCounters({ counters2inc });
	};
	//
	const handleDicrement = (counter) => {
		const counters2dic = [...this.state.counters];
		const idx = counters2dic.indexOf(counter);
		counters2dic[idx] = { ...counter };
		if (counters2dic[idx].value > 0) counters2dic[idx].value--;
		setCounters({ counters2dic });
	};

	const handleReset = () => {
		const counters2rest = counters.map((c) => {
			c.value = 0;
			return c;
		});
		setCounters({ counters2rest });
	};

	useEffect(() => {   
        // getStoreInfo()
      }, []);

	// render() {
		// console.log("App rendered !!")
	return (
		<React.Fragment>
			<NavBar
				totalCounters={
					counters.filter((c) => c.value !== 0).length
				}
			/>
			<main
				className='container'
				style={{
					position: 'fixed',
					left: 0,
					// width: 300,
				}}>
				<button style={{ cursor: 'pointer' }}>Buy Now !</button>
				<h4 style={{ color: 'red' }}>
					Discount available only for today! hurry up!!
				</h4>
				<Counters
					counters={counters}
					onDelete={handleDelete}
					onIncrement={handleIncrement}
					onDicrement={handleDicrement}
					onReset={handleReset}
				/>
			</main>
		</React.Fragment>
	);
// }
}

export default ShoppingCart;
