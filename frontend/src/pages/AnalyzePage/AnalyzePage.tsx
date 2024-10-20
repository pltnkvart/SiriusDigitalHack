import { useEffect, useState } from "react";
import { useGetClusterByIdQuery, useGetTextMutation, useGetWordFrequenceMutation } from "../../slices/api";
import { Button, Card, Skeleton } from "@gravity-ui/uikit";
import Markdown from "react-markdown";
import styles from './styles.module.css';
import { PieChart, Pie, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { PageLayout } from "../../components/PageLayout/PageLayout";
import { QUESTIONS } from "../../types/constants";
import { useNavigate, useParams } from "react-router-dom";

export const AnalyzePage = () => {
    const navigate = useNavigate();
    const { questionId } = useParams();
    const { data, isLoading } = useGetClusterByIdQuery(String(questionId));
    const [getText, { data: text, isLoading: isLoadingText }] = useGetTextMutation();
    const [words, setWords] = useState<(string | undefined)[]>([]);
    const [frequencies, setFrequencies] = useState<(number | undefined)[]>([]);
    const [getMainInfo, { isLoading: isLoadingMainInfo }] = useGetWordFrequenceMutation();

    useEffect(() => {
        const fetchText = async () => {
            if (data) {
                const toSend = data[0].map(item =>
                    item[0].map((word: string[]) => word.join(' ')).join(' ')
                );

                const wordsPromises = toSend.map(async (mainPoint, index) => {
                    if (mainPoint) {
                        const mainInfoResponse = await getMainInfo({ mainPoints: mainPoint });

                        if (mainInfoResponse.error) {
                            console.error("Failed to fetch main info", mainInfoResponse.error);
                            return { word: null, frequency: null };
                        } else {
                            return {
                                word: mainInfoResponse.data,
                                frequency: parseInt(data[0][index][1]) // Ensure conversion to number
                            };
                        }
                    }
                });

                // Wait for all main info data
                const resolvedWordData = await Promise.all(wordsPromises);

                const filteredWords = resolvedWordData.map(item => item?.word).filter(Boolean);
                const filteredFrequencies = resolvedWordData.map(item => item?.frequency).filter(Boolean);

                // Logs for debugging
                console.log("Words:", filteredWords);
                console.log("Frequencies:", filteredFrequencies);

                setWords(filteredWords.join(', ').split(', '));
                setFrequencies(filteredFrequencies);

                await getText({
                    question: 'Какие причины (факторы) сформировали ваше решение уйти из компании?',
                    mainPoints: toSend,
                });
            }
        };
        fetchText();
    }, [data]);

    const goToNextQuestion = () => {
        navigate('/analyze/' + (Number(questionId) + 1));
    };

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

    const DATA = words.map((word, index) => ({
        name: word,
        value: frequencies[index],
    }));

    console.log(DATA);

    return (
        <PageLayout isLoading={isLoading}>
            Вопрос: {QUESTIONS[Number(questionId) - 1]}
            <br />
            Количество кластеров: {data && data[0].length}
            <Button
                type="submit"
                view="action"
                size="m"
                onClick={goToNextQuestion}
                className={styles.analyze}
                disabled={questionId === '6'}
            >
                Следующий вопрос
            </Button>
            <div className={styles.flex}>
                <ResponsiveContainer height={"400px"}>
                    <PieChart>
                        <Pie
                            data={DATA}
                            dataKey="value"
                            cx="50%"
                            cy="50%"
                            outerRadius={150}
                            height={"400px"}
                            fill={COLORS[Math.floor(Math.random() * COLORS.length)]}
                            label
                        >{
                                DATA.map((_, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))
                            }
                            <Tooltip />
                        </Pie>
                        <Legend layout="vertical" align="right" verticalAlign="middle" />
                    </PieChart>
                </ResponsiveContainer>
                {isLoadingText ? <Skeleton className={styles.card} /> : <Card view='outlined' type="action"><><Markdown>{text}</Markdown></></Card>}
                {isLoadingMainInfo ? <Skeleton className={styles.card} /> :
                    data && data[0].map((item: [string, number][], index: number) => (
                        <div key={index}>
                            <p>Частота встречаемости: {item[1]}</p>
                            <p>Основная мысль: {words[index]}</p>
                        </div>
                    ))}
            </div>
        </PageLayout>
    );
};