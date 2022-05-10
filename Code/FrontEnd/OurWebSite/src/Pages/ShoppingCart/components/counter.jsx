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
				<span style={{ fontSize: 15 }} className={this.getBadgeClasses()}>
					{this.formatCount()}

					<button
						style={{ width: 50 }}
						className='btn btn-secondary btn-sm m-2'
						onClick={() => this.props.onIncrement(this.props.counter)}>
						+
					</button>
					<button
						style={{ width: 50 }}
						className='btn btn-secondary btn-sm'
						onClick={() => this.props.onDicrement(this.props.counter)}>
						-
					</button>
					<button
						style={{ width: 50 }}
						className='btn btn-danger btn-sm m-2'
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
		let classes = 'badge m-2 badge-';
		classes += this.props.counter.value === 0 ? 'warning' : 'primary';
		return classes;
	}

	formatCount() {
		const { value: count } = this.props.counter;
		return count === 0 ? 'Zero' : count;
	}
}

export default Counter;
