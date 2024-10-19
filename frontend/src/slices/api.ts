import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { BASE_URL } from '../types/constants';

export const API = createApi({
    reducerPath: 'api',
    baseQuery: fetchBaseQuery({ baseUrl: BASE_URL }),
    tagTypes: [],
    refetchOnFocus: true,
    refetchOnReconnect: true,
    refetchOnMountOrArgChange: true,
    keepUnusedDataFor: 10000,
    endpoints: (builder) => ({
        uploadFile: builder.mutation<void, File>({
            query: (file) => {
                const formData = new FormData();
                formData.append('file', file);

                return {
                    url: "files/upload",
                    method: 'POST',
                    credentials: 'include',
                    body: formData,                
                };
            },
            transformResponse: (_, meta) => {
                if(meta?.response) localStorage.setItem('sessionId', meta.response.headers.get('set-cookie') || "");
            },
        }),
        getClusters: builder.query<string[], void>({
            query: () => ({
                url: "clusters",
                credentials: 'include',
                method: 'GET',
            }),
        }),
        getClusterById: builder.query<Array<[Array<[string, number]>, number]>, string>({
            query: (id) => ({
                url: `clusters/${id}`,
                credentials: 'include',
                method: 'GET',
            }),
        }),
        getText: builder.mutation<string, {question: string, mainPoints: string[]}>({
            query: ({question, mainPoints}) => ({
                url: `magic`,
                credentials: 'include',
                method: 'POST',
                body: JSON.stringify({
                    question: question,
                    mainPoints: mainPoints,
                }),
                headers: {
                    'Content-Type': 'application/json',
                }
            }),
        }),
        getWordFrequence: builder.mutation<string, {mainPoints: string[]}>({
            query: ({mainPoints}) => ({
                url: `magic_points`,
                credentials: 'include',
                method: 'POST',
                body: JSON.stringify({
                    mainPoints: mainPoints,
                }),
                headers: {
                    'Content-Type': 'application/json',
                }
            }),
        }),
        healthCheck: builder.query<void, void>({
            query: () => ({
                url: "health",
                method: 'GET',
            }),
        }),
    })
})

export const {
    useGetTextMutation,
    useHealthCheckQuery,
    useGetClustersQuery,
    useGetWordFrequenceMutation,
    useGetClusterByIdQuery,
    useUploadFileMutation
} = API;