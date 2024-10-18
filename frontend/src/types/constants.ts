import {File} from '@gravity-ui/icons';

export const SERVICE_NAME = "Greenatom";

const PORT = 5000;
const HOST = "http://127.0.0.1"
const URL = `${HOST}:${PORT}`;

export const BASE_URL = `${URL}`;

export const MENU_ITEMS = [
    {
        id: 'upload',
        title: 'Загрузка файла',
        path: '/',
        icon: File,
    },
];

export interface IError{
    status: number;
    message: string;
}
