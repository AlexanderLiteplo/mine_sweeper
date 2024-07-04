import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';

export const initializeBoard = (width: number, height: number, numMines: number) => {
    return axios.post(`${API_URL}/initialize_board`, { width, height, numMines });
};

export const placeMines = (firstClickLocation: [number, number]) => {
    return axios.post(`${API_URL}/place_mines`, { firstClickLocation });
};