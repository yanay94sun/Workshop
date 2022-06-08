import React, { useState, useEffect } from 'react';
import Counter from './counter';

function Counters({counters, onDelete, onIncrement, onDicrement, onReset}) {
	// render() {
		return (
			<div className='container'>
				{counters.map((counter) => (
					<Counter
						key={counter.id}
						onDelete={onDelete}
						onIncrement={onIncrement}
						onDicrement={onDicrement}
						counter={counter} //
					/>
				))}
				<br />
				<button
					className='btn btn-primary m-2'
					onClick={onReset}
					style={{ cursor: 'pointer' }}>
					Reset
				</button>
			</div>
		);
	// }
}

export default Counters;
