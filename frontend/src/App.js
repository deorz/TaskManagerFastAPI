import React from "react";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import TasksPage from "./pages/TasksPage";
import HomePage from "./pages/HomePage";
import OrderPage from "./pages/OrderPage";
import CssBaseline from "@mui/material/CssBaseline";
import GlobalStyles from "@mui/material/GlobalStyles";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import Footer from "./components/Footer";
import CustomAppBar from "./components/AppBar";
import UserPage from "./pages/UserPage";
import SystemsPage from "./pages/SystemsPage";

function App() {
    return (
        <div className="App">
            <GlobalStyles styles={{ul: {margin: 0, padding: 0, listStyle: 'none'}}}/>
            <CssBaseline/>
            <BrowserRouter>
            <CustomAppBar/>
                <Routes>
                    <Route path="/" element={<HomePage/>}/>
                    <Route path="tasks/" element={<TasksPage/>} exact/>
                    <Route path="order/" element={<OrderPage/>} exact/>
                    <Route path="login/" element={<LoginPage />} exact/>
                    <Route path="register/" element={<RegisterPage />} exact/>
                    <Route path="user/" element={<UserPage />} exact/>
                    <Route path="system/" element={<SystemsPage />} exact/>
                </Routes>
            </BrowserRouter>
            <Footer sx={{mt: 3}}/>
        </div>
    );
}

export default App;
