import React from "react";
import Toolbar from "@mui/material/Toolbar";
import {ComputerOutlined} from "@mui/icons-material";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import AppBar from "@mui/material/AppBar";
import {useLocation, useNavigate} from "react-router-dom";
import {Link as RouterLink} from "react-router-dom";
import Avatar from '@mui/material/Avatar';
import {Divider, IconButton} from "@mui/material";


export default function CustomAppBar(props) {
    const location = useLocation();
    const navigate = useNavigate();
    const token = sessionStorage.getItem('token')
    const user = JSON.parse(sessionStorage.getItem('user'));

    return (
        <AppBar
            position="static"
            color="default"
            elevation={0}
            sx={{borderBottom: (theme) => `1px solid ${theme.palette.divider}`}}
        >
            <Toolbar sx={{flexWrap: 'wrap'}}>
                <ComputerOutlined sx={{mx: 1}}/>
                <Typography variant="h6" color="inherit" noWrap sx={{flexGrow: 1}}>
                    Диспетчер суперкомпьютера
                </Typography>
                <nav>
                    <Button
                        component={RouterLink}
                        variant="text"
                        color={location.pathname === "/" ? "primary" : "inherit"}
                        to="/"
                        sx={{my: 1, mx: 1.5}}
                    >
                        Главная страница
                    </Button>
                    <Button
                        component={RouterLink}
                        variant="text"
                        color={location.pathname === "/tasks" ? "primary" : "inherit"}
                        to="/tasks"
                        sx={{my: 1, mx: 1.5}}
                    >
                        Список задач
                    </Button>
                    <Button
                        component={RouterLink}
                        variant="text"
                        color={location.pathname === "/order" ? "primary" : "inherit"}
                        to="/order"
                        sx={{my: 1, mx: 1.5}}
                    >
                        Очередь
                    </Button>
                    {token !== null && user.is_staff === true ? 
                    <Button
                        component={RouterLink}
                        variant="text"
                        color={location.pathname === "/system" ? "primary" : "inherit"}
                        to="/system"
                        sx={{my: 1, mx: 1.5}}
                    >
                        Системы
                    </Button>
                : <></>}
                </nav>
                {token != null ?
                    <>
                        <Divider orientation="vertical" variant="middle" flexItem sx={{mx: 2}}/>
                        <IconButton onClick={() => navigate('/user')}>
                            <Avatar>
                                {user?.first_name?.substring(0, 1)}{user?.last_name?.substring(0, 1)}
                            </Avatar>
                        </IconButton>
                        <Typography variant="inherit" noWrap sx={{my: 1, mx: 1.5}}>
                            {user?.first_name} {user?.last_name}
                        </Typography>
                        <Button
                            onClick={e => {
                                sessionStorage.removeItem('token');
                                navigate('/', {replace: true})
                            }}
                            variant="contained"
                            sx={{my: 1, mx: 1.5}}
                        >
                            Выход
                        </Button>
                    </>
                    : <>
                        <Button
                            component={RouterLink}
                            variant="outlined"
                            to="/login"
                            sx={{my: 1, mx: 1.5}}
                        >
                            Войти
                        </Button>
                        <Button
                            component={RouterLink}
                            variant="contained"
                            to="/register"
                            sx={{my: 1, mx: 1.5}}
                        >
                            Зарегистрироваться
                        </Button>
                    </>
                }
            </Toolbar>
        </AppBar>
    )
};
