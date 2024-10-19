import { Text } from "@gravity-ui/uikit";
import ChartKit from '@gravity-ui/chartkit';
import type { YagrWidgetData } from '@gravity-ui/chartkit/yagr';

const data: YagrWidgetData = {
    data: {
        timeline: [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10
        ],
        graphs: [
            {
                id: '0',
                name: 'ПЕНСИЯ',
                color: 'rgba(255, 200, 92, 0.2)',
                data: Array.from({ length: 10 }, () => Math.floor(Math.random() * 100) + 1),
            },
        ],
    },
    libraryConfig: {
        chart: {
            series: {
                type: 'column',
            },
        },
        // title: {
        //     text: 'Burn-down Chart (График выполнения задач)',
        // },
    },
};

export const Chart = () => {
    return (
        <div >
            <ChartKit type="yagr" data={data} />
            <Text variant="body-1" color="secondary">Формула: Общее количество задач открытых - Сумма выполненных задач за день</Text>
        </div>
    );
}