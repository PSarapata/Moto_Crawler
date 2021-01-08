import React, { Component } from 'react';
import axiosInstance from '../axios';

import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Paper from '@material-ui/core/Paper';
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        MotoCrawler by Paweł Sarapata
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const useStyles = theme => ({
    root: {
      height: '100vh',
    },
    image: {
      backgroundImage: `url(https://i.pinimg.com/originals/0e/42/86/0e4286c3fdc428df4671114045b9edb2.jpg)`,
      backgroundRepeat: 'no-repeat',
      backgroundColor:
        theme.palette.type === 'light' ? theme.palette.grey[50] : theme.palette.grey[900],
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    },
    paper: {
      margin: theme.spacing(8, 4),
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
      marginTop: theme.spacing(1),
    },
    submit: {
      margin: theme.spacing(3, 0, 2),
    },
});

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {username: "", password: ""};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmitWThen = this.handleSubmitWThen.bind(this);
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  handleSubmitWThen(event){
      event.preventDefault();
      axiosInstance.post('/token/obtain/', {
              username: this.state.username,
              password: this.state.password
          }).then(
              result => {
                  axiosInstance.defaults.headers['Authorization'] = "JWT " + result.data.access;
                  localStorage.setItem('access_token', result.data.access);
                  localStorage.setItem('refresh_token', result.data.refresh);
                  localStorage.setItem('Username', this.state.username ? this.state.username : 'anonymous');
              },
              alert("You are now logged in, happy browsing!"),
              this.props.history.push('/'),
              window.location.reload()
      ).catch (error => {
          throw error;
      })
  }


  render() {

    const { classes } = this.props;

    return (
        <Grid container component="main" className={classes.root}>
          <CssBaseline/>
          <Grid item xs={false} sm={4} md={7} className={classes.image}/>
          <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
            <div className={classes.paper}>
              <Avatar className={classes.avatar}>
                <LockOutlinedIcon/>
              </Avatar>
              <Typography component="h1" variant="h5">
                Sign in
              </Typography>
              <form className={classes.form} onSubmit={this.handleSubmitWThen} noValidate>
                <TextField
                    variant="outlined"
                    required
                    fullWidth
                    id="username"
                    label="Username"
                    name="username"
                    value={this.state.username}
                    autoComplete="username"
                    onChange={this.handleChange}
                />
                <TextField
                    variant="outlined"
                    margin="normal"
                    required
                    fullWidth
                    name="password"
                    value={this.state.password}
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="current-password"
                    onChange={this.handleChange}
                />
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="primary"
                    className={classes.submit}
                >
                  Sign In
                </Button>
                <Grid container>
                  <Grid item>
                    <Link href="/register/" variant="body2">
                      {"Don't have an account? Sign Up"}
                    </Link>
                  </Grid>
                </Grid>
                <Box mt={5}>
                  <Copyright/>
                </Box>
              </form>
            </div>
          </Grid>
        </Grid>
    );
  }
}
export default withStyles(useStyles)(Login)