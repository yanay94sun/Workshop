import React, { Component } from 'react';
import Counter from './counter';

class Counters extends Component {
	render() {
		return (
			<div className='container'>
				<button className='btn btn-primary m-2' onClick={this.props.onReset}>
					Reset
				</button>
				<br />
				{this.props.counters.map((counter) => (
					<Counter
						key={counter.id}
						onDelete={this.props.onDelete}
						onIncrement={this.props.onIncrement}
						onDicrement={this.props.onDicrement}
						counter={counter} //
					/>
				))}
			</div>
		);
	}
}

export default Counters;
