import { useParams } from "react-router-dom";
import { useGetClustersQuery } from "../../slices/api";
import { Loader } from "@gravity-ui/uikit";

export const AnalyzePage = () => {
    const { sessionId } = useParams();
    const { data: clusters, isLoading } = useGetClustersQuery(sessionId || "");

    return <div>{isLoading ? <Loader /> : clusters}</div>;
}