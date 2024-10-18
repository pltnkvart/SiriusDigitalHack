import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { BASE_URL } from '../types/constants';

export const API = createApi({
    reducerPath: 'api',
    baseQuery: fetchBaseQuery({ baseUrl: BASE_URL }),
    tagTypes: [],
    refetchOnFocus: true,
    refetchOnReconnect: true,
    refetchOnMountOrArgChange: true,
    endpoints: (builder) => ({
        uploadFile: builder.mutation<void, File>({
            query: (file) => {
                const formData = new FormData();
                formData.append('file', file);

                return {
                    url: "files/upload",
                    method: 'POST',
                    body: formData,                
                };
            },
            transformResponse: (_, meta) => {
                if(meta?.response) localStorage.setItem('sessionId', meta.response.headers.get('set-cookie') || "");
            },
        }),
        getClusters: builder.query<string[], string>({
            query: (sessionCookie) => ({
                url: "clusters",
                headers: {
                    'Cookie': sessionCookie
                },
                credentials: 'include',
                method: 'GET',
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
    useHealthCheckQuery,
    useGetClustersQuery,
    useUploadFileMutation
} = API;