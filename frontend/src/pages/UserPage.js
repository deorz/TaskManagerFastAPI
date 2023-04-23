import React, {useState} from "react";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import Requests from "../requests/Requests";
import { useNavigate } from "react-router-dom";

export default function UserPage() {
    return (
        <>
            <UserForm/>
        </>
    )
}

function UserForm() {
    const navigate = useNavigate();
    const user = JSON.parse(localStorage.getItem('user'));
    const [passwordRequired, setRequired] = useState(false);
    
    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const response = await Requests.updateUser({
            userId: user.id_user,
            first_name: formData.get('first_name'),
            last_name: formData.get('last_name'),
            username: formData.get('username'),
            password: formData.get('password'),
            new_password: formData.get('new_password')
        })
        const userData = await response.json();
        if (response.status < 400) {
            localStorage.setItem('user', JSON.stringify(userData));
            navigate('/', {replace: true})
        }
        else {
            alert(userData.detail);
        }
    };
    
    const handleChange = (event) => {
        let value = event.target.value;
        if (value !== '') {
            setRequired(true)
        } else {
            setRequired(false)
        }
    }
    
    return (
        <>
            <Container disableGutters maxWidth="sm" component="main" sx={{pt: 8, pb: 4}}>
                <Typography
                    component="h1"
                    variant="h2"
                    align="center"
                    color="text.primary"
                    gutterBottom
                >
                    Страница пользователя
                </Typography>
            </Container>
            <Container disableGutters maxWidth="sm" component="main" sx={{pt: 4, pb: 4}}>
                <Box component="form" onSubmit={handleSubmit} noValidate sx={{mt: 3}}>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <TextField
                            fullWidth
                            id="first_name"
                            label="Имя"
                            name="first_name"
                            defaultValue={user.first_name}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                id="last_name"
                                label="Фамилия"
                                name="last_name"
                                defaultValue={user.last_name}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                id="username"
                                label="Имя пользователя"
                                name="username"
                                defaultValue={user.username}
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                name="password"
                                label="Пароль"
                                id="password"
                                onChange={handleChange}
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                required={passwordRequired}
                                name="new_password"
                                label="Новый Пароль"
                                id="new_password"
                                autoComplete="current-password"
                            />
                        </Grid>
                    </Grid>
                    <Button
                        type="submit"
                        variant="contained"
                        sx={{mt: 3, mb: 2}}
                    >
                        Обновить
                    </Button>
                </Box>
            </Container>
        </>
    )
}