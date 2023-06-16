import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';


const tiers = [
    {
        title: 'Задачи',
        description: [
            'Возможность загрузить программу на сервер',
            'Указать количество потоков исполнения',
            'Запускать программу на выполнение в любой удобный момент',
        ],
    },
    {
        title: 'Стэк',
        description: [
            'Python',
            'FastAPI',
            'PostgreSQL@14',
            'React JS',
            'React Material UI'
        ],
    },
    {
        title: 'Приоритет',
        description: [
            'Приоритет задачи и количество процессорных ядер используются для автоматического управления выполнением задач',
            'Т.е. если есть свободные процессорные ядра из очереди берется самая приоритетная задача',
        ],
    },
];

function HomePageContent() {
    return (
        <React.Fragment>
            <Container disableGutters maxWidth="sm" component="main" sx={{pt: 8, pb: 6}}>
                <Typography
                    component="h1"
                    variant="h2"
                    align="center"
                    color="text.primary"
                    gutterBottom
                >
                    Диспетчер задач для суперкомпьютера
                </Typography>
                <Typography variant="h5" align="center" color="text.secondary" component="p">
                    Магистерская работа Орженовского Дениса Станиславовича, студента
                    Национального исследовательского университета «Московского Энергетического Института»
                    группы А-14м-21
                </Typography>
            </Container>
            <Container maxWidth="lg" component="main">
                <Grid container spacing={8} alignItems="flex-end">
                    {tiers.map((tier) => (
                        <Grid
                            item
                            key={tier.title}
                            xs={6}
                            md={4}
                        >
                            <Card>
                                <CardHeader
                                    title={tier.title}
                                    subheader={tier.subheader}
                                    titleTypographyProps={{align: 'center'}}
                                    subheaderTypographyProps={{
                                        align: 'center',
                                    }}
                                    sx={{
                                        backgroundColor: (theme) =>
                                            theme.palette.mode === 'light'
                                                ? theme.palette.grey[200]
                                                : theme.palette.grey[700],
                                    }}
                                />
                                <CardContent>
                                    {tier.description.map((line) => (
                                        <Typography
                                            component="li"
                                            variant="subtitle1"
                                            align="center"
                                            key={line}
                                        >
                                            {line}
                                        </Typography>
                                    ))}
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Container>
            <Container
                maxWidth="md"
                component="footer"
                sx={{
                    borderTop: (theme) => `1px solid ${theme.palette.divider}`,
                    mt: 8,
                    py: [3, 6],
                }}
            >
            </Container>
        </React.Fragment>
    );
}

export default function HomePage() {
    return (
        <>
            <HomePageContent/>
        </>
    );
}
