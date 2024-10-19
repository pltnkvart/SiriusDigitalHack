import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Layout } from './components/Layout/Layout';
import { ErrorPage } from './pages/ErrorPage/ErrorPage';
import { InputFilePage } from './pages/InputFilePage/InputFilePage';
import { AnalyzePage } from './pages/AnalyzePage/AnalyzePage';

export const App = () => {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route
            path="/"
            element={<InputFilePage />}
            errorElement={<ErrorPage />}
          />
          <Route
            path="/analyze"
            element={<AnalyzePage />}
            errorElement={<ErrorPage />}
          />
          <Route path="*" element={<ErrorPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
};