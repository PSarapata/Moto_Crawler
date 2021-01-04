import React from 'react';

function OfferLoading(Component) {
	return function OfferLoadingComponent({ isLoading, ...props }) {
		if (!isLoading) return <Component {...props} />;
		return (
			<p style={{ fontSize: '25px' }}>
				Please wait, data is loading...
			</p>
		);
	};
}
export default OfferLoading;