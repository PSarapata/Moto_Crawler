import React, { useEffect } from 'react';
import axiosInstance from '../axios';
import { useHistory } from 'react-router-dom';

export default function SignOut() {
	const history = useHistory();

	useEffect(() => {
		axiosInstance.post('user/logout/blacklist/', {
			refresh_token: localStorage.getItem('refresh_token'),
		});
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		localStorage.removeItem('Username');
		axiosInstance.defaults.headers['Authorization'] = null;
		history.push('/login');
		window.location.reload();
	});
	return <div>Logout</div>;
}