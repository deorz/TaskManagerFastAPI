import React, {useEffect, useState, useRef} from "react";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import TableBody from "@mui/material/TableBody";
import TableContainer from "@mui/material/TableContainer";
import { useNavigate } from 'react-router-dom';
import Requests from "../requests/Requests";


export default function OrderPage () {
    return (
        <>
            <OrderContent/>
        </>
    )
};

function OrderContent() {
    const [data, setData] = useState([]);
    const navigate = useNavigate();
    const dataFetchedRef = useRef(false);

    const getOrder = async () => {
        const token = localStorage.getItem('token')
        if (token) {
            try {
                const response = await Requests.getOrder();
                const json = await response.json();
                setData(json);
            } catch (error) {
                console.error(error);
            }
        } else {
            navigate('/login', {replace: true})
        }
    }

    useEffect(() => {
        if (dataFetchedRef.current) return;
        dataFetchedRef.current = true;
        getOrder();
    }, []);

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
                    Очередь исполнения
                </Typography>
            </Container>
            <Container disableGutters maxWidth="lg" component="main" sx={{pt: 4, pb: 4}}>
                <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell align="left">Имя файла</TableCell>
                                <TableCell align="center">Количество потоков</TableCell>
                                <TableCell align="center">Приоритет</TableCell>
                                <TableCell align="center">Создано</TableCell>
                                <TableCell align="center">Номер в очереди</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data.map((row) => (
                                <TableRow
                                    key={row.task.id_task}
                                    sx={{'&:last-child td, &:last-child th': {border: 0}}}
                                >
                                    <TableCell align="left" component="th" scope="row">
                                        {row.task.file?.readable_file_name}
                                    </TableCell>
                                    <TableCell align="center">{row.task.num_threads}</TableCell>
                                    <TableCell align="center">{row.task.priority}</TableCell>
                                    <TableCell align="center">{row.task.created_at.replace('T', ' ')}</TableCell>
                                    <TableCell align="center">{row.order_number}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Container>
        </React.Fragment>
    )
}
