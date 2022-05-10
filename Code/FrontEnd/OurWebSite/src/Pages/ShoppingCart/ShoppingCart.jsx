import React, { Component, useEffect } from 'react';
import NavBar from './components/navbar';
import Counters from './components/counters.jsx';

class ShoppingCart extends Component {
	state = {
		counters: [
			{ id: 1, value: 5, tags: ['tag1', 'tag2', 'tag3'] },
			{ id: 2, value: 0, tags: ['tag1', 'tag2', 'tag3'] },
			{ id: 3, value: 0, tags: ['tag1', 'tag2', 'tag3'] },
			{ id: 4, value: 0, tags: ['tag1', 'tag2', 'tag3'] },
		],
	};

	handleDelete = (counterId) => {
		const counters = this.state.counters.filter((c) => c.id !== counterId);
		this.setState({ counters });
	};

	handleIncrement = (counter) => {
		const counters = [...this.state.counters];
		const idx = counters.indexOf(counter);
		counters[idx] = { ...counter };
		counters[idx].value++;
		this.setState({ counters });
	};
	//
	handleDicrement = (counter) => {
		const counters = [...this.state.counters];
		const idx = counters.indexOf(counter);
		counters[idx] = { ...counter };
		if (counters[idx].value > 0) counters[idx].value--;
		this.setState({ counters });
	};

	handleReset = () => {
		const counters = this.state.counters.map((c) => {
			c.value = 0;
			return c;
		});
		this.setState({ counters });
	};
	render() {
		// console.log("App rendered !!")
		return (
			<React.Fragment>
				<NavBar
					totalCounters={
						this.state.counters.filter((c) => c.value !== 0).length
					}
				/>
				<main
					className='container'
					style={{
						position: 'fixed',
						left: 0,
						width: 200,
					}}>
					<Counters
						counters={this.state.counters}
						onDelete={this.handleDelete}
						onIncrement={this.handleIncrement}
						onDicrement={this.handleDicrement}
						onReset={this.handleReset}
					/>
				</main>
			</React.Fragment>
		);
	}
}

export default ShoppingCart;
