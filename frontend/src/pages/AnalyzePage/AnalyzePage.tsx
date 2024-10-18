import { useParams } from "react-router-dom";

export const AnalyzePage = () => {
    const { id } = useParams();
    return <div>Анализ файла {id}</div>;
}