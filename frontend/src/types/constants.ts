import {LayoutRows3} from '@gravity-ui/icons';

export const SERVICE_NAME = "Greenatom";

const PORT = 3000;
const HOST = "http://localhost"
const URL = `${HOST}:${PORT}`;

export const BASE_URL = `${URL}/api/`;

export const MENU_ITEMS = [
    {
        id: 'upload',
        title: 'Загрузка файла',
        path: '/',
        icon: LayoutRows3,
    },
];

export interface IError{
    status: number;
    message: string;
}
