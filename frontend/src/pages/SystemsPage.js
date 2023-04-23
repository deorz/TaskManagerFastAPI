import React, { useEffect, useRef, useState } from 'react';
import {
    Box, Button, Container, Divider, Grid, IconButton,
    Modal, Paper, Stack, Table, TableBody, TableCell,
    TableContainer, TableHead, TableRow, TextField, Typography
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import Requests from "../requests/Requests";

export default function SystemsPage() {
    return (
        <>
            <SystemsPageContent />
        </>
    );
};

function SystemsPageContent() {
    const [systemsData, setSystemsData] = useState([]);
    const [createOpen, setCreateOpen] = useState(false);
    const dataFetchedRef = useRef(false);

    const getSystems = async () => {
        const response = await Requests.getSystems();
        const data = await response.json();
        setSystemsData(data);
    }

    useEffect(() => {
        if (dataFetchedRef.current) return;
        dataFetchedRef.current = true;
        getSystems();
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        await Requests.createSystem({ host: data.get('host'), threads: data.get('threads') })

        setCreateOpen(false);
        await getSystems();
    };

    const changeSystemState = async (systemId) => {
        const response = await Requests.changeSystemState({ systemId: systemId });
        const data = await response.json();
        alert(data.detail);
        await getSystems();
    };

    const deleteSystem = async (systemId) => {
        const response = await Requests.deleteSystem({ systemId: systemId });
        const data = await response.json();
        alert(data.detail);
        await getSystems();
    }

    return (
        <>
            <Container disableGutters maxWidth="sm" component="main" sx={{ pt: 8, pb: 4 }}>
                <Typography
                    component="h1"
                    variant="h2"
                    align="center"
                    color="text.primary"
                    gutterBottom
                >
                    Виртуальные машины
                </Typography>
            </Container>
            <Container disableGutters maxWidth="lg" component="main" sx={{ pt: 4, pb: 4 }}>
                <Button onClick={() => setCreateOpen(true)} variant="contained" sx={{ my: 4 }}>
                    Создать
                </Button>
                <Modal
                    open={createOpen}
                    onClose={() => setCreateOpen(false)}
                    aria-labelledby="create-task-modal"
                >
                    <Box>
                        <CreateSystemForm handleSubmit={handleSubmit} />
                    </Box>
                </Modal>
                <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell />
                                <TableCell align="left">Хост</TableCell>
                                <TableCell align="center">Количество потоков</TableCell>
                                <TableCell align="center">Доступное количество потоков</TableCell>
                                <TableCell align="center">Активна</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {systemsData.map((row) => (
                                <TableRow
                                    key={row.id_system}
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell>
                                        <Stack direction="row" spacing={1}>
                                            <IconButton
                                                onClick={() => deleteSystem(row.id_system)}
                                                size="small"
                                            >
                                                <DeleteIcon />
                                            </IconButton>
                                            <Divider orientation="vertical" variant="middle" flexItem />
                                            <IconButton
                                                onClick={() => changeSystemState(row.id_system)}
                                                size="small"
                                                color={row.active ? "error" : "success"}
                                            >
                                                {row.active ? <StopIcon /> : <PlayArrowIcon />}
                                            </IconButton>
                                        </Stack>
                                    </TableCell>
                                    <TableCell align="left" component="th" scope="row">
                                        {row.host}
                                    </TableCell>
                                    <TableCell align="center">{row.threads}</TableCell>
                                    <TableCell align="center">{row.available_threads}</TableCell>
                                    <TableCell align="center">{row.active ? 'Да' : 'Нет'}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Container>
        </>
    );
};


function CreateSystemForm(props) {
    return (
        <React.Fragment>
            <Box sx={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                maxWidth: "lg",
                bgcolor: 'background.paper',
                p: 4,
            }}>
                <Typography component="h1" variant="h5">
                    Добавить виртуальную машину
                </Typography>
                <Box component="form" onSubmit={props.handleSubmit} noValidate sx={{ mt: 3 }}>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                id="host"
                                label="Хост машины (IP-адрес)"
                                name="host"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                required
                                fullWidth
                                type="number"
                                id="threads"
                                label="Количество потоков"
                                name="threads"
                            >
                            </TextField>
                        </Grid>
                    </Grid>
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2 }}
                    >
                        Создать
                    </Button>
                </Box>
            </Box>
        </React.Fragment>
    )
}