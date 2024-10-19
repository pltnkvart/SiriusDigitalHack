import { useEffect, useState } from "react";
import { useGetClusterByIdQuery, useGetTextMutation, useGetWordFrequenceMutation } from "../../slices/api";
import { Loader, Text } from "@gravity-ui/uikit";
import { settings } from '@gravity-ui/chartkit';
import { YagrPlugin } from '@gravity-ui/chartkit/yagr';
import { Chart } from "../../components/Charts/Chart";
import Markdown from "react-markdown";

settings.set({ plugins: [YagrPlugin] });

export const AnalyzePage = () => {
    const { data, isLoading } = useGetClusterByIdQuery(1);
    const [getText, { data: text, isLoading: isLoadingText }] = useGetTextMutation();
    const [words, setWords] = useState<string[]>([]);
    const [getMainInfo] = useGetWordFrequenceMutation();

    useEffect(() => {
        const fetchText = async () => {
            if (data) {
                const mainInfo = await getMainInfo(data[0].map((item: any) => item[0].map((word: string[]) => word.join(' '))))
                setWords([...words, ...mainInfo]);
                await getText({
                    question: 'Какие причины (факторы) сформировали ваше решение уйти из компании?',
                    mainPoints: data[0].map((item: any) => item[0].map((word: string[]) => word.join(' '))).join(' '),
                });
            }
        }
        fetchText();
    }, [getText, data]);

    const toString = (data: any) => {
        return data[0]?.map((item: any, index: number) => (
            `${index + 1}. Частота встречаемости: ${item[1]}. Слова: ${item[0].map((word: string[]) => word.join(' ')).join(' ')}`
        )).join('\n')
    }

    return (
        <div>
            {isLoading ? <Loader /> :
                <>
                    Количество кластеров: {data && data[0].length}
                    <br />
                    {data && data[0].map((item: string[][][]) => (
                        <>
                            <p>Частота встречаемости: {item[1]}</p>
                            <p>Слова: {item[0].map((word: string[]) => word.join(' ')).join(' ')}</p>
                        </>
                    ))}
                    <Chart />
                    {isLoadingText ? <Loader /> : <Markdown>{text}</Markdown>}
                    <Text variant="body-1" color="secondary">{toString(data)}</Text>
                </>
            }
        </div>
    );
}