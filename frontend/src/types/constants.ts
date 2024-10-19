import {File} from '@gravity-ui/icons';

export const SERVICE_NAME = "Greenatom";

const PORT = 5050;
const HOST = "http://localhost"
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
