import React from 'react';
import Link from "@material-ui/core/Link";

function OfferLoading(Component) {
	return function OfferLoadingComponent({ isLoading, ...props }) {
		if (!isLoading) return <Component {...props} />;
		return (
			<p style={{ fontSize: '25px' }}>
				Please wait, data is loading... If are not logged in, please <Link href="/login/">Login</Link> first.
			</p>
		);
	};
}
export default OfferLoading;