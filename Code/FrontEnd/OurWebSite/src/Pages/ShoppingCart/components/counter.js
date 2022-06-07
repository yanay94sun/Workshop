import React, { Component } from 'react';

class Counter extends Component {
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

	render() {
		return (
			<React.Fragment>
				<span>
					<span style={this.getBadgeClasses()}>{this.formatCount()}</span>

					<button
						style={{
							width: 50,
							backgroundColor: 'gray',
							margin: 5,
							cursor: 'pointer',
						}}
						// className='btn btn-secondary btn-sm m-2'
						onClick={() => this.props.onIncrement(this.props.counter)}>
						+
					</button>
					<button
						style={{
							width: 50,
							backgroundColor: 'gray',
							margin: 5,
							cursor: 'pointer',
						}}
						// className='btn btn-secondary btn-sm'
						onClick={() => this.props.onDicrement(this.props.counter)}>
						-
					</button>
					<button
						style={{
							width: 50,
							backgroundColor: 'red',
							margin: 5,
							cursor: 'pointer',
						}}
						// className='btn btn-danger btn-sm m-2'
						onClick={() => this.props.onDelete(this.props.counter.id)}>
						Delete
					</button>
				</span>
				<ul>
					{this.props.counter.tags.map((tag) => (
						<li key={tag}>{tag}</li>
					))}
				</ul>
			</React.Fragment>
		);
	}

	getBadgeClasses() {
		let badgeStyle = {
			border: '1px solid blue',
			fontSize: 18,
			margin: 5,
			marginLeft: '10px',
		};
		this.props.counter.value === 0
			? (badgeStyle.backgroundColor = 'gold')
			: (badgeStyle.backgroundColor = 'dodgerblue');

		// classes += this.props.counter.value === 0 ? 'warning' : 'primary';
		return badgeStyle;
	}

	formatCount() {
		const { value: count } = this.props.counter;
		return count === 0 ? 'Zero' : count;
	}
}

export default Counter;
