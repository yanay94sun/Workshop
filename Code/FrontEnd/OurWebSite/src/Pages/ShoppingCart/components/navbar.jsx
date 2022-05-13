import React, { Component } from 'react';

// stateless functional component
const NavBar = (props) => {
	return (
		<nav className='navbar navbar-light bg-light'>
			<div className='container-fluid'>
				<span className='navbar-brand mb-0 h1'>
					Navbar{' '}
					<span className='badge badge-pill badge-secondary'>
						{' '}
						{props.totalCounters}
					</span>
				</span>
			</div>
		</nav>
	);
};

export default NavBar;
