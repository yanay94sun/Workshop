import React, { Component } from 'react';
import Counter from './counter';

class Counters extends Component {
	render() {
		return (
			<div className='container'>
				{this.props.counters.map((counter) => (
					<Counter
						key={counter.id}
						onDelete={this.props.onDelete}
						onIncrement={this.props.onIncrement}
						onDicrement={this.props.onDicrement}
						counter={counter} //
					/>
				))}
				<br />
				<button
					className='btn btn-primary m-2'
					onClick={this.props.onReset}
					style={{ cursor: 'pointer' }}>
					Reset
				</button>
			</div>
		);
	}
}

export default Counters;
