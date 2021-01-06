import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import CssBaseline from '@material-ui/core/CssBaseline';
import { makeStyles } from "@material-ui/core/styles";
import { NavLink } from 'react-router-dom';
import Link from '@material-ui/core/Link';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
    appBar: {
        borderBottom: `1px solid ${theme.palette.divider}`,
    },
    link: {
		margin: theme.spacing(1, 1.5),
	},
	toolbarTitle: {
		flexGrow: 1,
	},
}));

function Header() {
    const classes = useStyles();
    return (
        <React.Fragment>
            <CssBaseline/>
            <AppBar
                position="static"
                color="inherit"
                elevation={0}
                className={classes.appBar}
            >
                <Toolbar className={classes.toolbar}>
                    <Link
                        component={NavLink}
                        to="/"
                        underline="none"
                        color="inherit"
                    >
                    <Typography variant="h6" color="inherit" noWrap className={classes.toolbarTitle}>
                        MotoCrawler
                    </Typography>
                    </Link>
                    <Button
                        color="textPrimary"
                        href="#"
                        variant="outlined"
                        className={classes.link}
                        component={NavLink}
                        to="/register"
                    >
                        Register
                    </Button>
                    <Button
                        href="#"
                        color="primary"
                        variant="outlined"
                        className={classes.link}
                        component={NavLink}
                        to="/login"
                    >
                        Login
                    </Button>
                    <Button
                        href="#"
                        color="primary"
                        variant="outlined"
                        className={classes.link}
                        component={NavLink}
                        to="/logout"
                    >
                        Logout
                    </Button>
                </Toolbar>
            </AppBar>
        </React.Fragment>
    );
}

export default Header;
