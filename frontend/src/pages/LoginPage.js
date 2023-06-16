import React from "react";
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import PersonIcon from '@mui/icons-material/Person';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import {Link as RouterLink, useNavigate} from "react-router-dom";

import Requests from "../requests/Requests";


export default function LoginPage () {
    const navigate = useNavigate();

    const authorization = async ({email, password}) => {
        const response = await Requests.signIn({email: email, password: password})
        const result = await response.json()
        if (result.access_token) {
            sessionStorage.setItem('token', result.access_token)
            const userResponse = await Requests.getUser();
            const userData = await userResponse.json();
            sessionStorage.setItem('user', JSON.stringify(userData));
            navigate('/', {replace: true})
        }
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        authorization({email: data.get('email'), password: data.get('password')});
    };
    return (
        <>
            <Container component="main" maxWidth="xs">
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                        <PersonIcon />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Вход
                    </Typography>
                    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Электронная почта"
                            name="email"
                            autoComplete="email"
                            autoFocus
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Пароль"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Войти
                        </Button>
                        <Grid container>
                            <Grid item xs>
                                <Link
                                    component={RouterLink}
                                    to="#"
                                    variant="body2"
                                >
                                    Забыли пароль?
                                </Link>
                            </Grid>
                            <Grid item>
                                <Link
                                    component={RouterLink}
                                    to="/register"
                                    variant="body2"
                                >
                                    Нет аккаунта? Зарегистрироваться
                                </Link>
                            </Grid>
                        </Grid>
                    </Box>
                </Box>
            </Container>
        </>
    )
};
