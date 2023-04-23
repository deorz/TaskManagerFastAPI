import React, {useEffect, useRef, useState} from "react";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import TableBody from "@mui/material/TableBody";
import TableContainer from "@mui/material/TableContainer";
import Requests from "../requests/Requests";
import {useNavigate} from "react-router-dom";
import {
    Divider,
    FormHelperText,
    IconButton,
    MenuItem,
    Modal, Skeleton,
    Stack,
} from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import SearchIcon from '@mui/icons-material/Search';
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import FileUpload from "../components/FileUpload";
import {Close} from "@mui/icons-material";

function CreateTaskForm(props) {
    const handleSubmit = props.hanleSubmit;
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
                    Создать задачу
                </Typography>
                <Box component="form" onSubmit={handleSubmit} noValidate sx={{mt: 3}}>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <Typography align="center" variant="subtitle1" sx={{pb: 2}}>
                                Исполняемый Python Файл
                            </Typography>
                            <FileUpload file={props.file} setFile={props.setFile}/>
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                id="params"
                                label="Параметры командной строки"
                                name="params"
                            />
                            <FormHelperText>
                                Обратите внимание, что динамический ввод данных доступен только через аргументы
                                командной строки
                            </FormHelperText>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                select
                                required
                                fullWidth
                                defaultValue={1}
                                id="num_threads"
                                label="Количество потоков"
                                name="num_threads"
                            >
                                {new Array(8).fill().map(
                                    (_, option) => (
                                        <MenuItem key={option + 1} value={option + 1}>
                                            {option + 1}
                                        </MenuItem>
                                    ),
                                )}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                select
                                required
                                fullWidth
                                name="priority"
                                defaultValue={1}
                                label="Приоритет"
                                id="priority"
                            >
                                {new Array(100).fill().map(
                                    (_, option) => (
                                        <MenuItem key={option + 1} value={option + 1}>
                                            {option + 1}
                                        </MenuItem>
                                    ),
                                )}
                            </TextField>
                        </Grid>
                    </Grid>
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{mt: 3, mb: 2}}
                    >
                        Создать
                    </Button>
                </Box>
            </Box>
        </React.Fragment>
    )
}

function TaskViewForm(props) {
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
                <Stack direction="row" justifyContent="space-between">
                    <Typography component="h1" variant="h5">
                        Задача
                    </Typography>
                    <IconButton onClick={() => props.handleClose()}>
                        <Close/>
                    </IconButton>
                </Stack>
                <Box component="form" noValidate sx={{mt: 3}}>
                    {
                        props.loading ?
                            <Grid container spacing={2}>
                                <Grid item xs={12}>
                                    <Skeleton variant="rounded" width={600} height={50}/>
                                </Grid>
                                <Grid item xs={12}>
                                    <Skeleton variant="rounded" width={600} height={50}/>
                                </Grid>
                                <Grid item xs={12}>
                                    <Skeleton variant="rounded" width={600} height={50}/>
                                </Grid>
                                <Grid item xs={12}>
                                    <Skeleton variant="rounded" width={600} height={50}/>
                                </Grid>
                                <Grid item xs={12}>
                                    <Skeleton variant="rounded" width={600} height={50}/>
                                </Grid>
                                <Grid item xs={12}>
                                    <Skeleton variant="rounded" width={600} height={50}/>
                                </Grid>
                                <Grid item xs={12}>
                                    <Skeleton variant="rounded" width={600} height={50}/>
                                </Grid>
                                <Grid item xs={12}>
                                    <Skeleton variant="rounded" width={600} height={50}/>
                                </Grid>
                            </Grid>
                            :
                            <Grid container spacing={2}>
                                <Grid item xs={12}>
                                    <TextField
                                        fullWidth
                                        disabled
                                        type="text"
                                        label="Файл"
                                        value={props.data.file.readable_file_name}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        fullWidth
                                        disabled
                                        type="text"
                                        label="Параметры командной строки"
                                        value={props.data.params}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        fullWidth
                                        disabled
                                        type="number"
                                        label="Приоритет"
                                        value={props.data.priority}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        fullWidth
                                        disabled
                                        type="text"
                                        label="Создано"
                                        value={props.data.created_at.replace('T', ' ')}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={4}>
                                    <TextField
                                        fullWidth
                                        disabled
                                        type="text"
                                        label="Статус"
                                        value={props.data.status.name}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={2}>
                                    <TextField
                                        fullWidth
                                        disabled
                                        type="number"
                                        label="Код"
                                        value={props.data.exitcode}
                                    />
                                </Grid>
                                <Grid item xs={12}>
                                    <TextField
                                        fullWidth
                                        multiline
                                        disabled
                                        type="text"
                                        label="Результат выполнения"
                                        value={props.data.output}
                                    />
                                </Grid>
                                <Grid item xs={12}>
                                    <TextField
                                        fullWidth
                                        multiline
                                        disabled
                                        type="text"
                                        label="Ошибки"
                                        value={props.data.errors}
                                    />
                                </Grid>
                            </Grid>
                    }
                </Box>
            </Box>
        </React.Fragment>
    )
}

