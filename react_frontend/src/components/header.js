import React, {useState} from 'react';
import { NavLink } from 'react-router-dom';
import { useHistory } from 'react-router-dom';

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import CssBaseline from '@material-ui/core/CssBaseline';
import { makeStyles, withStyles } from "@material-ui/core/styles";
import Breadcrumbs from '@material-ui/core/Breadcrumbs';
import Link from '@material-ui/core/Link';
import Button from '@material-ui/core/Button';
import SearchBar from 'material-ui-search-bar';
import AccountCircleIcon from '@material-ui/icons/AccountCircle';
import StarsIcon from '@material-ui/icons/Stars';
import Chip from '@material-ui/core/Chip';
import {emphasize} from "@material-ui/core";

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
    breadcrumb: {
        paddingRight: `20px`,
    },
    activeFavourites: {
        backgroundColor: 'whitesmoke',
        color: "primary",
        fontWeight: theme.typography.fontWeightBold,
        '&:hover, &:focus': {
        backgroundColor: 'lightskyblue'
        },
        '&:active': {
        boxShadow: theme.shadows[1],
        backgroundColor: 'cyan'
        },
    }
}));

const StyledBreadcrumb = withStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.grey[100],
    height: theme.spacing(3),
    color: theme.palette.grey[800],
    fontWeight: theme.typography.fontWeightBold,
    '&:hover, &:focus': {
      backgroundColor: theme.palette.grey[300],
    },
    '&:active': {
      boxShadow: theme.shadows[1],
      backgroundColor: emphasize(theme.palette.grey[300], 0.12),
    },
  },
}))(Chip);

function Header() {
    let favourites;
    const classes = useStyles();
    let history = useHistory();
    const [data, setData] = useState({ search: '' });

	const goSearch = (e) => {
        history.push({
            pathname: '/search/',
            search: '?search=' + data.search,
        });
        window.location.reload();
    };

    if (localStorage.getItem('Username')) {
        favourites =
            <Link
                component={NavLink}
                to="/favourites">
                <Breadcrumbs className={classes.breadcrumb}>

                    <Chip label="Favourites" icon={<StarsIcon style={{fill: 'green', fontSize: "avatarSmall"}}/>} className={classes.activeFavourites}/>

                </Breadcrumbs>
            </Link>
    } else {
        favourites =
            <Breadcrumbs className={classes.breadcrumb}>
                <StyledBreadcrumb label="Favourites" icon={<StarsIcon fontSize="avatarSmall"/>}/>
            </Breadcrumbs>
    }

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
                    <Typography variant="h6" color="inherit" noWrap className={classes.toolbarTitle}>
                        <Link
                            component={NavLink}
                            to="/"
                            underline="none"
                            color="inherit"
                        >
                            MotoCrawler
                        </Link>
                    </Typography>
                    <Typography variant="subtitle2" gutterBottom={true} color="textSecondary">
                        <Breadcrumbs className={classes.breadcrumb}>
                          <StyledBreadcrumb
                            label= {`Current User:${localStorage.getItem('Username')
                                        ? " " + localStorage.getItem('Username')
                                        : "Anonymous"}`}
                            icon={<AccountCircleIcon style={{fontSize: 'avatarSmall', fill: 'cornflowerblue'}} />}
                          />
                        </Breadcrumbs>
                        {favourites}
                    </Typography>
                    <SearchBar
						value={data.search}
						onChange={(newValue) => setData({ search: newValue })}
						onRequestSearch={() => goSearch(data.search)}
                        placeholder="Search by Model"
					/>
                    <Button
                        color="default"
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
