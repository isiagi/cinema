import axios from "axios";

const API_URL = "http://127.0.0.1:8000/auth";

export const login = async (email: string, password: string) => {
    return axios.post(`${API_URL}/login/`, { email, password });
};

export const register = async (userData: { email: string, name: string, password: string }) => {
    return axios.post(`${API_URL}/create-account/`, userData);
};

export const forgot_password = async (email: string) => {
    return axios.post(`${API_URL}/forgot-password/`, { email });
};

export const resetPassword = async (uidb64: string, token: string, newPassword: string) => {
    return axios.post(`${API_URL}/reset-password/${uidb64}/${token}/`, { new_password: newPassword });
};