function TasksContent() {
    const [tasksData, setTasksData] = useState([]);
    const [createOpen, setCreateOpen] = useState(false);
    const [infoOpen, setInfoOpen] = useState(false);
    const [infoLoading, setInfoLoading] = React.useState(false);
    const [taskData, setTaskData] = useState({})
    const [file, setFile] = useState();
    const navigate = useNavigate();
    const handleCreateOpen = () => setCreateOpen(true);
    const handleCreateClose = () => setCreateOpen(false);
    const handleInfoOpen = () => setInfoOpen(true);
    const handleInfoClose = () => setInfoOpen(false);
    const dataFetchedRef = useRef(false);

    const delay = ms => new Promise(
        resolve => setTimeout(resolve, ms)
    );

    const getTasks = async () => {
        const token = localStorage.getItem('token')
        if (token) {
            try {
                const response = await Requests.getTasks();
                const json = await response.json();
                setTasksData(json);
            } catch (error) {
                console.error(error);
            }
        } else {
            navigate('/login', {replace: true})
        }
    };

    const deleteTask = async (task_id) => {
        const response = await Requests.deleteTask({task_id: task_id});
        if (response.status === 400) {
            const result = await response.json();
            alert(result.detail);
        }
        await getTasks();
    };

    const executeTask = async (task_id) => {
        const response = await Requests.executeTask({task_id: task_id});
        const result = await response.json();
        alert(result.detail);
    };

    const showTaskInfo = async (task_id) => {
        setInfoLoading(true);
        handleInfoOpen();
        const response = await Requests.getTask({task_id: task_id})
        const result = await response.json();
        setTaskData(result);
        await delay(1000);
        setInfoLoading(false);
    };

    useEffect(() => {
        if (dataFetchedRef.current) return;
        dataFetchedRef.current = true;
        getTasks();
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        await Requests.createTask({
            file: {
                "name": file.name,
                "mimetype": file.mimetype,
                "body": file.body
            },
            params: data.get('params'),
            num_threads: data.get('num_threads'),
            priority: data.get('priority'),
        })
        setFile({});
        handleCreateClose();
        await getTasks();
    };

    return (
        <React.Fragment>
            <Container disableGutters maxWidth="sm" component="main" sx={{pt: 8, pb: 4}}>
                <Typography
                    component="h1"
                    variant="h2"
                    align="center"
                    color="text.primary"
                    gutterBottom
                >
                    Список задач
                </Typography>
            </Container>
            <Container disableGutters maxWidth="lg" component="main" sx={{pt: 4, pb: 4}}>
                <Button onClick={handleCreateOpen} variant="contained" sx={{my: 4}}>
                    Создать
                </Button>
                <Modal
                    open={createOpen}
                    onClose={handleCreateClose}
                    aria-labelledby="create-task-modal"
                >
                    <Box>
                        <CreateTaskForm hanleSubmit={handleSubmit} file={file} setFile={setFile}/>
                    </Box>
                </Modal>
                <Modal
                    open={infoOpen}
                    onClose={handleInfoClose}
                    aria-labelledby="task-info-modal"
                >
                    <Box>
                        <TaskViewForm data={taskData} handleClose={handleInfoClose} loading={infoLoading}/>
                    </Box>
                </Modal>
                <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell/>
                                <TableCell align="left">Имя файла</TableCell>
                                <TableCell align="center">Количество потоков</TableCell>
                                <TableCell align="center">Приоритет</TableCell>
                                <TableCell align="center">Создано</TableCell>
                                <TableCell align="center">Статус</TableCell>
                                <TableCell/>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {tasksData.map((row) => (
                                <TableRow
                                    key={row.id_task}
                                    sx={{'&:last-child td, &:last-child th': {border: 0}}}
                                >
                                    <TableCell>
                                        <Stack direction="row" spacing={1}>
                                            <IconButton onClick={() => deleteTask(row.id_task)} size="small">
                                                <DeleteIcon/>
                                            </IconButton>
                                            <Divider orientation="vertical" variant="middle" flexItem/>
                                            <IconButton onClick={() => showTaskInfo(row.id_task)} size="small">
                                                <SearchIcon/>
                                            </IconButton>
                                        </Stack>
                                    </TableCell>
                                    <TableCell align="left" component="th" scope="row">
                                        {row.file?.readable_file_name}
                                    </TableCell>
                                    <TableCell align="center">{row.num_threads}</TableCell>
                                    <TableCell align="center">{row.priority}</TableCell>
                                    <TableCell align="center">{row.created_at.replace('T', ' ')}</TableCell>
                                    <TableCell align="center">{row.status?.name}</TableCell>
                                    <TableCell>
                                        <IconButton onClick={() => executeTask(row.id_task)} size="small">
                                            <PlayArrowIcon/>
                                        </IconButton>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Container>
        </React.Fragment>
    )
}

export default function TasksPage() {
    return (
        <>
            <TasksContent/>
        </>
    )
};
