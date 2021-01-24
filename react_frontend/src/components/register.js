import React, { useState } from 'react';
import axiosInstance from '../axios';
import { useHistory } from 'react-router-dom';
//MaterialUI
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';

const useStyles = makeStyles((theme) => ({
	paper: {
		marginTop: theme.spacing(8),
		display: 'flex',
		flexDirection: 'column',
		alignItems: 'center',
	},
	avatar: {
		margin: theme.spacing(1),
		backgroundColor: theme.palette.secondary.main,
	},
	form: {
		width: '100%', // Fix IE 11 issue.
		marginTop: theme.spacing(3),
	},
	submit: {
		margin: theme.spacing(3, 0, 2),
	},
}));

export default function Register() {
	const history = useHistory();
	const initialFormData = Object.freeze({
		email: '',
		username: '',
		password: '',
	});

	const [formData, updateFormData] = useState(initialFormData);
	let [usernameErrs, setUsernameErr] = useState('');
	let [emailErrs, setEmailErr] = useState('');
	let [passwordErrs, setPasswordErr] = useState('');

	const handleChange = (e) => {
		updateFormData({
			...formData,
			// Trimming any whitespace
			[e.target.name]: e.target.value.trim(),
		});
	};

	const handleSubmit = (e) => {
		usernameErrs = ''
		emailErrs = ''
		passwordErrs = ''

		e.preventDefault();
		console.log(formData);

		if (validateForm()) {
			axiosInstance
				.post(`user/create/`, {
					email: formData.email,
					username: formData.username,
					password: formData.password,
				})
				.then((res) => {
					history.push('/login');
					alert("Account has been created, you can now log in!")
					console.log(res);
					console.log(res.data);
				});
		}
	};

	const validateForm = () => {
		let formIsValid = true
		let username = formData.username
		let email = formData.email
		let password = formData.password

		if (!username) {
			formIsValid = false
			setUsernameErr(usernameErrs + '*Please enter your username.\n')
		}

		if (username) {
			if (!username.match(/^\w+$/)) {
				formIsValid = false
				setUsernameErr(usernameErrs + '*Only alphanumeric characters are allowed.\n')
			}
		}

		if (!email) {
			formIsValid = false
			setEmailErr(emailErrs + '*Please enter your email.\n')
		}

		if (email) {
			let pattern = new RegExp(/^(('[\w-\s]+')|([\w-]+(?:\.[\w-]+)*)|('[\w-\s]+')([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
			if (!pattern.test(email)) {
				formIsValid = false
				setEmailErr(emailErrs + '*Please enter valid email\n')
			}
		}

		if (!password) {
			formIsValid = false
			setPasswordErr(passwordErrs + '*Please enter your password.\n')
		}

		if (password) {
			if (!password.match(new RegExp("^(?=.*[a-z])(?=.*[0-9])(?=.{6,})"))) {
				formIsValid = false
				setPasswordErr(passwordErrs + '*Password must contain alphanumeric characters, minimum length 6.\n')
			}
		}

		return formIsValid
	}


	const classes = useStyles();

	return (
		<Container component="main" maxWidth="xs">
			<CssBaseline />
			<div className={classes.paper}>
				<Avatar className={classes.avatar}></Avatar>
				<Typography component="h1" variant="h5">
					Register
				</Typography>
				<form className={classes.form} noValidate>
					<Grid container spacing={2}>
						<Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								id="email"
								label="Email Address"
								name="email"
								autoComplete="email"
								onChange={handleChange}
							/>
							<div className='errorMsg' style={{color: "red"}}>{emailErrs}</div>
						</Grid>
						<Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								id="username"
								label="Username"
								name="username"
								autoComplete="username"
								onChange={handleChange}
							/>
							<div className='errorMsg' style={{color: "red"}}>{usernameErrs}</div>
						</Grid>
						<Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								name="password"
								label="Password"
								type="password"
								id="password"
								autoComplete="current-password"
								onChange={handleChange}
							/>
							<div className='errorMsg' style={{color: "red"}}>{passwordErrs}</div>
						</Grid>
					</Grid>
					<Button
						type="submit"
						fullWidth
						variant="contained"
						color="primary"
						className={classes.submit}
						onClick={handleSubmit}
					>
						Sign Up
					</Button>
					<Grid container justify="flex-end">
						<Grid item>
							<Link href="/login/" variant="body2">
								Already have an account? Sign in
							</Link>
						</Grid>
					</Grid>
				</form>
			</div>
		</Container>
	);
}